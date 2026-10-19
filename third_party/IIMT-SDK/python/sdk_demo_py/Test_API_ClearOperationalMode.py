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
    print("尝试清除操作模式...")
    clear_operational_result = API_ClearOperationalMode(handle)
    if clear_operational_result:
        print(f"清除成功！返回值：{clear_operational_result}")
    else:
        print("清除失败！")
    
