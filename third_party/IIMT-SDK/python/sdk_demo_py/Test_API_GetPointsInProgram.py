 

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
    print("尝试获取程序中路点信息...")
    program_file_name=b"unkn"
    result,points_info = API_GetPointsInProgram(handle,program_file_name)
    if result:
        print(f"获取程序中路点信息成功:{points_info.description}")
    else:
        print("获取程序中路点信息失败！")
    
