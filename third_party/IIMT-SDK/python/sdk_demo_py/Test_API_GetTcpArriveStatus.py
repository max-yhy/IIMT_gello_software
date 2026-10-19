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
    print("尝试获取TCP达位状态...")
    tcp_position = TcpPosition()
    tcp_position.robotTcp = (ctypes.c_double * 6)(-0.78709,-0.12355,0.04737,-2.20212,-1.48857,0.63530)
    result,arrive_status = API_GetTcpArriveStatus(handle,tcp_position)
    if result:
        print("获取TCP达位状态成功！")
        # 解析状态
        if arrive_status.value == ArriveStatus.ARRIVE_STATUS_ARRIVED:
            print("TCP已达位")
        elif arrive_status.value == ArriveStatus.ARRIVE_STATUS_NOT_ARRIVED:
            print("TCP未达位")
        elif arrive_status.value == ArriveStatus.ARRIVE_STATUS_ERROR:
            print("TCP达位出错")
        else:
            print(f"未知状态码：{status.value}")
        # 输出关节弧度值（如果有返回）
        print(f"TCP值：{tcp_position.robotTcp[:]}")
    else:
        print("获取TCP达位状态失败！")
