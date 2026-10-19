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
    print("尝试末端TCP位置标定...")
    points = b"0.030,-1.644,1.818,-2.262,-1.239,0.036;0.132,-1.578,1.756,-2.240,-2.031,-0.218;0.160,-1.409,1.317,-1.137,-2.192,-0.084;0.051,-1.272,1.048,-0.683,-1.630,-0.360"
    result = API_TcpPositionCalibration(handle,points)
    if result:
        print("Tcp位置标定成功！")
    else:
        print("Tcp位置标定失败！")
    
