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
    level = CollisionLevel.COLLISION_LEVEL_ZERO
    print("尝试设置碰撞等级...")
    result = API_SetCollisionLevel(handle,level)
    if result:
        print(f"设置碰撞等级{level}")
    else:
        print("设置失败！")
    
