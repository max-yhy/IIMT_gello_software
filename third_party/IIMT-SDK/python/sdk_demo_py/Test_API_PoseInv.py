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
    print("尝试计算位姿的逆...")
    p_from = TcpPosition()
    p_from.robotTcp = (ctypes.c_double * 6)(-0.38710,-0.14182,0.91375,-0.04443,0.82116,-0.06083)
    result,result_pose = API_PoseInv(handle,p_from)
    if result:
        print(f"逆变换结果: {result_pose.robotTcp[:]}")
    else:
        print("位姿求逆失败！")
