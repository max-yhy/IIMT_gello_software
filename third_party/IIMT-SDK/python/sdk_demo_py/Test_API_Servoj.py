from iimt_api import *
import time

def joint_linear_interp(q_start, q_end, step_num):
    """
    关节空间线性插值
    :param q_start: 起始关节角度列表 [q1, q2, q3, ...]
    :param q_end: 目标关节角度列表 [q1, q2, q3, ...]
    :param step_num: 插值总步数
    :return: 轨迹列表 traj，格式：[[q0],[q1],...,[step_num]]
    """
    traj = []
    dof = 6
    #dof = len(q_start)  # 关节自由度

    for i in range(step_num + 1):
        t = i / step_num  # 归一化时间 0~1
        q = []
        for j in range(dof):
            # 单关节线性插值公式
            q_val = q_start[j] * (1 - t) + q_end[j] * t
            q.append(q_val)
        traj.append(q)

    return traj
print("尝试登录...")
login_result,handle = API_Login()
print(f"登录后的句柄值: {handle.value}")
print(f"API_Login 返回值: {login_result}")
if login_result:
    print("登录成功")
else:
    print("登录失败")
if login_result: 
	print("开始尝试获取机器人当前关节位置弧度")
	result,joint_rad = API_GetRobotJointRad(handle)
	if result:
		print(f"机器人关节弧度: {[joint_rad.robotRad[i] for i in range(6)]}")
	else:
		print("获取弧度失败")
		exit()		
	current_joint_rad = (ctypes.c_double * 6)(*joint_rad.robotRad[:6])
	target_joint_rad = (ctypes.c_double * 6)(0.00000,-1.31072,0.0,-1.57072,-1.57072,0.00000)
	traj_points = joint_linear_interp(current_joint_rad,target_joint_rad,600)
	for i in range(len(traj_points)):
		point = traj_points[i]
		print("尝试servoj运动")  
		servoj = ServojParam()
		joints = point[:6]  # 取前6个
		for i in range(6):
			servoj.q[i] = joints[i]
		servoj.a = ctypes.c_float(7)
		servoj.v = ctypes.c_float(5)     
		servoj.t = ctypes.c_float(0.008)
		servoj.lookahead_time = ctypes.c_float(0.0)  #0.08
		servoj.gain = ctypes.c_float(0)       
		servoj_result = API_Servoj(handle,servoj)
		time.sleep(0.008)
		if servoj_result:
			print("servoj指令成功")
		else:
			print("servoj指令失败")
    
