import socket

def tcp_connect(server_ip, server_port, timeout=3):
    """
    TCP客户端连接函数（带超时）
    成功返回 socket 对象，失败返回 None
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout)
    
    try:
        s.connect((server_ip, server_port))
        print(f"成功连接到服务端 {server_ip}:{server_port}（超时时间：{timeout}秒）")
        return s  # 成功，返回 socket（由调用者负责后续使用和关闭）
    except ConnectionRefusedError:
        print(f"连接失败：服务端 {server_ip}:{server_port} 未启动/拒绝连接")
    except socket.timeout:
        print(f"连接超时：{timeout}秒内未连接到 {server_ip}:{server_port}")
    except Exception as e:
        print(f"客户端异常：{e}")
    
    # 只有在失败时才关闭 socket
    s.close()
    print("\n客户端socket已关闭")
    return None  # 明确返回 None 表示失败
def tcp_send(s,send_msg):
	s.send(send_msg.encode("utf-8"))     
	
def tcp_recv(s):
	recv_msg = s.recv(1024)
	return recv_msg
	
def tcp_close(s):	
	s.close()


