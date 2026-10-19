from iimt_api import *
import time
print("尝试登录...")
login_result,handle = API_Login()
print(f"登录后的句柄值: {handle.value}")
print(f"API_Login 返回值: {login_result}")
if login_result:
    print("登录成功")
else:
    print("登录失败")
if login_result:
    
    print("尝试设置安装角度...")
    tiltAngle=45.0
    baseRotationAngle=0.0
    result = API_SetMountedAngle(handle,tiltAngle,baseRotationAngle)
    if result:        
        print(f"tiltAngle:{tiltAngle},baseRotationAngle:{baseRotationAngle}设置成功")
    else:
        print("tiltAngle:{tiltAngle},baseRotationAngle:{baseRotationAngle}设置失败")
