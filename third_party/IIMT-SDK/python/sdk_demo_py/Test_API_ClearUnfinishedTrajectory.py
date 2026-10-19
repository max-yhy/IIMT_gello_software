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
	print("清除未完成的轨迹...")
	clear_unfinished_trajectory_result = API_ClearUnfinishedTrajectory(handle)
	print(f"API_ClearUnfinishedTrajectory 返回值: {clear_unfinished_trajectory_result}")
	if clear_unfinished_trajectory_result:
		print("清除未完成的轨迹成功")
	else:
		print("清除未完成的轨迹失败")       
        
       
          
