"""Qt GELLO/IIMT monitor and direct teleoperation launcher.

The window opens in read-only mode.  It continuously displays:

* the current six IIMT joint positions;
* the raw GELLO/Dynamixel positions;
* the converted IIMT target positions;
* target minus current error;

in both radians and degrees.

Only the "启动控制" button enables direct API_Servoj calls.  "停止控制"
clears the send flag but keeps the read-only monitor running.  No
逐步逼近/interpolation is performed here: every control-cycle target is sent
directly to the IIMT adapter.
"""

from __future__ import annotations

import argparse
import math
import re
import shutil
import sys
import threading
import time
from pathlib import Path
from typing import Sequence

import numpy as np
from dynamixel_sdk import COMM_SUCCESS, GroupSyncRead, PacketHandler, PortHandler
from omegaconf import DictConfig, OmegaConf

try:
    from PyQt6.QtCore import QThread, Qt, pyqtSignal
    from PyQt6.QtWidgets import (
        QApplication,
        QAbstractItemView,
        QGridLayout,
        QGroupBox,
        QHeaderView,
        QLabel,
        QMainWindow,
        QMessageBox,
        QPushButton,
        QTableWidget,
        QTableWidgetItem,
        QVBoxLayout,
        QWidget,
    )
except ModuleNotFoundError as exc:
    if exc.name and exc.name.startswith("PyQt6"):
        raise SystemExit(
            "缺少 PyQt6，请先执行：\n"
            "  uv pip install --python .venv/bin/python PyQt6"
        ) from exc
    raise

from gello.robots.iimt import IIMTRobot


PRESENT_POSITION_ADDRESS = 132
PRESENT_POSITION_LENGTH = 4
DEFAULT_BAUDRATE = 57600
DEFAULT_UI_UPDATE_PERIOD = 0.1


def read_raw_positions(
    reader: GroupSyncRead,
    ids: Sequence[int],
) -> np.ndarray:
    """Read Dynamixel present positions and convert encoder ticks to radians."""

    result = reader.txRxPacket()
    if result != COMM_SUCCESS:
        raise RuntimeError(f"Dynamixel read failed: {result}")

    positions = []
    for motor_id in ids:
        if not reader.isAvailable(
            motor_id, PRESENT_POSITION_ADDRESS, PRESENT_POSITION_LENGTH
        ):
            raise RuntimeError(f"Position unavailable for Dynamixel ID {motor_id}")

        ticks = reader.getData(
            motor_id, PRESENT_POSITION_ADDRESS, PRESENT_POSITION_LENGTH
        )
        if ticks > 0x7FFFFFFF:
            ticks -= 0x100000000
        positions.append(ticks / 2048.0 * math.pi)

    return np.asarray(positions, dtype=np.float64)


class ControlThread(QThread):
    """Owns the hardware connections and runs the read/send loop."""

    ready = pyqtSignal()
    data_updated = pyqtSignal(object)
    calibrated = pyqtSignal(object)
    error = pyqtSignal(str)

    def __init__(
        self,
        cfg: DictConfig,
        config_path: str,
        read_gripper: bool = True,
    ) -> None:
        super().__init__()
        self._cfg = cfg
        self._config_path = Path(config_path).resolve()
        self._read_gripper = read_gripper
        self._stop_requested = threading.Event()
        self._control_enabled = threading.Event()
        self._state_lock = threading.Lock()
        self._joint_offsets: np.ndarray | None = None
        self._joint_signs: np.ndarray | None = None
        self._latest_current_rad: np.ndarray | None = None
        self._latest_gello_raw_rad: np.ndarray | None = None

    def enable_control(self) -> None:
        self._control_enabled.set()

    def disable_control(self) -> None:
        self._control_enabled.clear()

    def request_stop(self) -> None:
        self._control_enabled.clear()
        self._stop_requested.set()

    def calibrate_current_pose(self) -> None:
        """Align Gello to the current IIMT pose and save new offsets.

        This only changes the offset mapping. It never calls API_Servoj.
        The operator must first place the IIMT arm and Gello in the same
        physical pose, with control stopped.
        """

        with self._state_lock:
            if (
                self._latest_current_rad is None
                or self._latest_gello_raw_rad is None
                or self._joint_signs is None
            ):
                raise RuntimeError("尚未取得完整的 IIMT/Gello 数据，不能标定")
            current_rad = self._latest_current_rad.copy()
            gello_raw_rad = self._latest_gello_raw_rad.copy()
            joint_signs = self._joint_signs.copy()

        # target = (raw - offset) * sign == current
        new_offsets = gello_raw_rad[:6] - joint_signs * current_rad
        if not np.all(np.isfinite(new_offsets)):
            raise RuntimeError("标定结果包含 NaN 或 infinity")
        if not self._config_path.is_file():
            raise FileNotFoundError(f"配置文件不存在：{self._config_path}")

        config_text = self._config_path.read_text(encoding="utf-8")
        pattern = re.compile(
            r"(?m)^([ \t]*joint_offsets:[ \t]*)"
            r"\[[^\]\n]*\]"
            r"([ \t]*(?:#.*)?)$"
        )

        def replace_offsets(match: re.Match[str]) -> str:
            values = ", ".join(f"{value:.6f}" for value in new_offsets)
            return f"{match.group(1)}[{values}]{match.group(2)}"

        updated_text, count = pattern.subn(
            replace_offsets, config_text, count=1
        )
        if count != 1:
            raise RuntimeError(
                f"在配置文件中没有找到唯一的 joint_offsets：{self._config_path}"
            )

        backup_path = self._config_path.with_suffix(
            self._config_path.suffix + ".bak"
        )
        temp_path = self._config_path.with_name(
            self._config_path.name + ".tmp"
        )
        shutil.copy2(self._config_path, backup_path)
        temp_path.write_text(updated_text, encoding="utf-8")
        temp_path.replace(self._config_path)

        with self._state_lock:
            self._joint_offsets = new_offsets.copy()
        self.calibrated.emit(new_offsets.copy())

    def run(self) -> None:
        port = None
        reader = None
        robot = None

        try:
            robot_cfg = self._cfg.robot
            dynamixel_cfg = self._cfg.agent.dynamixel_config

            joint_ids = [int(value) for value in dynamixel_cfg.joint_ids]
            joint_offsets = np.asarray(
                dynamixel_cfg.joint_offsets, dtype=np.float64
            )
            joint_signs = np.asarray(
                dynamixel_cfg.joint_signs, dtype=np.float64
            )
            if len(joint_ids) != 6:
                raise ValueError(
                    f"当前 UI 要求 6 个 Gello 主臂 ID，配置中有 {len(joint_ids)} 个"
                )
            if joint_offsets.shape != (6,) or joint_signs.shape != (6,):
                raise ValueError("joint_offsets 和 joint_signs 必须各有 6 个值")

            with self._state_lock:
                self._joint_offsets = joint_offsets.copy()
                self._joint_signs = joint_signs.copy()

            gello_ids = list(joint_ids)
            if self._read_gripper and 7 not in gello_ids:
                gello_ids.append(7)

            gello_port = str(self._cfg.agent.port)
            baudrate = int(
                dynamixel_cfg.get("baudrate", DEFAULT_BAUDRATE)
            )
            port = PortHandler(gello_port)
            packet = PacketHandler(2.0)
            reader = GroupSyncRead(
                port,
                packet,
                PRESENT_POSITION_ADDRESS,
                PRESENT_POSITION_LENGTH,
            )

            if not port.openPort():
                raise RuntimeError(f"无法打开 Gello 串口：{gello_port}")
            if not port.setBaudRate(baudrate):
                raise RuntimeError(f"无法设置 Gello 波特率：{baudrate}")
            for motor_id in gello_ids:
                if not reader.addParam(motor_id):
                    raise RuntimeError(f"无法读取 Dynamixel ID {motor_id}")

            robot = IIMTRobot(
                robot_ip=str(robot_cfg.get("robot_ip", "192.168.8.87")),
                robot_port=int(robot_cfg.get("robot_port", 29999)),
                servoj_acceleration=float(
                    robot_cfg.get("servoj_acceleration", 7.0)
                ),
                servoj_velocity=float(robot_cfg.get("servoj_velocity", 5.0)),
                servoj_period=float(robot_cfg.get("servoj_period", 0.004)),
                servoj_lookahead_time=float(
                    robot_cfg.get("servoj_lookahead_time", 0.0)
                ),
                servoj_gain=float(robot_cfg.get("servoj_gain", 0.0)),
                print_target=bool(robot_cfg.get("print_target", False)),
                print_target_interval=float(
                    robot_cfg.get("print_target_interval", 0.5)
                ),
            )

            control_hz = float(self._cfg.get("hz", 30))
            if not math.isfinite(control_hz) or control_hz <= 0:
                raise ValueError(f"hz 必须是正数，当前为 {control_hz}")
            control_period = 1.0 / control_hz

            self.ready.emit()
            next_tick = time.monotonic()
            last_ui_update = 0.0

            while not self._stop_requested.is_set():
                gello_raw_rad = read_raw_positions(reader, gello_ids)
                iimt_current_rad = robot.get_joint_state()
                with self._state_lock:
                    self._latest_gello_raw_rad = gello_raw_rad.copy()
                    self._latest_current_rad = iimt_current_rad.copy()
                    current_offsets = self._joint_offsets.copy()

                target_rad = (
                    gello_raw_rad[:6] - current_offsets
                ) * joint_signs

                # Check immediately before sending. Stop can be clicked while
                # the read calls above are in progress.
                if self._control_enabled.is_set():
                    robot.command_joint_state(target_rad)

                now = time.monotonic()
                if (
                    last_ui_update == 0.0
                    or now - last_ui_update >= DEFAULT_UI_UPDATE_PERIOD
                ):
                    self.data_updated.emit(
                        {
                            "current_rad": iimt_current_rad.copy(),
                            "gello_raw_rad": gello_raw_rad.copy(),
                            "target_rad": target_rad.copy(),
                            "control_enabled": self._control_enabled.is_set(),
                        }
                    )
                    last_ui_update = now

                next_tick += control_period
                delay = next_tick - time.monotonic()
                if delay > 0:
                    self._stop_requested.wait(delay)
                else:
                    # Reading/network latency exceeded one cycle. Do not
                    # accumulate stale sleep debt.
                    next_tick = time.monotonic()

        except Exception as exc:
            self._control_enabled.clear()
            self.error.emit(f"{type(exc).__name__}: {exc}")
        finally:
            self._control_enabled.clear()
            if robot is not None:
                robot.close()
            if reader is not None:
                reader.clearParam()
            if port is not None:
                port.closePort()


class MainWindow(QMainWindow):
    """Qt front end for the direct GELLO -> IIMT control path."""

    def __init__(
        self,
        cfg: DictConfig,
        config_path: str,
        read_gripper: bool = True,
    ) -> None:
        super().__init__()
        self._closing = False
        self._has_error = False
        self._config_path = config_path
        self._read_gripper = read_gripper

        self.setWindowTitle("GELLO → IIMT 关节监控与控制")
        self.resize(1250, 560)

        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)

        title = QLabel("GELLO / IIMT 关节数据")
        title.setStyleSheet("font-size: 20px; font-weight: bold;")
        main_layout.addWidget(title)

        self.status_label = QLabel(
            "正在连接 IIMT 和 Gello，只读监控尚未就绪……"
        )
        self.status_label.setStyleSheet("color: #555;")
        main_layout.addWidget(self.status_label)

        self.table = QTableWidget(7, 9)
        self.table.setHorizontalHeaderLabels(
            [
                "关节",
                "IIMT 当前 rad",
                "IIMT 当前 deg",
                "Gello 原始 rad",
                "Gello 原始 deg",
                "目标 rad",
                "目标 deg",
                "误差 rad",
                "误差 deg",
            ]
        )
        self.table.verticalHeader().setVisible(False)
        self.table.setEditTriggers(
            QAbstractItemView.EditTrigger.NoEditTriggers
        )
        self.table.setSelectionMode(
            QAbstractItemView.SelectionMode.NoSelection
        )
        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )
        self.table.setAlternatingRowColors(True)
        for row in range(7):
            self.table.setItem(row, 0, QTableWidgetItem(f"J{row + 1}"))
        self.table.item(6, 0).setText("J7 夹爪")
        main_layout.addWidget(self.table)

        info_box = QGroupBox("控制")
        info_layout = QGridLayout(info_box)
        info_layout.addWidget(
            QLabel(
                "打开界面只读取数据；点击启动后，按配置 hz 直接调用 API_Servoj。"
            ),
            0,
            0,
            1,
            2,
        )
        info_layout.addWidget(
            QLabel("配置文件："),
            1,
            0,
        )
        info_layout.addWidget(QLabel(config_path), 1, 1)

        self.start_button = QPushButton("启动控制")
        self.start_button.setEnabled(False)
        self.start_button.clicked.connect(self._start_control)
        info_layout.addWidget(self.start_button, 2, 0)

        self.stop_button = QPushButton("停止控制")
        self.stop_button.setEnabled(False)
        self.stop_button.clicked.connect(self._stop_control)
        info_layout.addWidget(self.stop_button, 2, 1)

        self.calibrate_button = QPushButton("标定当前姿态并保存 offset")
        self.calibrate_button.setEnabled(False)
        self.calibrate_button.clicked.connect(self._calibrate_current_pose)
        info_layout.addWidget(self.calibrate_button, 3, 0, 1, 2)
        info_layout.addWidget(
            QLabel(
                "标定前请让 IIMT 和 Gello 处于同一物理姿态；只更新 offset，不改 joint_signs。"
            ),
            4,
            0,
            1,
            2,
        )

        main_layout.addWidget(info_box)

        self.thread = ControlThread(
            cfg,
            config_path=config_path,
            read_gripper=read_gripper,
        )
        self.thread.ready.connect(self._on_ready)
        self.thread.data_updated.connect(self._update_table)
        self.thread.calibrated.connect(self._on_calibrated)
        self.thread.error.connect(self._on_error)
        self.thread.finished.connect(self._on_finished)
        self.thread.start()

    @staticmethod
    def _number(value: float, decimals: int) -> str:
        if not np.isfinite(value):
            return "NaN"
        return f"{value:.{decimals}f}"

    def _set_cell(self, row: int, column: int, text: str) -> None:
        item = self.table.item(row, column)
        if item is None:
            item = QTableWidgetItem()
            self.table.setItem(row, column, item)
        item.setText(text)
        item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

    def _update_table(self, data: object) -> None:
        payload = data
        current_rad = np.asarray(payload["current_rad"])
        gello_raw_rad = np.asarray(payload["gello_raw_rad"])
        target_rad = np.asarray(payload["target_rad"])
        error_rad = target_rad - current_rad

        for row in range(7):
            if row < 6:
                values = [
                    self._number(current_rad[row], 6),
                    self._number(np.rad2deg(current_rad[row]), 3),
                    self._number(gello_raw_rad[row], 6),
                    self._number(np.rad2deg(gello_raw_rad[row]), 3),
                    self._number(target_rad[row], 6),
                    self._number(np.rad2deg(target_rad[row]), 3),
                    self._number(error_rad[row], 6),
                    self._number(np.rad2deg(error_rad[row]), 3),
                ]
            elif len(gello_raw_rad) > 6:
                values = [
                    "—",
                    "—",
                    self._number(gello_raw_rad[6], 6),
                    self._number(np.rad2deg(gello_raw_rad[6]), 3),
                    "—",
                    "—",
                    "—",
                    "—",
                ]
            else:
                values = ["—"] * 8

            for column, value in enumerate(values, start=1):
                self._set_cell(row, column, value)

        if payload["control_enabled"]:
            self.status_label.setText(
                "控制中：正在直接发送 Gello 目标到 IIMT API_Servoj"
            )
            self.status_label.setStyleSheet("color: #b00020; font-weight: bold;")

    def _on_ready(self) -> None:
        self.start_button.setEnabled(True)
        self.calibrate_button.setEnabled(True)
        self.status_label.setText(
            "已连接。当前是只读监控；点击“启动控制”才会发送 API_Servoj。"
        )
        self.status_label.setStyleSheet("color: #176b2c;")

    def _start_control(self) -> None:
        if not self.thread.isRunning():
            return
        self.thread.enable_control()
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        self.calibrate_button.setEnabled(False)
        self.status_label.setText(
            "控制中：正在直接发送 Gello 目标到 IIMT API_Servoj"
        )
        self.status_label.setStyleSheet("color: #b00020; font-weight: bold;")

    def _stop_control(self) -> None:
        self.thread.disable_control()
        self.start_button.setEnabled(self.thread.isRunning())
        self.stop_button.setEnabled(False)
        self.calibrate_button.setEnabled(self.thread.isRunning())
        self.status_label.setText("已停止发送，仍在继续读取当前关节和目标数据。")
        self.status_label.setStyleSheet("color: #176b2c;")

    def _calibrate_current_pose(self) -> None:
        if not self.thread.isRunning():
            return

        self.thread.disable_control()
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(False)
        self.calibrate_button.setEnabled(False)

        answer = QMessageBox.question(
            self,
            "确认标定",
            "请确认 IIMT 和 Gello 当前处于同一物理姿态。\n"
            "标定只更新 joint_offsets，不发送 API_Servoj。\n\n"
            "是否继续？",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )
        if answer != QMessageBox.StandardButton.Yes:
            self.start_button.setEnabled(True)
            self.calibrate_button.setEnabled(True)
            self.status_label.setText("已取消标定，仍保持只读监控。")
            self.status_label.setStyleSheet("color: #176b2c;")
            return

        try:
            self.thread.calibrate_current_pose()
        except Exception as exc:
            self.start_button.setEnabled(True)
            self.calibrate_button.setEnabled(True)
            self.status_label.setText(
                f"标定失败：{type(exc).__name__}: {exc}"
            )
            self.status_label.setStyleSheet(
                "color: #b00020; font-weight: bold;"
            )

    def _on_calibrated(self, offsets: object) -> None:
        values = np.asarray(offsets, dtype=np.float64)
        formatted = ", ".join(f"{value:.6f}" for value in values)
        self.start_button.setEnabled(True)
        self.calibrate_button.setEnabled(True)
        self.status_label.setText(
            f"标定完成，offset 已保存；当前未发送控制。\n[{formatted}]"
        )
        self.status_label.setStyleSheet("color: #176b2c;")

    def _on_error(self, message: str) -> None:
        self._has_error = True
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(False)
        self.calibrate_button.setEnabled(False)
        self.status_label.setText(f"错误：{message}")
        self.status_label.setStyleSheet("color: #b00020; font-weight: bold;")

    def _on_finished(self) -> None:
        if self._closing:
            return
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(False)
        self.calibrate_button.setEnabled(False)
        if not self._has_error:
            self.status_label.setText("硬件线程已停止。")
            self.status_label.setStyleSheet("color: #555;")

    def closeEvent(self, event) -> None:  # noqa: N802 - Qt API name
        self._closing = True
        self.thread.request_stop()
        if not self.thread.wait(5000):
            self.status_label.setText(
                "硬件线程仍在退出，请确认 API 调用已经返回。"
            )
        event.accept()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", default="configs/iimt.yaml")
    parser.add_argument(
        "--no-gripper",
        action="store_true",
        help="不读取/显示 Dynamixel ID7",
    )
    args = parser.parse_args()

    cfg = OmegaConf.load(args.config)
    app = QApplication(sys.argv)
    window = MainWindow(
        cfg,
        config_path=args.config,
        read_gripper=not args.no_gripper,
    )
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
