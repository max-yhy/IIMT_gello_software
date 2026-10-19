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
    print("尝试末端TCP方向标定...")
    points = b"0.049,-1.461,1.063,-1.220,-1.571,0.006;0.056,-1.631,1.237,-1.224,-1.571,0.013;0.056,-1.551,0.980,-1.047,-1.571,0.013"
    result = API_TcpDirectionCalibration(handle,points)
    if result:
        print("Tcp方向标定成功！")
    else:
        print("Tcp方向标定失败！")
    
