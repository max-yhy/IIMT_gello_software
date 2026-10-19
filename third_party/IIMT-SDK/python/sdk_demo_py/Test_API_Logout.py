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
    print(f"注销前，句柄值: {handle.value}")
    logout_result = API_Logout(handle)
    if logout_result:
        print(f"API_Logout 返回值: {logout_result}")
        print("连接已关闭")
    else:
        print("注销失败")        
               
          
