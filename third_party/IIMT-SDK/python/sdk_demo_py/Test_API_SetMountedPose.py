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
    mounted_pose = MountedPose.INVERTED_MOUNTED
    print("尝试设置安装姿态...")
    result = API_SetMountedPose(handle,mounted_pose)
    if result:
        print(f"设置安装姿态成功{mounted_pose}")
    else:
        print("设置安装姿态成功失败！")
