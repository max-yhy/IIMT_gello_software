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
    print("尝试启动...")
    play_result = API_Play(handle)
    print(f"API_Play 返回值：{play_result}")
    if play_result:
        print("启动成功")
    else:
        print("启动失败")           
          
