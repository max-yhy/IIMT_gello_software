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
    print("尝试获取机器人状态...")
    result,robot_status = API_GetRobotStatus(handle)
    if result:
        print(f"获取成功，获取值为：{robot_status.value}")        
    else:
        print("获取失败")
    
