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
    print("开始尝试获取机器人关节位置角度")
    result,joint_Angle = API_GetRobotJointAngle(handle)
    if result:
        print(f"机器人关节角度: {[joint_Angle.robotAngle[i] for i in range(6)]}")
    else:
        print("获取角度失败")
