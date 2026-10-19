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
    print("尝试获取碰撞等级...")
    result,level = API_GetCollisionLevel(handle)
    if result:
        if level.value == CollisionLevel.COLLISION_LEVEL_ZERO:
            print("碰撞关闭")
        elif level.value == CollisionLevel.COLLISION_LEVEL_ONE:
            print("碰撞级别为1级")
        elif level.value == CollisionLevel.COLLISION_LEVEL_TWO:
            print("碰撞级别为2级")
        elif level.value == CollisionLevel.COLLISION_LEVEL_THREE:
            print("碰撞级别为3级")
        elif level.value == CollisionLevel.COLLISION_LEVEL_FOUR:
            print("碰撞级别为4级")
        elif level.value == CollisionLevel.COLLISION_LEVEL_FIVE:
            print("碰撞级别为5级")
        else:
            print("获取异常数据！")                      
    else:
        print("获取失败！")
    
