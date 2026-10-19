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
    print("尝试远程执行脚本...")
    script_content = b"setAO(2,8.5)"
    result = API_ExecuteScript(handle,script_content)
    if result:
        print(f"远程执行成功")
    else:
        print("远程执行失败")
    
