from iimt_api import *

#给 frame 赋值十六进制字符串（带空格/不带空格都可以）
def set_frame_data(frame, hex_str):
    # 去掉空格
    hex_str = hex_str.replace(" ", "")
    # 转bytes
    data = bytes.fromhex(hex_str)
    # 赋值
    for i in range(len(data)):
        frame.data[i] = data[i]
    frame.data_len = len(data)
# 完整打印 bytes 为 十六进制空格分隔格式    
def bytes2hex(data, length=None):
    """把 c_ubyte 数组 转成 干净的十六进制字符串"""
    if length is None:
        length = len(data)
    return ' '.join(f'{b:02x}' for b in data[:length]).upper()

def print_frame(title, frame):
    """规范打印一帧数据（带长度 + 干净数据）"""
    data_hex = bytes2hex(frame.data, frame.data_len)
    print(f"{title}: 长度={frame.data_len}  数据={data_hex}")
print("尝试登录...")
login_result,handle = API_Login()
print(f"登录后的句柄值: {handle.value}")
print(f"API_Login 返回值: {login_result}")
if login_result:
    print("登录成功")
else:
    print("登录失败")
if login_result:
    print("尝试打开串口...")
    param = UART_Params()
    param.SerialPortName = b"/dev/ttyUSB0"
    param.BaudRate = IIMT_BaudRate.Baud9600
    param.DataBits = IIMT_DataBits.Data8
    param.Parity = IIMT_Parity.NoParity
    param.StopBits = IIMT_StopBits.OneStop	
    open_result = API_OpenSerialPort(handle,param)
    if open_result:
        print("串口打开成功")
        print("尝试发送ModbusRTU命令，获取回应...")
        rtu_request = ModbusRTU_Frame()
        rtu_response = ModbusRTU_Frame()
        timeout = 2
        # 直接传带空格的十六进制字符串就行！
        #hex_string = '01 01 00 00 00 01 fd ca'
        hex_string = '01 10 00 06 00 0A 14 00 0B 00 16 00 21 00 2C 00 37 00 42 00 4D 00 58 00 63 00 64 FC 5F'
		# 赋值给 rtu_request
        set_frame_data(rtu_request, hex_string)
        result = API_SendRtuCmd(handle,rtu_request,rtu_response,timeout)
        if result:
        	print("串口命令发送成功...")
        	print_frame("发送的命令", rtu_request)
        	print_frame("接收到的响应", rtu_response)
        else:
        	print("串口命令发送失败...")
        print("尝试关闭串口...")
        result = API_CloseSerialPort(handle)
        if result:
        	print("串口关闭成功！")
        else:
        	print("串口关闭失败！")
    
