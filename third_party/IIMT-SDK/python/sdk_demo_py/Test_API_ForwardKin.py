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
        print("尝试获取运动学正解值...")
        joint_rad = JointRad()
        joint_rad.robotRad = (ctypes.c_double * 6)(0.00001,-1.57074,0.29524,-1.57074,-1.57073,0.00000)
        result,tcp_pose = API_ForwardKin(handle,joint_rad)
        if result:
            print(f"获取成功，得到返回值为：\n{[tcp_pose.robotTcp[i] for i in range(6)]}\n")    
        else:
            print(f"获取正解失败")
