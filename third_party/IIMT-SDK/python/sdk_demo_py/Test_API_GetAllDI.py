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
    print("尝试获取所有数字输入口状态...")
    result,all_di_status = API_GetAllDI(handle)
    if result:
        print(f"获取成功，{[all_di_status.IoInfo[i].value for i in range(16)]}\n")
    else:
        print("获取失败")
