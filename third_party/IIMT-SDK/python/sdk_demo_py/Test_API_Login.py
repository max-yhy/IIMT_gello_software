from iimt_api import *


print("尝试登录...")
login_result,handle = API_Login()
print(f"登录后的句柄值: {handle.value}")
if login_result:
	print("登录成功")
else:
	print("登录失败")
    