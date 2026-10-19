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
    print("尝试获取变量值...")
    var_name = b"i_var_1"
    result,var_value = API_GetVariableValue(handle,var_name)
    if result:
        print(f"获取变量值为:{var_value.description}")
    else:
        print("获取变量值失败")
    
