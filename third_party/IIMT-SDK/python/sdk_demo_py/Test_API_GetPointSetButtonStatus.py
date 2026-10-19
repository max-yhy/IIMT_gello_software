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
    print("尝试获取末端点位设置按钮状态...")
    result,status = API_GetPointSetButtonStatus(handle)
    if result:
        print("获取末端点位设置按钮状态成功！")
        if status.value == ToolButtonStatus.BUTTON_STATUS_ERROR:
            print("状态不可用机器人可能未上电释放抱闸！")
        elif status.value == ToolButtonStatus.BUTTON_STATUS_PRESS_DOWN:
            print("点位设置按钮处于按下状态！")
        elif status.value == ToolButtonStatus.BUTTON_STATUS_RELEASE:
            print("点位设置按钮处于松开状态！")
        else:
            print("获取状态异常！！！")        
    else:
        print("获取末端点位设置按钮状态失败！")
    
