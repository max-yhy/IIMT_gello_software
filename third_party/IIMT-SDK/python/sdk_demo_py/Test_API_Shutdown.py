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
    print("尝试关闭控制器...")
    result = API_Shutdown(handle)
    if result:
        print("关闭控制器成功")
    else:
        print("关闭控制器失败")
    
