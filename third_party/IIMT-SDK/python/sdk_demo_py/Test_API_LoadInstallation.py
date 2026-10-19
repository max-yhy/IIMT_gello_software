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
    print("尝试加载安装配置...")
    installation_file_name=b"default2"
    loadinstallation_result = sdk.API_LoadInstallation(handle,installation_file_name)
    if loadinstallation_result:
        print(f"加装配置成功，返回值：{loadinstallation_result}")
    else:
        print("加载安装配置失败")
    
