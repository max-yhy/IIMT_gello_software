from iimt_api import *

print("尝试登录...")
login_result,handle = API_Login()
print(f"登录后的句柄值: {handle.value}")
print(f"API_Login 返回值: {login_result}")
if login_result:
    print("登录成功")
else:
    print("登录失败")
if login_result:
    print("尝试获取关节达位状态...")
    joint_rad = JointRad()
    joint_rad.robotRad = (ctypes.c_double * 6)(-0.027,-0.027,-0.35,-0.027,-0.027,-0.027)
    result,arrive_status = API_GetJointArriveStatus(handle,joint_rad)
    if result:
        print("获取关节达位状态成功！")
        # 解析状态
        if arrive_status.value == ArriveStatus.ARRIVE_STATUS_ARRIVED:
            print("关节已达位")
        elif arrive_status.value == ArriveStatus.ARRIVE_STATUS_NOT_ARRIVED:
            print("关节未达位")
        elif arrive_status.value == ArriveStatus.ARRIVE_STATUS_ERROR:
            print("关节达位出错")
        else:
            print(f"未知状态码：{status.value}")
        # 输出关节弧度值（如果有返回）
        print(f"关节弧度值：{joint_rad.robotRad[:]}")
    else:
        print("获取关节达位状态失败！")
