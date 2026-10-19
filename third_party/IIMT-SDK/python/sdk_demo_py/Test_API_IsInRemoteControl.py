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
    print("尝试获取远程状态...")
    result,is_in_remote_control = API_IsInRemoteControl(handle)
    if result:
        result_str = is_in_remote_control.description.decode('utf-8').rstrip('\x00')
        if result_str == "false":
            print("当前不为远程状态...")
        elif result_str == "true":
            print("当前为远程状态...")
        else:
            print(f"获取远程状态值异常，当前获取值：{result_str}")    
    else:
        print("获取远程状态失败!")
    
