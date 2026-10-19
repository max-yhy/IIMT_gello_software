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
    print("尝试获取DI状态...")
    di_num = 1
    result,di_status = API_GetDI(handle,di_num)
    if result:        
        if di_status.value == IoStatus.IO_STATUS_LOW:
            print(f"DI{di_num}状态为低电平")
        elif di_status.value == IoStatus.IO_STATUS_HIGH:
            print(f"DI{di_num}状态为高电平")            
    else:
        print("获取DI状态失败")
    
