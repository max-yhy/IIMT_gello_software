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
        tcp_pose = TcpPosition()
        tcp_pose.robotTcp = (ctypes.c_double * 6)(-0.14753,-0.11901,0.69581,-1.75866,0.00001,1.57087)
        ref_joint_rad = JointRad()
        ref_joint_rad.robotRad = (ctypes.c_double * 6)(0.00000,-1.57072,0.54639,-1.57072,-1.57072,0.00000)
        print("尝试获取运动学逆解值...")
        result,joint_rad = API_InverseKin(handle,tcp_pose,ref_joint_rad)
        if result:
            print(f"获取成功，得到返回值为：\n{[joint_rad.robotRad[i] for i in range(6)]}\n")
        else:
            print(f"获取逆解失败")
        


