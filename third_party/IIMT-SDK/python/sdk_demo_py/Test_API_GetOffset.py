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
    print("尝试获取轨迹偏移量...")
    result,offset = API_GetOffset(handle)
    if result:
        print(f"获取的偏移量为：\n{offset.x_offset}\n{offset.y_offset}\n{offset.z_offset}\n{offset.rx_offset}\n{offset.ry_offset}\n{offset.rz_offset}\n")
    else:
        print("获取偏移量失败")
    
