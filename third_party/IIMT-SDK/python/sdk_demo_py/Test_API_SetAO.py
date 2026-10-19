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
    
    print("尝试设置AO状态...")
    ao_num=3
    value=5.3
    result = API_SetAO(handle,ao_num,value)
    if result:        
        print(f"AO{ao_num}状态设置成功")
    else:
        print("AO{ao_num}状态设置失败")
    
