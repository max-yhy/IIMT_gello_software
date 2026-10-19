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
        print("尝试执行lua脚本文件...")
        remote_absolute_path_file_name = r"/home/iimt/lua_file1/test2.lua"
        result = API_ExecuteFile(handle,remote_absolute_path_file_name.encode('utf-8'))
        if result:
            print("执行成功！")
        else:
            print("执行失败！")
