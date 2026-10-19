from iimt_api import *
import numpy as np
import ctypes
import time

# -----------------------------------------------------------------------------
# 纯 numpy 实现四元数 SLERP（不依赖 scipy！）
# -----------------------------------------------------------------------------
def quat_slerp(q1, q2, t):
    """
    四元数球面线性插值
    q1, q2: [w, x, y, z]
    t: 0~1
    返回: 插值后的四元数 [w,x,y,z]
    """
    dot = np.dot(q1, q2)

    # 防止角度翻转
    if dot < 0.0:
        q1 = -q1
        dot = -dot

    # 接近重合直接线性插值
    if dot > 0.9995:
        q = q1 + t * (q2 - q1)
        return q / np.linalg.norm(q)

    # 标准 SLERP
    theta_0 = np.arccos(dot)
    theta = theta_0 * t
    sin_theta = np.sin(theta)
    sin_theta_0 = np.sin(theta_0)

    s0 = np.cos(theta) - dot * sin_theta / sin_theta_0
    s1 = sin_theta / sin_theta_0

    return s0 * q1 + s1 * q2

# -----------------------------------------------------------------------------
# 旋转向量 ↔ 四元数 互转（纯 numpy）
# -----------------------------------------------------------------------------
def rotvec_to_quat(rotvec):
    """旋转向量 [rx, ry, rz] → 四元数 [w, x, y, z]"""
    angle = np.linalg.norm(rotvec)
    if angle < 1e-6:
        return np.array([1.0, 0.0, 0.0, 0.0])
    axis = rotvec / angle
    s = np.sin(angle * 0.5)
    w = np.cos(angle * 0.5)
    x = axis[0] * s
    y = axis[1] * s
    z = axis[2] * s
    return np.array([w, x, y, z])

def quat_to_rotvec(quat):
    """四元数 [w,x,y,z] → 旋转向量 [rx, ry, rz]"""
    w, x, y, z = quat
    angle = 2 * np.arccos(np.clip(w, -1.0, 1.0))
    if angle < 1e-6:
        return np.zeros(3)
    axis = np.array([x, y, z]) / np.sin(angle * 0.5)
    return axis * angle

# -----------------------------------------------------------------------------
# 笛卡尔直线插补（无 scipy 版）
# -----------------------------------------------------------------------------
def cartesian_linear_interp(p_start, p_end, step_num):
    """
    笛卡尔空间直线插补（位置LERP + 姿态SLERP）
    输入：[x,y,z,rx,ry,rz]
    输出：轨迹 [[x,y,z,rx,ry,rz], ...]
    """
    if len(p_start) != 6 or len(p_end) != 6 or step_num <= 0:
        return []

    # 位置
    pos_start = np.array(p_start[:3])
    pos_end = np.array(p_end[:3])

    # 旋转
    rot_start = np.array(p_start[3:])
    rot_end = np.array(p_end[3:])

    # 转四元数
    q_start = rotvec_to_quat(rot_start)
    q_end = rotvec_to_quat(rot_end)

    traj = []
    for i in range(step_num + 1):
        t = i / step_num

        # 位置插值
        pos = (1 - t) * pos_start + t * pos_end

        # 姿态插值（SLERP）
        q = quat_slerp(q_start, q_end, t)
        rot = quat_to_rotvec(q)

        point = np.concatenate([pos, rot]).tolist()
        traj.append(point)

    return traj

# -----------------------------------------------------------------------------
# 主程序（完全不变）
# -----------------------------------------------------------------------------
print("尝试登录...")
login_result, handle = API_Login()
print(f"登录后的句柄值: {handle.value}")
print(f"API_Login 返回值: {login_result}")

if login_result:
    print("登录成功")
else:
    print("登录失败")
    exit()

print("开始尝试获取机器人TCP位置")
result, tcp_position = API_GetRobotTcpPosition(handle)
if not result:
    print("获取TCP位置失败")
    exit()

print(f"机器人TCP位置: {[tcp_position.robotTcp[i] for i in range(6)]}")

current_tcp_pose = tcp_position.robotTcp[:6]
target_tcp_pose = [-0.42713, -0.14303, 0.68271, -2.03987, 0.00012, 1.57103]

# 轨迹插值（无 scipy）
traj_points = cartesian_linear_interp(current_tcp_pose, target_tcp_pose, 100)

# 发送 servoc
for i, point in enumerate(traj_points):
    print("尝试servoc运动")
    servoc = ServocParam()
    for j in range(6):
        servoc.p[j] = ctypes.c_double(point[j])

    servoc.a = ctypes.c_float(7)
    servoc.v = ctypes.c_float(5)
    servoc.t = ctypes.c_float(0.008)
    servoc.lookahead_time = ctypes.c_float(0.0)

    servoc_result = API_Servoc(handle, servoc)
    time.sleep(0.008)

    if servoc_result:
        print(f"第{i}点 servoc 指令成功")
    else:
        print(f"第{i}点 servoc 指令失败")
