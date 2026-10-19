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
    print("尝试获取机器人操作模式...")
    result,operational_mode = API_GetOperationalMode(handle)
    if result:
        print(f"获取机器人操作模式成功:{operational_mode.description}")
    else:
        print("获取机器人操作模式失败")
    
