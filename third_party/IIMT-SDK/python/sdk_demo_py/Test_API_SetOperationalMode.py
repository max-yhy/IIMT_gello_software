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
	#operational_mode=b"manual"
    operational_mode=b"automatic"
    print("尝试设置机器人操作模式...")
    set_operational_result = sdk.API_SetOperationalMode(handle,operational_mode)
    if set_operational_result:
        print(f"设置操作模式成功")
    else:
    	print("设置操作模式失败！")
