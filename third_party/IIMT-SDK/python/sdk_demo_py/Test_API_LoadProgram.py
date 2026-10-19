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
        print("尝试加载程序...")
        program_file_name=b"test"
        load_program_result = API_LoadProgram(handle, program_file_name)
        print(f"API_LoadProgram 返回值：{load_program_result}")
        if load_program_result:
            print("加载程序成功...")
        else:
            print("加载程序失败...")

