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
    print("开始尝试获取机器人型号...")
    result,robot_model = API_GetRobotModel(handle)
    if result:
        print(f"获取机器人型号成功:{robot_model.description}")
    else:
        print("获取机器人型号失败")
    
