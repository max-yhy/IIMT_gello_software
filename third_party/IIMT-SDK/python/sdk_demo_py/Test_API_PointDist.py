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
    print("尝试获取两点之间距离...")
    p_from = TcpPosition()
    p_from.robotTcp = (ctypes.c_double * 6)(-0.38710,-0.14182,0.91375,-0.04443,0.82116,-0.06083);
    p_to = TcpPosition()
    p_to.robotTcp = (ctypes.c_double * 6)(-0.47635,-0.14182,0.81555,-0.02574,0.55751,-0.04884);
    result,distance = API_PointDist(handle,p_from, p_to)
    if result:
        print(f"距离为: {distance.value:.4f} 米")  # 保留4位小数
    else:
        print("获取两点距离失败！")
