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
	print("开始尝试获取被加载程序...")
	load_program_name = b"unknown"
	load_program_result = API_LoadProgram(handle,load_program_name)
	if load_program_result:
		print(f"获取被加载程序成功:返回值：{load_program_result}")
	else:
		print("获取被加载程序失败！")
	print("获取错误信息描述...")
	get_error_info_result,error_info = API_GetErrorInfo(handle)
	if get_error_info_result:
		print(f"获取错误信息描述成功，返回值:{get_error_info_result}\n错误信息:{error_info.description}")
	else:
		print(f"获取失败")       
          
