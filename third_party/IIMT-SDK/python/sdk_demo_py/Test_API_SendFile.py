import os
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
	local_absolute_path_file_name = r"/home/iimt/lua_file/test1.lua"
    #local_absolute_path_file_name = r"F:\lua_file\test1.lua"
	save_path = r"/home/iimt/lua_file1/"
	save_file_name = r"test2.lua"
    # 验证本地文件路径是否存在
	if not os.path.isfile(local_absolute_path_file_name):
		print(f"本地文件 {local_absolute_path_file_name} 不存在")
		exit(1)
	print("尝试远程传输文件...")
	result = API_SendFile(handle, local_absolute_path_file_name.encode('utf-8'),save_path.encode('utf-8'),save_file_name.encode('utf-8'))
	if result:
		print(f"传输成功")
	else:
		print("传输失败")
