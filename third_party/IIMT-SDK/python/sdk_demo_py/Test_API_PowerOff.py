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
    print("尝试下电...")
    power_off_result = API_PowerOff(handle)
    print(f"API_PowerOff 返回值：{power_off_result}")
    if power_off_result:
        print("下电成功")
    else:
        print("下电失败")           
          
