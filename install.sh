#!/usr/bin/env bash
# Install GELLO + the local IIMT/Dynamixel integration on Ubuntu/Debian.
#
# Usage:
#   ./install.sh
#   ./install.sh --skip-system
#   ./install.sh --dev
#
# The script is intentionally idempotent. It uses the repository-local .venv
# and does not require "source .venv/bin/activate" for the final checks.

set -Eeuo pipefail
IFS=$'\n\t'

usage() {
    cat <<'EOF'
Usage: ./install.sh [options]

Options:
  --skip-system  Skip apt packages and dialout group setup.
  --dev          Also install requirements_dev.txt.
  -h, --help     Show this help.
EOF
}

skip_system=0
install_dev=0
for arg in "$@"; do
    case "$arg" in
        --skip-system)
            skip_system=1
            ;;
        --dev)
            install_dev=1
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        *)
            echo "Unknown option: $arg" >&2
            usage >&2
            exit 2
            ;;
    esac
done

if [ "$EUID" -eq 0 ]; then
    echo "请不要用 sudo 运行整个 install.sh。" >&2
    echo "直接运行 ./install.sh；脚本只在需要时对 apt/usermod 使用 sudo。" >&2
    exit 1
fi

repo_root="$(cd -- "$(dirname -- "$0")" && pwd)"
# If the file arrived from an archive without its executable bit, make the
# next invocation possible. The first invocation must use: bash install.sh.
chmod +x -- "$0" 2>/dev/null || true

user_name="$(id -un)"
user_home="$(getent passwd "$(id -u)" | cut -d: -f6)"
venv_dir="$repo_root/.venv"
python_bin="$venv_dir/bin/python"
sdk_demo_dir="$repo_root/third_party/IIMT-SDK/python/sdk_demo_py"
sdk_library="$repo_root/third_party/IIMT-SDK/python/linux/x64/lib/libiimtcl.so"

log() {
    printf '\n[install] %s\n' "$*"
}

warn() {
    printf '\n[install][WARN] %s\n' "$*" >&2
}

die() {
    printf '\n[install][ERROR] %s\n' "$*" >&2
    exit 1
}

if [ "$skip_system" -eq 0 ]; then
    command -v sudo >/dev/null 2>&1 || die "缺少 sudo；或者使用 --skip-system 跳过系统安装。"
    command -v apt-get >/dev/null 2>&1 || die "当前脚本需要 Ubuntu/Debian 的 apt-get。"

    log "安装系统工具、Qt X11 依赖和 Python 构建依赖"
    sudo apt-get update
    sudo apt-get install -y \
        build-essential \
        ca-certificates \
        curl \
        git \
        python3 \
        python3-venv \
        libegl1 \
        libgl1 \
        libxcb-cursor0 \
        libxcb-icccm4 \
        libxcb-image0 \
        libxcb-keysyms1 \
        libxcb-randr0 \
        libxcb-render-util0 \
        libxcb-shape0 \
        libxcb-sync1 \
        libxcb-xinerama0 \
        libxcb-xkb1 \
        libxkbcommon-x11-0

    log "把 $user_name 加入 dialout 组"
    sudo usermod -aG dialout "$user_name"
else
    warn "已跳过 apt 和 dialout 设置；请确认系统有 Qt xcb 依赖，且当前用户属于 dialout。"
fi

command -v git >/dev/null 2>&1 || die "缺少 git。"
command -v curl >/dev/null 2>&1 || die "缺少 curl。"

log "初始化 Git 子模块"
git -C "$repo_root" submodule update --init --recursive

if ! command -v uv >/dev/null 2>&1; then
    if [ -x "$user_home/.local/bin/uv" ]; then
        export PATH="$user_home/.local/bin:$PATH"
    else
        log "安装 uv"
        curl -LsSf https://astral.sh/uv/install.sh | sh
        export PATH="$user_home/.local/bin:$PATH"
    fi
fi
command -v uv >/dev/null 2>&1 || die "uv 安装后仍不可用，请重新打开终端后再运行。"
log "使用 $(uv --version)"

[ -f "$repo_root/requirements.txt" ] || die "找不到 requirements.txt。"
[ -f "$repo_root/setup.py" ] || die "找不到 setup.py。"
[ -f "$repo_root/third_party/DynamixelSDK/python/setup.py" ] \
    || die "找不到 third_party/DynamixelSDK/python，请先初始化 DynamixelSDK 子模块。"
[ -d "$sdk_demo_dir" ] \
    || die "找不到 IIMT SDK Python 目录：$sdk_demo_dir。请把 IIMT-SDK 放入 third_party/。"
[ -f "$sdk_library" ] \
    || die "找不到 IIMT Linux 动态库：$sdk_library。"

if [ ! -x "$python_bin" ]; then
    log "创建 Python 3.11 虚拟环境：$venv_dir"
    uv venv --python 3.11 "$venv_dir"
else
    log "复用已有虚拟环境：$venv_dir"
fi

log "安装 requirements.txt"
uv pip install --python "$python_bin" -r "$repo_root/requirements.txt"

log "安装 GELLO 本地包"
uv pip install --python "$python_bin" -e "$repo_root"

log "安装本地 DynamixelSDK Python 包"
uv pip install --python "$python_bin" -e \
    "$repo_root/third_party/DynamixelSDK/python"

if [ "$install_dev" -eq 1 ]; then
    log "安装开发依赖 requirements_dev.txt"
    uv pip install --python "$python_bin" -r \
        "$repo_root/requirements_dev.txt"
fi

log "执行 Python 核心依赖检查"
"$python_bin" - <<'PY'
import numpy
import omegaconf
import PyQt6
import tyro
import zmq
import dynamixel_sdk

print("Python dependencies: OK")
print("numpy:", numpy.__version__)
print("PyQt6: OK")
print("DynamixelSDK: OK")
PY

log "执行 IIMT SDK 动态库导入检查（不会登录机器人，不会运动）"
"$python_bin" - <<PY
from gello.robots.iimt import _load_iimt_sdk

_load_iimt_sdk("192.168.8.87", 29999)
print("IIMT SDK: OK")
PY

qt_plugin="$("$python_bin" - <<'PY'
from pathlib import Path
import PyQt6

print(Path(PyQt6.__file__).parent / "Qt6" / "plugins" / "platforms" / "libqxcb.so")
PY
)"

if command -v ldd >/dev/null 2>&1; then
    missing_libraries="$(ldd "$qt_plugin" 2>/dev/null | awk '/not found/ {print}')"
    if [ -n "$missing_libraries" ]; then
        warn "Qt xcb 插件仍有缺失动态库："
        printf '%s\n' "$missing_libraries" >&2
    else
        log "Qt xcb 平台插件依赖：OK"
    fi
fi

if id -nG "$user_name" | tr ' ' '\n' | grep -qx dialout; then
    log "当前登录会话已包含 dialout"
else
    warn "dialout 已写入用户组，但当前终端可能还未刷新。请注销并重新登录，或重启电脑。"
fi

cat <<EOF

安装完成。

项目目录：
  $repo_root

启动 Qt 监控/控制界面：
  cd $repo_root
  ./.venv/bin/python experiments/launch_yam_ui.py

读取 Gello 原始关节：
  ./.venv/bin/python scripts/read_gello.py \\
    --port /dev/serial/by-id/usb-FTDI_USB__-__Serial_Converter_FTBMFB57-if00-port0 \\
    --ids 1 2 3 4 5 6 \\
    --once

注意：
  1. IIMT-SDK 是本地文件，脚本只检查，不会从互联网下载。
  2. 当前 configs/iimt.yaml 使用 IIMT IP 192.168.8.87。
  3. 启动 Qt UI 前不要同时运行 launch_yaml.py 或 read_gello.py，以免占用串口。
  4. 加入 dialout 后需要重新登录，串口权限才会在新会话中生效。
EOF
