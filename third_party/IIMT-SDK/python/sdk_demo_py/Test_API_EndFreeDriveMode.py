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
    print("尝试停止自由拖动...")
    result = API_EndFreeDriveMode(handle)
    if result:
        print("自用拖动停止动成功")
    else:
        print("自由拖动停止失败")
    
