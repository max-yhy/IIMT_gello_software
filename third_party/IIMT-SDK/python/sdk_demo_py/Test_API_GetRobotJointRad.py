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
    print("开始尝试获取机器人关节位置弧度")
    result,joint_rad = API_GetRobotJointRad(handle)
    if result:
        print(f"机器人关节弧度: {[joint_rad.robotRad[i] for i in range(6)]}")
    else:
        print("获取弧度失败")

    
