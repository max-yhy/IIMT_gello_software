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
    print("尝试设置轨迹偏移量...")
    offset = TrajectoryOffset()
    offset.x_offset = 1.22
    offset.y_offset = 2.564
    offset.z_offset = 3.2
    offset.rx_offset = 4.8
    offset.ry_offset = 5.9
    offset.rz_offset = 1.02   
    result = sdk.API_SetOffset(handle,offset) 
    if result:
        print(f"设置轨迹偏移量成功")          
    else:
        print("设置轨迹偏移量失败")
