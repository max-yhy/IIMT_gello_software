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
        print("开始尝试手动示教...")
        # 对每个关节进行手动示教操作
        result = API_ManualTeachStart(handle, 2, 1)
        if (result):
        	print("开始尝试结束手动示教...")
        	API_ManualTeachEnd(handle, 2, 1)
