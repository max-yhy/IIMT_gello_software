import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
import socket

class LaserTrackerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("CXZK-JXB200S 激光焊缝跟踪传感器控制 (TCP)")
        self.root.geometry("850x700")
        self.root.resizable(False, False)

        # 传感器状态变量
        self.sock = None
        self.connected = False
        self.tracking_enabled = False
        self.laser_on = False
        self.reading_deviation = False
        self.read_thread = None

        # ===================== 界面布局 =====================
        # 1. 连接参数区域
        frame_conn = ttk.LabelFrame(root, text="传感器连接参数")
        frame_conn.pack(padx=10, pady=10, fill=tk.X)

        ttk.Label(frame_conn, text="传感器IP:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.ip_entry = ttk.Entry(frame_conn, width=20)
        self.ip_entry.grid(row=0, column=1, padx=5, pady=5)
        self.ip_entry.insert(0, "192.168.1.100")

        ttk.Label(frame_conn, text="端口:").grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)
        self.port_entry = ttk.Entry(frame_conn, width=10)
        self.port_entry.grid(row=0, column=3, padx=5, pady=5)
        self.port_entry.insert(0, "8000")  # 创想常用端口，确认实际端口！

        # 从站ID 不再需要（TCP 自定义协议）
        self.slave_label = ttk.Label(frame_conn, text="（TCP模式无需从站ID）", foreground="gray")
        self.slave_label.grid(row=0, column=4, columnspan=2, padx=5, pady=5)

        self.conn_btn = ttk.Button(frame_conn, text="连接传感器", command=self.toggle_connect)
        self.conn_btn.grid(row=0, column=6, padx=10, pady=5)

        self.status_label = ttk.Label(frame_conn, text="状态：未连接", foreground="red")
        self.status_label.grid(row=0, column=7, padx=10, pady=5)

        # 2. 核心控制区域
        frame_ctrl = ttk.LabelFrame(root, text="核心控制")
        frame_ctrl.pack(padx=10, pady=5, fill=tk.X)

        self.laser_btn = ttk.Button(frame_ctrl, text="打开激光", command=self.toggle_laser, state=tk.DISABLED)
        self.laser_btn.grid(row=0, column=0, padx=10, pady=10)

        self.enable_btn = ttk.Button(frame_ctrl, text="开启使能", command=self.toggle_enable, state=tk.DISABLED)
        self.enable_btn.grid(row=0, column=1, padx=10, pady=10)

        ttk.Label(frame_ctrl, text="工艺号:").grid(row=0, column=2, padx=5, pady=10, sticky=tk.W)
        self.process_entry = ttk.Entry(frame_ctrl, width=8)
        self.process_entry.grid(row=0, column=3, padx=5, pady=10)
        self.process_entry.insert(0, "1")
        self.process_btn = ttk.Button(frame_ctrl, text="调用工艺号", command=self.set_process_id, state=tk.DISABLED)
        self.process_btn.grid(row=0, column=4, padx=5, pady=10)

        self.read_var = tk.BooleanVar()
        self.read_check = ttk.Checkbutton(frame_ctrl, text="实时读取偏差(X/Z)", variable=self.read_var,
                                          command=self.toggle_read_deviation, state=tk.DISABLED)
        self.read_check.grid(row=0, column=5, padx=10, pady=10)

        # 3. 偏差显示区域
        frame_deviation = ttk.LabelFrame(root, text="焊缝偏差(mm)")
        frame_deviation.pack(padx=10, pady=5, fill=tk.X)

        ttk.Label(frame_deviation, text="X轴偏差:").grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
        self.deviation_x_label = ttk.Label(frame_deviation, text="--", font=("Arial", 12))
        self.deviation_x_label.grid(row=0, column=1, padx=5, pady=10)

        ttk.Label(frame_deviation, text="Z轴偏差:").grid(row=0, column=2, padx=10, pady=10, sticky=tk.W)
        self.deviation_z_label = ttk.Label(frame_deviation, text="--", font=("Arial", 12))
        self.deviation_z_label.grid(row=0, column=3, padx=5, pady=10)

        # 4. 日志显示区域
        frame_log = ttk.LabelFrame(root, text="操作日志")
        frame_log.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

        self.log_text = tk.Text(frame_log, height=8, state=tk.DISABLED)
        self.log_text.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)

    def log(self, msg):
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, f"[{time.strftime('%H:%M:%S')}] {msg}\n")
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)

    def send_command(self, cmd_str):
        """发送命令并返回响应（带超时）"""
        if not self.connected or not self.sock:
            return None
        try:
            self.log(f"发送指令: {cmd_str}")
            self.sock.sendall(cmd_str.encode('utf-8') + b'\n')  # 假设以\n结尾
            # 尝试接收响应（最多1024字节，超时由socket设置）
            response = self.sock.recv(1024).decode('utf-8').strip()
            self.log(f"收到响应: {response}")
            return response
        except Exception as e:
            self.log(f"通信错误: {e}")
            return None

    def toggle_connect(self):
        if not self.connected:
            try:
                ip = self.ip_entry.get().strip()
                port = int(self.port_entry.get().strip())
                # 创建并连接
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.sock.settimeout(3)  # 3秒超时
                self.sock.connect((ip, port))
                self.connected = True
                self.status_label.config(text="状态：已连接", foreground="green")
                self.conn_btn.config(text="断开传感器")
                self.laser_btn.config(state=tk.NORMAL)
                self.enable_btn.config(state=tk.NORMAL)
                self.process_btn.config(state=tk.NORMAL)
                self.read_check.config(state=tk.NORMAL)
                self.log(f"成功连接传感器 {ip}:{port}")
            except Exception as e:
                self.log(f"连接失败：{e}")
                messagebox.showerror("错误", f"连接失败：{e}")
                if self.sock:
                    self.sock.close()
                    self.sock = None
        else:
            self.stop_read_deviation()
            self.connected = False
            if self.sock:
                try:
                    self.sock.close()
                except:
                    pass
                self.sock = None
            self.status_label.config(text="状态：未连接", foreground="red")
            self.conn_btn.config(text="连接传感器")
            self.laser_btn.config(state=tk.DISABLED, text="打开激光")
            self.enable_btn.config(state=tk.DISABLED, text="开启使能")
            self.process_btn.config(state=tk.DISABLED)
            self.read_check.config(state=tk.DISABLED)
            self.read_var.set(False)
            self.laser_on = False
            self.tracking_enabled = False
            self.deviation_x_label.config(text="--")
            self.deviation_z_label.config(text="--")
            self.log("已断开传感器连接")

    def toggle_laser(self):
        if not self.connected:
            return
        if not self.laser_on:
            cmd = "[6.0,2.0,4.0,1.0]"
            resp = self.send_command(cmd)
            if resp is not None:
                self.laser_on = True
                self.laser_btn.config(text="关闭激光")
                self.log("激光已开启")
                messagebox.showinfo("提示", "激光开启成功！")
            else:
                messagebox.showerror("错误", "激光开启失败！")
        else:
            cmd = "[6.0,2.0,4.0,2.0]"
            resp = self.send_command(cmd)
            if resp is not None:
                self.laser_on = False
                self.laser_btn.config(text="打开激光")
                self.log("激光已关闭")
                messagebox.showinfo("提示", "激光关闭成功！")
            else:
                messagebox.showerror("错误", "激光关闭失败！")

    def toggle_enable(self):
        if not self.connected:
            return
        if not self.tracking_enabled:
            cmd = "[6.0,2.0,5.0,1.0]"
            resp = self.send_command(cmd)
            if resp is not None:
                self.tracking_enabled = True
                self.enable_btn.config(text="关闭使能")
                self.log("使能已开启")
                messagebox.showinfo("提示", "使能开启成功！")
            else:
                messagebox.showerror("错误", "使能开启失败！")
        else:
            cmd = "[6.0,2.0,5.0,2.0]"
            resp = self.send_command(cmd)
            if resp is not None:
                self.tracking_enabled = False
                self.enable_btn.config(text="开启使能")
                self.log("使能已关闭")
                messagebox.showinfo("提示", "使能关闭成功！")
            else:
                messagebox.showerror("错误", "使能关闭失败！")

    def set_process_id(self):
        if not self.connected:
            messagebox.warning("提示", "请先连接传感器！")
            return
        try:
            pid = int(self.process_entry.get().strip())
            if pid < 0 or pid > 65535:
                raise ValueError("工艺号范围 0-65535")
            # 假设工艺号指令格式：[6.0,2.0,6.0,<pid>]
            cmd = f"[6.0,2.0,6.0,{float(pid)}]"
            resp = self.send_command(cmd)
            if resp is not None:
                self.log(f"工艺号 {pid} 设置成功")
                messagebox.showinfo("提示", f"工艺号 {pid} 调用成功！")
            else:
                messagebox.showerror("错误", "工艺号设置失败！")
        except Exception as e:
            self.log(f"工艺号错误: {e}")
            messagebox.showerror("错误", f"工艺号输入错误：{e}")

    def read_deviation_loop(self):
        """轮询读取偏差（假设需发送读取命令，或传感器主动推送）"""
        # 如果传感器主动推送，这里只需 recv；否则需发读取命令
        while self.reading_deviation and self.connected:
            try:
                # 方案1：假设传感器主动推送偏差数据（如 "[1.23, -0.45]"）
                # data = self.sock.recv(1024).decode('utf-8').strip()
                
                # 方案2：主动发送读取命令（根据手册确认）
                # 例如：发送 "[6.0,1.0,0.0,0.0]" 请求偏差
                # self.sock.sendall("[6.0,1.0,0.0,0.0]\n".encode())
                # data = self.sock.recv(1024).decode().strip()

                # 此处按“主动推送”模拟（实际需根据协议调整）
                # 为演示，我们每秒伪造一次（实际应 recv）
                time.sleep(1)
                # 模拟从传感器读到的数据，例如："[1.25,-0.30]"
                # 实际应替换为：data = self.sock.recv(1024).decode().strip()
                # 假设我们收到了有效数据
                # 示例解析：
                # if data.startswith('[') and data.endswith(']'):
                #     vals = list(map(float, data[1:-1].split(',')))
                #     x, z = vals[0], vals[1]

                # ⚠️ 以下仅为演示！你需要根据实际协议修改！
                # 这里暂时不实现真实读取，仅展示框架
                self.log("（模拟）正在读取偏差...")
                # 如需真实读取，请取消注释下面逻辑并适配协议
                """
                data = self.sock.recv(1024).decode('utf-8').strip()
                if data.startswith('[') and data.endswith(']'):
                    try:
                        nums = list(map(float, data[1:-1].split(',')))
                        if len(nums) >= 2:
                            x_val, z_val = nums[0], nums[1]
                            self.root.after(0, lambda: self.deviation_x_label.config(text=f"{x_val:.2f}"))
                            self.root.after(0, lambda: self.deviation_z_label.config(text=f"{z_val:.2f}"))
                            self.log(f"读取偏差：X={x_val:.2f}mm, Z={z_val:.2f}mm")
                    except:
                        pass
                """
            except Exception as e:
                self.log(f"偏差读取异常: {e}")
                time.sleep(1)

    def toggle_read_deviation(self):
        if self.read_var.get():
            if not self.connected:
                self.read_var.set(False)
                messagebox.warning("提示", "请先连接传感器！")
                return
            self.reading_deviation = True
            self.read_thread = threading.Thread(target=self.read_deviation_loop, daemon=True)
            self.read_thread.start()
            self.log("开始实时读取焊缝偏差")
        else:
            self.stop_read_deviation()

    def stop_read_deviation(self):
        self.reading_deviation = False
        self.read_var.set(False)
        self.log("停止实时读取焊缝偏差")

    def on_closing(self):
        self.stop_read_deviation()
        if self.connected:
            self.toggle_connect()
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = LaserTrackerGUI(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()
