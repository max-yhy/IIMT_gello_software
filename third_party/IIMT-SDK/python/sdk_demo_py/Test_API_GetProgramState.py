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
    print("尝试查询程序状态...")
    run_result,program_state = API_GetProgramState(handle)
    if run_result:
        print(f"程序状态:{program_state.description}")               
    else:
        print("检查程序程序状态失败！")
    
