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
	print("机器人错误复位...")
	reset_robot_error_result = API_ResetRobotError(handle)
	print(f"API_ResetRobotError 返回值: {reset_robot_error_result}")
	if reset_robot_error_result:
		print("机器人错误复位成功")
	else:
		print("机器人错误复位失败")       
        
       
          
