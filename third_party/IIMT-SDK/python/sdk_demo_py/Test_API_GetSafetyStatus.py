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
    print("开始尝试获取安全状态...")
    result,safety_status = API_GetSafetyStatus(handle)
    if result:
        print(f"获取安全状态成功:{safety_status.description}")
    else:
        print("获取安全状态失败！")
    
