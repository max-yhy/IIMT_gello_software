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
	print("尝试急停...")
	emergency_stop_result = API_EmergencyStop(handle)
	print(f"API_EmergencyStop 返回值: {emergency_stop_result}")
	if emergency_stop_result:
		print("急停成功")
	else:
		print("急停失败")       
        
       
          
