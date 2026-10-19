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
    print("尝试movej运动") 
    movej = MovejParam()
    movej.q = (ctypes.c_double * 6)(0,-1.57,0,-1.57,-1.57,0)
    movej.v = ctypes.c_float(100)
    movej.a = ctypes.c_float(100)     
    movej.j = ctypes.c_float(100)
    movej.r = ctypes.c_float(0)         
    movej_result = API_Movej(handle,movej,True,30)
    if movej_result:
        print("movej指令成功")
    else:
        print("movej指令失败")
    
