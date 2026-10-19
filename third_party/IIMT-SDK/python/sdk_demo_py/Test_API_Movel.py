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
    print("尝试movel运动") 
    movel = MovelParam()
    movel.p = (ctypes.c_double * 6)(-0.53910,-0.14182,0.79482,-0.00962,0.22851,-0.04254)
    movel.v = ctypes.c_float(100)
    movel.tool_v = ctypes.c_float(1000)     
    movel.tool_a = ctypes.c_float(1000)
    movel.r = ctypes.c_float(0)         
    result = API_Movel(handle,movel,True,30)
    if result:
        print("movel指令成功")
    else:
        print("movel指令失败")
    
