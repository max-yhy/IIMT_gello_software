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
    print("尝试停止...")
    stop_result = API_Stop(handle)
    print(f"API_Stop 返回值：{stop_result}")
    if stop_result:
        print("停止成功")
    else:
        print("停止失败")            
          
