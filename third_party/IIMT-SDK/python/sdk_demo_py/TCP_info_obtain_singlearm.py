import socket
import struct
import time

# 请根据实际情况修改机器人的 IP 和端口
ROBOT_IP = "192.168.1.10"
ROBOT_PORT = 30003
PACKET_SIZE = 868
FORCE_LPF_ALPHA = 0.2


class ForceLowPassFilter:
    """Simple exponential low-pass filter for 6D force/torque."""

    def __init__(self, alpha=FORCE_LPF_ALPHA):
        self._alpha = alpha
        self._state = None

    def apply(self, force_dict):
        if self._state is None:
            self._state = dict(force_dict)
            return self._state

        filtered = {}
        for key, value in force_dict.items():
            prev = self._state.get(key, value)
            filtered[key] = self._alpha * value + (1.0 - self._alpha) * prev
        self._state = filtered
        return filtered


_force_filter = ForceLowPassFilter(alpha=FORCE_LPF_ALPHA)


def recv_exact(sock, length):
    """确保每次都能完整接收指定长度的数据包，防止粘包或半包"""
    data = b''
    while len(data) < length:
        packet = sock.recv(length - len(data))
        if not packet:
            raise Exception("连接被服务端断开")
        data += packet
    return data


def read_robot_data():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.settimeout(5.0)

    try:

        
        print(f"正在连接机械臂 {ROBOT_IP}:{ROBOT_PORT}...")
        client.connect((ROBOT_IP, ROBOT_PORT))
        print(">>> TCP 连接成功！开始实时读取末端位姿与力矩...\n")

        count = 0
        while True:
            # 接收完整的一帧数据包 (868字节)
            response = recv_exact(client, PACKET_SIZE)
            count += 1

            # 降频显示（每接收20帧打印一次），避免终端刷屏太快看不清

                # 利用前4个字节的包长(868)自动判断底层端序是小端还是大端
            test_len = struct.unpack('>i', response[0:4])[0]
            endian = '>' if test_len == 868 else '<'
            try:
                    # 核心解析：从偏移量 388 开始，连续读取 12 个 double (每个8字节，共96字节)
                    parsed_data = struct.unpack_from(endian + '12d', response, offset=388)

                    # 获取当前时间戳
                    timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

                    # 1. 前 6 个是 Tool 坐标 (X, Y, Z, Rx, Ry, Rz)
                    tool_x, tool_y, tool_z, tool_rx, tool_ry, tool_rz = parsed_data[0:6]
                    tool_x *= 0.001  # 转换为毫米
                    tool_y *= 0.001
                    tool_z *= 0.001

                    # 2. 后 6 个是 TCP Force，根据实测顺序为 Fx, Mx, Fy, My, Fz, Mz
                    tcp_fx, tcp_mx, tcp_fy, tcp_my, tcp_fz, tcp_mz = parsed_data[6:12]

                    # 将力和力矩全局乘以9.8
                    tcp_fx *= 9.8
                    tcp_fy *= 9.8
                    tcp_fz *= 9.8
                    tcp_mx *= 9.8
                    tcp_my *= 9.8
                    tcp_mz *= 9.8

                    filtered_force = _force_filter.apply(
                        {
                            'fx': tcp_fx,
                            'fy': tcp_fy,
                            'fz': tcp_fz,
                            'mx': tcp_mx,
                            'my': tcp_my,
                            'mz': tcp_mz
                        }
                    )

                    # 打印解析后的数据并附加时间戳
                    print(f"[{timestamp}] Tool坐标: X={tool_x:.3f}, Y={tool_y:.3f}, Z={tool_z:.3f}, Rx={tool_rx:.3f}, Ry={tool_ry:.3f}, Rz={tool_rz:.3f}")
                    print(f"[{timestamp}] TCP力: Fx={filtered_force['fx']:.3f}, Fy={filtered_force['fy']:.3f}, Fz={filtered_force['fz']:.3f}, Mx={filtered_force['mx']:.3f}, My={filtered_force['my']:.3f}, Mz={filtered_force['mz']:.3f}\n")

                    return {
                         "tool_position":{
                            'x': tool_x,
                            'y': tool_y,
                            'z': tool_z,
                            'rx': tool_rx,
                            'ry': tool_ry,
                            'rz': tool_rz
                         },
                                 "tcp_force": filtered_force
                    }

            except Exception as e:
                    print(f"数据解析失败: {e}")

    except KeyboardInterrupt:
        print("\n>>> 已收到停止指令 (Ctrl+C)，退出读取...")
    except Exception as e:
        print(f"\n发生通讯错误: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    read_robot_data()