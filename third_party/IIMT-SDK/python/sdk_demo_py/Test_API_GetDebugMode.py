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
	print("开始尝试设置调试模式...")
	is_setdebug = True
	is_debug_result = API_SetDebugMode(handle,is_setdebug)
	if is_debug_result:
		print(f"设置调试模式成功，返回值：{is_debug_result}")
	else:
		print("设置调试模式失败")   	 
	print("开始尝试获取调试模式...")
	isdebug_result,is_debug = API_GetDebugMode(handle)
	if isdebug_result:
		if is_debug.value == True: 
		    print(f"当前处于调试模式下，调试值：{is_debug.value}")
		elif is_debug.value == False:
		    print(f"当前未处于调试模式，调试值：{is_debug.value}")            
	else:
		print("获取调试模式失败")       
             
          
