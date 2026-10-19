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
    print("尝试打开串口...")
    param = IIMT_SerialPortParameters()
    param.SerialPortName = b"/dev/ttyUSB0"
    param.BaudRate = IIMT_BaudRate.Baud115200
    param.DataBits = IIMT_DataBits.Data8
    param.Parity = IIMT_Parity.NoParity
    param.StopBits = IIMT_StopBits.OneStop	
    open_result = API_OpenSerialPort(handle,param)
    if open_result:
    	print("串口打开成功")
    	print("尝试关闭串口...")
    	result = API_CloseSerialPort(handle)
    	if result:
		    print("串口关闭成功！")
    	else:
    		print("串口关闭失败！")
    else:
    	print("串口打开失败")
   
    
