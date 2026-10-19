from iimt_api import *
from iimt_tcp_socket import *
from crnt_laser_control import *
import math
import ast

def dynamic_finding(handle,sock):
    last_tcp_position = TcpPosition()
    weld_point = [0,0,0,0,0,0]
    while True:
        result,tcp_position = API_GetRobotTcpPosition(handle)
        if result:
            print(f"机器人TCP位置: {[tcp_position.robotTcp[i] for i in range(6)]}")
            if last_tcp_position == tcp_position:
                break
            for i in range(6):
                last_tcp_position.robotTcp[i] = tcp_position.robotTcp[i]
            send_msg = get_robot_send_msg(tcp_position.robotTcp)
            tcp_send(sock,send_msg)
            recv_data = tcp_recv(sock)
            recv_msg = recv_data.decode("utf-8")
            print(f"send pose响应1：{recv_msg}")
            point = get_seam_point(recv_data,tcp_position.robotTcp)
            if point is not None:
                weld_point = point
                break	
        else:
            print("获取TCP位置失败")
            break
    return weld_point	
	
print("尝试登录...")
login_result,handle = API_Login()
print(f"登录后的句柄值: {handle.value}")
print(f"API_Login 返回值: {login_result}")
if login_result:
    print("登录成功")
else:
    print("登录失败")
if login_result: 
    print("尝试movel运动") 
    movel = MovelParam()
    movel.p = (ctypes.c_double * 6)(-0.62700,-0.11989,0.28962,2.993,0.115,2.040)
    movel.v = ctypes.c_float(100)
    movel.tool_v = ctypes.c_float(1000)     
    movel.tool_a = ctypes.c_float(1000)
    movel.r = ctypes.c_float(0)         
    result = API_Movel(handle,movel,True,60)
    if result:
        print("movel指令1成功")
    else:
        print("movel指令1失败")
        exit(1)
    sock = login_laser()
    if sock is not None:
    	open_laser(sock)
    else:
    	print("无法建立连接，退出")
    	exit(1)
    movel.p = (ctypes.c_double * 6)(-0.62701,-0.07924,0.28960,2.993,0.115,2.040)
    result = API_Movel(handle,movel,False,0)
    weld_point_1 = dynamic_finding(handle,sock)
    
    close_laser(sock)		
    movel.p = (ctypes.c_double * 6)(-0.62705,-0.42800,0.28963,2.993,0.115,2.040)        
    result = API_Movel(handle,movel,True,60)
    if result:
        print("movel指令2成功")
    else:
        print("movel指令2失败")	
        exit(1)
    open_laser(sock)
    movel.p = (ctypes.c_double * 6)(-0.62709,-0.54556,0.28960,2.993,0.115,2.040)
    result = API_Movel(handle,movel,False,0)
    weld_point_2 = dynamic_finding(handle,sock)
    close_laser(sock)	
    logout_laser(sock)		
    print(f"开始焊接点: {[weld_point_1[i] for i in range(6)]}")
    print(f"结束焊接点: {[weld_point_2[i] for i in range(6)]}")
    movel.p = (ctypes.c_double * 6)(weld_point_1[0],weld_point_1[1],weld_point_1[2],weld_point_1[3],weld_point_1[4],weld_point_1[5])
    result = API_Movel(handle,movel,True,120)
    movel.p = (ctypes.c_double * 6)(weld_point_2[0],weld_point_2[1],weld_point_2[2],weld_point_2[3],weld_point_2[4],weld_point_2[5])
    result = API_Movel(handle,movel,True,120)
	# deg = 180
	# rad = math.radians(deg)
	# print(rad)  # 输出: 3.141592653589793 (即 π)
