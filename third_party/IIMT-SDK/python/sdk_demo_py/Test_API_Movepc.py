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
    print("尝试movepc运动") 
    movepc = MovepcParam()
    movepc.passing_point = (ctypes.c_double * 6)(-0.60331,-0.06536,0.42140,3.136,0,1.566)
    movepc.end_point = (ctypes.c_double * 6)(-0.38628,-0.1701,0.42127,3.136,0,1.566)
    movepc.tool_v = ctypes.c_float(600)     
    movepc.tool_a = ctypes.c_float(1000)
    movepc.circle = 0
    movepc.count = 1
    movepc.r = 25
    movepc.mode = 0       
    result = API_Movepc(handle,movepc,False,0)
    if result:
        print("执行圆形轨迹成功")
    else:
        print("执行圆形轨迹失败")

    
