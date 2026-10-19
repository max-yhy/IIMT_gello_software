from iimt_api import *
import time

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
    print("尝试0x10写1个寄存器命令，获取回应...")
    rtu_request = ModbusRTU_Request()
    rtu_response = ModbusRTU_Frame()
    timeout = 2
    rtu_request.slave_addr = 0x09 
    rtu_request.func_code = 0x10 
    rtu_request.start_addr = 1000
    rtu_request.data_number = 0x0001 
    # 数据域
    data_list = [0x01]
    for i, val in enumerate(data_list):
    	rtu_request.data[i] = val
    rtu_request.data_len = rtu_request.data_number*2
    result = API_ModbusRtuRWEndTool(handle,rtu_request,rtu_response,timeout)
    if result:
    	print("尝试0x10写1个寄存器命令成功...")
    	print_frame("接收到的响应", rtu_response)
    else:
    	print("串口01命令发送失败...")
    print("尝试0x10写2个寄存器命令，获取回应...")
    rtu_request.slave_addr = 0x09 
    rtu_request.func_code = 0x10 
    rtu_request.start_addr = 1001
    rtu_request.data_number = 0x0002 
     # 数据域
    data_list = [65380,65535]
    result = API_ModbusRtuRWEndTool(handle,rtu_request,rtu_response,timeout)
    if result:
    	print("尝试0x10写2个寄存器命令成功...")
    	print_frame("接收到的响应", rtu_response)
    else:
    	print("尝试0x10写2个寄存器命令失败...")
    print("尝试0x04命令读取1个寄存器...")	
    rtu_request.slave_addr = 0x09
    rtu_request.func_code = 0x04
    rtu_request.start_addr = 1000 
    rtu_request.data_number = 0x0001
    result = API_ModbusRtuRWEndTool(handle,rtu_request,rtu_response,timeout)
    if result:
    	print("0x04命令读取一个寄存器成功...")
    	print_frame("接收到的响应", rtu_response)
    else:
    	print("0x04命令读取一个寄存器失败...")	
    print("尝试0x04命令读取2个寄存器...")	
    rtu_request.slave_addr = 0x09
    rtu_request.func_code = 0x04
    rtu_request.start_addr = 1000 
    rtu_request.data_number = 0x0002
    result = API_ModbusRtuRWEndTool(handle,rtu_request,rtu_response,timeout)
    if result:
    	print("0x04命令读取2个寄存器成功...")
    	print_frame("接收到的响应", rtu_response)
    else:
    	print("0x04命令读取2个寄存器失败...")	

    
