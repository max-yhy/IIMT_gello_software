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
    print("尝试查询运行状态...")
    run_result,program_running = API_Running(handle)
    if run_result:
        print(f"运行状态:{program_running.description}")               
    else:
        print("检查程序运行状态失败！")
    
