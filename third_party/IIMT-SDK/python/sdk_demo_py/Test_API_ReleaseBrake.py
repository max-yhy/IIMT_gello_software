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
    print("尝试使能...")
    release_brake_result = API_ReleaseBrake(handle)
    print(f"API_ReleaseBrake 返回值：{release_brake_result}")
    if release_brake_result:
        print("使能成功")
    else:
        print("使能失败")       
