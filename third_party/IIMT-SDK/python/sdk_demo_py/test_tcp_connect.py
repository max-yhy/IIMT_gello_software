import socket

def tcp_client_advanced(server_ip, server_port, timeout=3):
    """
    进阶TCP客户端（带超时、循环发送、接收响应）
    :param server_ip: 服务端IP
    :param server_port: 服务端端口
    :param timeout: 连接/发送/接收超时时间（秒），默认3秒
    """
    # 1. 创建socket并设置超时
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.settimeout(timeout)  # 设置全局超时（连接/发送/接收都生效）
    
    try:
        # 2. 连接服务端
        client_socket.connect((server_ip, server_port))
        print(f"✅ 成功连接到服务端 {server_ip}:{server_port}（超时时间：{timeout}秒）")
        
        # 3. 循环发送消息（输入"exit"退出）
        while True:
            # 输入要发送的消息
            send_msg = input("\n请输入要发送的字符串（输入'exit'退出）：")
            
            # 退出条件
            if send_msg.strip().lower() == "exit":
                print("📤 客户端主动退出")
                break
            
            # 空消息跳过
            if not send_msg.strip():
                print("⚠️ 消息不能为空，请重新输入")
                continue
            
            # 4. 发送消息（转bytes）
            client_socket.send(send_msg.encode("utf-8"))
            print(f"📤 已发送：{send_msg}")
            
            # 5. 接收服务端响应（可选，若服务端会返回数据）
            try:
                # 接收缓冲区设为1024字节，可根据需求调整
                recv_data = client_socket.recv(1024)
                if recv_data:
                    # 转字符串（与encode编码一致）
                    recv_msg = recv_data.decode("utf-8")
                    print(f"📥 服务端响应：{recv_msg}")
                else:
                    print("⚠️ 服务端已关闭连接")
                    break
            except socket.timeout:
                print("⚠️ 接收响应超时（服务端未返回数据）")
    
    except ConnectionRefusedError:
        print(f"❌ 连接失败：服务端 {server_ip}:{server_port} 未启动/拒绝连接")
    except socket.timeout:
        print(f"❌ 连接超时：{timeout}秒内未连接到 {server_ip}:{server_port}")
    except Exception as e:
        print(f"❌ 客户端异常：{e}")
    finally:
        # 关闭socket
        client_socket.close()
        print("\n🔌 客户端socket已关闭")

# ------------------- 测试调用 -------------------
if __name__ == "__main__":
    # 配置服务端IP和端口（替换为你的实际地址）
    SERVER_IP = "192.168.0.105"  # 本地测试用127.0.0.1，远程用服务端公网/内网IP
    SERVER_PORT = 29998       # 需与服务端监听端口一致
    TIMEOUT = 3              # 超时时间（秒），对齐你之前C++的3秒逻辑
    
    tcp_client_advanced(SERVER_IP, SERVER_PORT, TIMEOUT)
