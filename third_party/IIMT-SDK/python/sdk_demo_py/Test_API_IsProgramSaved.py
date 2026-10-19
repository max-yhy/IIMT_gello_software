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
    print("尝试查询程序保存状态...")
    result,program_saved = API_IsProgramSaved(handle)
    if result:
        print(f"程序保存状态:{program_saved.description}")               
    else:
        print("检查程序保存状态失败!")
    
