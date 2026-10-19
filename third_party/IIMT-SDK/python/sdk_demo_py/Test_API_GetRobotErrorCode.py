"""
0:正常 
1:机器人关节速度过快 
2:机器人伺服堵转 
3:机器人硬件过流 
4:电流阈值超限 
5:机器人伺服过温 
6:机器人光栅脉冲丢失 
7:机器人转子定位失败 
8:磁编码器报错 
9:磁编码器过圈保护 
10:欠压保护 
11:机器人继电器打开失败 
12:硬件错误 
13:磁编光编位置差值过大错误 
14: 磁编异常过圈错误 
15:通讯失败 
16:位置超差保护 
17:上位机下发数据出现跳点 
19:机器人本体连接失败 
20:规划错误 
21:超出限制 
22:奇异速度 
40:过温
"""   

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
    print("尝试获取机器人错误码...")
    result,error_code = API_GetRobotErrorCode(handle)
    if result:
        print("获取机器人错误码成功！")
        if error_code.value == 0:
            print("机器人状态正常")
        else:
            print(f"机器人错误码为{error_code.value}")
    else:
        print("获取机器人错误码失败！")
    
