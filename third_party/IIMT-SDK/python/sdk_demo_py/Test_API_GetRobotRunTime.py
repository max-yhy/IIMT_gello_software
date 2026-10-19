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
    print("尝试获取运行时间...")
    result,run_time = API_GetRobotRunTime(handle)
    if result:
        print(f"运行时间为{run_time.value}(s)")
    else:
        print("获取运行时间失败")
    
