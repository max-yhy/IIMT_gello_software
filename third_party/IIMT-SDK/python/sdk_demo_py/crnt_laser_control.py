from iimt_api import *
from iimt_tcp_socket import *
import math
import ast

def login_laser():
	SERVER_IP = "192.168.0.105"  
	SERVER_PORT = 5022 
	TIMEOUT = 3              # 超时时间（秒
	socket_client = tcp_connect(SERVER_IP, SERVER_PORT, TIMEOUT)
	return socket_client
def open_laser(s):
    turn_on_the_laser = "[6.0,2.0,4.0,1.1]"
    tcp_send(s,turn_on_the_laser)
    recv_data = tcp_recv(s)
    if recv_data:
        # 转字符串（与encode编码一致）
        recv_msg = recv_data.decode("utf-8")
        print(f"turn_on_the_laser响应：{recv_msg}")
    enable_laser = "[6.0,2.0,5.0,1.1]"
    tcp_send(s,enable_laser)
    recv_data = tcp_recv(s)
    if recv_data:
        recv_msg = recv_data.decode("utf-8")
        print(f"enable_laser响应：{recv_msg}")
def close_laser(s):
    disable_laser = "[6.0,2.0,5.0,2.1]"
    tcp_send(s,disable_laser)
    recv_data = tcp_recv(s)
    if recv_data:
     	# 转字符串（与encode编码一致）
        recv_msg = recv_data.decode("utf-8")
        print(f"disable_laser响应：{recv_msg}")  
    turn_off_the_laser = "[6.0,2.0,4.0,2.1]"
    tcp_send(s,turn_off_the_laser)
    recv_data = tcp_recv(s)
    if recv_data:
        recv_msg = recv_data.decode("utf-8")
        print(f"turn_off_the_laser响应：{recv_msg}")
def logout_laser(s):  
	tcp_close(s)    

def get_robot_send_msg(tcp_pose):
	msg_template = [3.0,1.0,7.0, 245.1922,12.2921,675.3138,5.3447,21.862,0.5881,1.0]   #消息格式模板
	posx = tcp_pose[0] *1000 
	posy = tcp_pose[1] *1000 
	posz = tcp_pose[2] *1000 
	posw = math.degrees(tcp_pose[3])
	posp = math.degrees(tcp_pose[4])
	posr = math.degrees(tcp_pose[5])
	msg_template[3] = posx
	msg_template[4] = posy
	msg_template[5] = posz
	msg_template[6] = posw
	msg_template[7] = posp
	msg_template[8] = posr
	return str(msg_template)
	
def get_seam_point(recv_data,tcp_position):
	recv_msg = recv_data.decode("utf-8")
	lst = ast.literal_eval(recv_msg)
	seam_point = [0.0,0.0,0.0,0.0,0.0,0.0]
	recv_msg_len = len(lst)
	print(f"recv_msg_len：{recv_msg_len}")
	if len(lst) >= 10:
		lst_9 = lst[9]
		print(f"lst[9]：{lst_9}")
		if (lst[9] == 1.0):
			seam_point[0] = lst[3]/1000.0
			seam_point[1] = lst[4]/1000.0
			seam_point[2] = lst[5]/1000.0
			seam_point[3] = tcp_position[3]
			seam_point[4] = tcp_position[4]
			seam_point[5] = tcp_position[5]
			return seam_point
	return None		

