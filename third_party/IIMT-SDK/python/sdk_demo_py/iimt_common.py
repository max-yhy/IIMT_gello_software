# -*- coding: utf-8 -*-
import platform
import os

class CommonSettings:
    def __init__(self):
        #self.address = b'10.10.33.193'  # IP地址
        self.address = b'192.168.8.87'  # IP地址
        self.port = 29999               # 端口号
        current_platform = platform.system()
        print(f"当前的系统: {current_platform}")
        
        if current_platform == "Windows":
            # 获取当前脚本的绝对路径
            current_script_path = os.path.abspath(__file__)
            # 获取当前脚本所在的目录
            current_script_dir = os.path.dirname(current_script_path)
            print(f"current_script_dir: {current_script_dir}")
           
            dll_folder = os.path.join(r"..\windows\x64\lib")
            target_dll = "iimtcl.dll"
            self.path = os.path.join(dll_folder, target_dll)  # 动态库路径
            print(f"动态库路径: {self.path}")
            
        elif current_platform == "Linux":
            self.path = os.path.join(r"../linux/x64/lib", "libiimtcl.so")  # 动态库路径
        else:
            self.path = ""   

common = CommonSettings()     
