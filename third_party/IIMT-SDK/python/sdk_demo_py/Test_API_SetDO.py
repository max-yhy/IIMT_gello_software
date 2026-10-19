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
    print("尝试设置DO状态...")
    do_num = 1
    do_status = IoStatus.IO_STATUS_HIGH
    result = API_SetDO(handle,do_num,do_status)
    if result:        
        print(f"DO{do_num}状态设置成功")
    else:
        print("DO{do_num}状态设置失败")
