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
    print("尝试获取下电延迟时间...")
    result,delay_time = API_GetPowerOffDelayTime(handle)
    if result:
        print(f"下电延迟时间为{delay_time.value}(ms)")
    else:
        print("获取下电延迟时间失败")
    
