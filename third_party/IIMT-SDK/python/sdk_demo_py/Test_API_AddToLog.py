from iimt_api import *

log_text = b"It's so hot!Help me,human."


print("尝试登录...")
login_result,handle = API_Login()
print(f"登录后的句柄值: {handle.value}")
print(f"API_Login 返回值: {login_result}")
if login_result:
    print("登录成功")
else:
    print("登录失败")
if login_result:
	print("开始尝试添加消息到日志...")
	addlog_result = API_AddToLog(handle,log_text)    
	print(f"API_AddToLog 返回值： {addlog_result}")
	if addlog_result:
		print("添加成功")
	else:
		print("添加失败")

    
