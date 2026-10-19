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
	print("尝试上电...")
	power_on_result = API_PowerOn(handle)
	print(f"API_PowerOn 返回值: {power_on_result}")
	if power_on_result:
		print("上电成功")
	else:
		print("上电失败")       
        
       
          
