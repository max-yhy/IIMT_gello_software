import ctypes
from ctypes import c_short,c_ushort, c_uint,c_int,c_long,c_double, POINTER,c_char_p,c_void_p
import time
from iimt_common import common
from iimt_ctypes import *

try:
    sdk = ctypes.CDLL(common.path)  
except OSError as e:
    print(f"Failed to load SDK dynamic library: {e}")
    exit(1)

def API_HelloWorld():
	try:
		sdk.API_HelloWorld()  
	except Exception as e:
		print(f"Exception occurred: {e}")

def API_Login(): 
    sdk.API_Login.argtypes = [ctypes.c_char_p, ctypes.c_int, ctypes.POINTER(JTRHD)]
    sdk.API_Login.restype = BOOL
    ip = common.address
    port = common.port 
    handle = JTRHD()
    try:
        result = sdk.API_Login(ip, port, ctypes.byref(handle))
        return result,handle    
    except Exception as e:
        print(f"Exception occurred: {e}")    
        
def API_Logout(handle):   
	sdk.API_Logout.argtypes = [ctypes.POINTER(JTRHD)]
	sdk.API_Logout.restype = BOOL  
	try:
	    result = sdk.API_Logout(ctypes.byref(handle))    
	    return result    
	except Exception as e:
	    print(f"Exception occurred: {e}")      
	    
def API_SetDebugMode(handle,is_debug):   
	sdk.API_SetDebugMode.argtypes = [JTRHD,BOOL]
	sdk.API_SetDebugMode.restype = BOOL  
	try:
	    result = sdk.API_SetDebugMode(handle,is_debug)    
	    return result    
	except Exception as e:
	    print(f"Exception occurred: {e}")  
	    
def API_GetDebugMode(handle):   
	sdk.API_SetDebugMode.argtypes = [JTRHD,ctypes.POINTER(BOOL)]
	sdk.API_SetDebugMode.restype = BOOL
	is_debug = BOOL()  
	try:
	    result = sdk.API_GetDebugMode(handle,ctypes.byref(is_debug))    
	    return result,is_debug   
	except Exception as e:
	    print(f"Exception occurred: {e}")   
	      
def API_GetErrorInfo(handle):   
	sdk.API_GetErrorInfo.argtypes = [JTRHD,ctypes.POINTER(ErrorInfo)]
	sdk.API_GetErrorInfo.restype = BOOL
	info = ErrorInfo()  
	try:
	    result = sdk.API_GetErrorInfo(handle,ctypes.byref(info))    
	    return result,info   
	except Exception as e:
	    print(f"Exception occurred: {e}")	 
	    
def API_PowerOn(handle):   
	sdk.API_PowerOn.argtypes = [JTRHD]
	sdk.API_PowerOn.restype = BOOL 
	try:
	    result = sdk.API_PowerOn(handle)    
	    return result   
	except Exception as e:
	    print(f"Exception occurred: {e}")	
	    
def API_ReleaseBrake(handle):   
	sdk.API_ReleaseBrake.argtypes = [JTRHD]
	sdk.API_ReleaseBrake.restype = BOOL 
	try:
	    result = sdk.API_ReleaseBrake(handle)    
	    return result   
	except Exception as e:
	    print(f"Exception occurred: {e}")	    

def API_PowerOff(handle):   
	sdk.API_PowerOff.argtypes = [JTRHD]
	sdk.API_PowerOff.restype = BOOL 
	try:
	    result = sdk.API_PowerOff(handle)    
	    return result   
	except Exception as e:
	    print(f"Exception occurred: {e}")	  
	    
def API_Play(handle):   
	sdk.API_Play.argtypes = [JTRHD]
	sdk.API_Play.restype = BOOL 
	try:
	    result = sdk.API_Play(handle)    
	    return result   
	except Exception as e:
	    print(f"Exception occurred: {e}")	 
	    
def API_Stop(handle):   
	sdk.API_Stop.argtypes = [JTRHD]
	sdk.API_Stop.restype = BOOL 
	try:
	    result = sdk.API_Stop(handle)    
	    return result   
	except Exception as e:
	    print(f"Exception occurred: {e}")	
	    
def API_Pause(handle):   
	sdk.API_Pause.argtypes = [JTRHD]
	sdk.API_Pause.restype = BOOL 
	try:
	    result = sdk.API_Pause(handle)    
	    return result   
	except Exception as e:
	    print(f"Exception occurred: {e}")	    	          	    
	          
def API_LoadProgram(handle,program_file_name):
	sdk.API_LoadProgram.argtypes = [JTRHD,ctypes.c_char_p]
	sdk.API_LoadProgram.restype = BOOL
	try:
	    result = sdk.API_LoadProgram(handle,program_file_name)    
	    return result   
	except Exception as e:
	    print(f"Exception occurred: {e}")	
	    
def API_LoadInstallation(handle,installation_file_name):
	sdk.API_LoadInstallation.argtypes = [JTRHD,ctypes.c_char_p]
	sdk.API_LoadInstallation.restype = BOOL
	try:
	    result = sdk.API_LoadInstallation(handle,installation_file_name)    
	    return result   
	except Exception as e:
	    print(f"Exception occurred: {e}")	
	    
def API_Shutdown(handle):   
	sdk.API_Shutdown.argtypes = [JTRHD]
	sdk.API_Shutdown.restype = BOOL 
	try:
	    result = sdk.API_Shutdown(handle)    
	    return result   
	except Exception as e:
	    print(f"Exception occurred: {e}")	
	    
def API_Running(handle):
	sdk.API_Running.argtypes = [JTRHD,ctypes.POINTER(ProgramRunning)]
	sdk.API_Running.restype = BOOL
	program_running = ProgramRunning()
	try:
	    result = sdk.API_Running(handle,ctypes.byref(program_running))    
	    return result,program_running   
	except Exception as e:
	    print(f"Exception occurred: {e}")  
	    
def API_IsProgramSaved(handle):
	sdk.API_IsProgramSaved.argtypes = [JTRHD,ctypes.POINTER(ProgramSaved)]
	sdk.API_IsProgramSaved.restype = BOOL
	program_saved = ProgramSaved()
	try:
	    result = sdk.API_IsProgramSaved(handle,ctypes.byref(program_saved))    
	    return result,program_saved   
	except Exception as e:
	    print(f"Exception occurred: {e}") 	     
	    
def API_IsInRemoteControl(handle):
	sdk.API_IsInRemoteControl.argtypes = [JTRHD,ctypes.POINTER(InRemoteControl)]
	sdk.API_IsInRemoteControl.restype = BOOL
	in_remote_control = InRemoteControl()
	try:
	    result = sdk.API_IsInRemoteControl(handle,ctypes.byref(in_remote_control))    
	    return result,in_remote_control   
	except Exception as e:
	    print(f"Exception occurred: {e}") 	
	    
def API_Popup(handle,popup_text):
	sdk.API_Popup.argtypes = [JTRHD,ctypes.c_char_p]
	sdk.API_Popup.restype = BOOL
	try:
	    result = sdk.API_Popup(handle,popup_text)    
	    return result   
	except Exception as e:
	    print(f"Exception occurred: {e}")	 
	    
def API_ClosePopup(handle):   
	sdk.API_Shutdown.argtypes = [JTRHD]
	sdk.API_Shutdown.restype = BOOL 
	try:
	    result = sdk.API_ClosePopup(handle)    
	    return result   
	except Exception as e:
	    print(f"Exception occurred: {e}")	                 
   
def API_AddToLog(handle,log_text):   
	sdk.API_AddToLog.argtypes = [JTRHD,ctypes.c_char_p]
	sdk.API_AddToLog.restype = BOOL  
	try:
	    result = sdk.API_AddToLog(handle,log_text)    
	    return result    
	except Exception as e:
	    print(f"Exception occurred: {e}")   
	    
def API_GetControllerVersion(handle):
	sdk.API_GetControllerVersion.argtypes = [JTRHD,ctypes.POINTER(ControllerVersion)]
	sdk.API_GetControllerVersion.restype = BOOL
	controller_version = ControllerVersion()
	try:
	    result = sdk.API_GetControllerVersion(handle,ctypes.byref(controller_version))    
	    return result,controller_version   
	except Exception as e:
	    print(f"Exception occurred: {e}")	
	    
def API_GetVersion(handle):
	sdk.API_GetVersion.argtypes = [JTRHD,ctypes.POINTER(VersionInfo)]
	sdk.API_GetVersion.restype = BOOL
	version = VersionInfo()
	try:
	    result = sdk.API_GetVersion(handle,ctypes.byref(version))    
	    return result,version   
	except Exception as e:
	    print(f"Exception occurred: {e}")	
	    
def API_GetRobotModel(handle):
	sdk.API_GetRobotModel.argtypes = [JTRHD,ctypes.POINTER(RobotModel)]
	sdk.API_GetRobotModel.restype = BOOL
	robot_model = RobotModel()
	try:
	    result = sdk.API_GetRobotModel(handle,ctypes.byref(robot_model))    
	    return result,robot_model   
	except Exception as e:
	    print(f"Exception occurred: {e}")	
	    
def API_GetSerialNumber(handle):
	sdk.API_GetSerialNumber.argtypes = [JTRHD,ctypes.POINTER(SerialNumber)]
	sdk.API_GetSerialNumber.restype = BOOL
	serial_number = SerialNumber()
	try:
	    result = sdk.API_GetSerialNumber(handle,ctypes.byref(serial_number))    
	    return result,serial_number   
	except Exception as e:
	    print(f"Exception occurred: {e}")	   
	    
def API_GetRobotMode(handle):
	sdk.API_GetRobotMode.argtypes = [JTRHD,ctypes.POINTER(RobotMode)]
	sdk.API_GetRobotMode.restype = BOOL
	robot_mode = RobotMode()
	try:
	    result = sdk.API_GetRobotMode(handle,ctypes.byref(robot_mode))    
	    return result,robot_mode   
	except Exception as e:
	    print(f"Exception occurred: {e}")	 
	    
def API_GetLoadedProgram(handle):
	sdk.API_GetLoadedProgram.argtypes = [JTRHD,ctypes.POINTER(LoadedProgram)]
	sdk.API_GetLoadedProgram.restype = BOOL
	loaded_program = LoadedProgram()
	try:
	    result = sdk.API_GetLoadedProgram(handle,ctypes.byref(loaded_program))    
	    return result,loaded_program   
	except Exception as e:
	    print(f"Exception occurred: {e}")
	    
def API_GetSafetyStatus(handle):
	sdk.API_GetSafetyStatus.argtypes = [JTRHD,ctypes.POINTER(SafetyStatus)]
	sdk.API_GetSafetyStatus.restype = BOOL
	safety_status = SafetyStatus()
	try:
	    result = sdk.API_GetSafetyStatus(handle,ctypes.byref(safety_status))    
	    return result,safety_status   
	except Exception as e:
	    print(f"Exception occurred: {e}")	    
	    
def API_GetProgramState(handle):
	sdk.API_GetProgramState.argtypes = [JTRHD,ctypes.POINTER(ProgramState)]
	sdk.API_GetProgramState.restype = BOOL
	program_state = ProgramState()
	try:
	    result = sdk.API_GetProgramState(handle,ctypes.byref(program_state))    
	    return result,program_state   
	except Exception as e:
	    print(f"Exception occurred: {e}") 	 
	    
def API_GetOperationalMode(handle):
	sdk.API_GetOperationalMode.argtypes = [JTRHD,ctypes.POINTER(OperationalMode)]
	sdk.API_GetOperationalMode.restype = BOOL
	operational_mode = OperationalMode()
	try:
	    result = sdk.API_GetOperationalMode(handle,ctypes.byref(operational_mode))    
	    return result,operational_mode   
	except Exception as e:
	    print(f"Exception occurred: {e}") 	 
	    
def API_SetOperationalMode(handle,operational_mode):   
	sdk.API_SetOperationalMode.argtypes = [JTRHD,ctypes.c_char_p]
	sdk.API_SetOperationalMode.restype = BOOL  
	try:
	    result = sdk.API_SetOperationalMode(handle,operational_mode)    
	    return result    
	except Exception as e:
	    print(f"Exception occurred: {e}")	 
	    
def API_ClearOperationalMode(handle):   
	sdk.API_ClearOperationalMode.argtypes = [JTRHD]
	sdk.API_ClearOperationalMode.restype = BOOL 
	try:
	    result = sdk.API_ClearOperationalMode(handle)    
	    return result   
	except Exception as e:
	    print(f"Exception occurred: {e}")	
	    
def API_FreeDriveMode(handle):   
	sdk.API_FreeDriveMode.argtypes = [JTRHD]
	sdk.API_FreeDriveMode.restype = BOOL 
	try:
	    result = sdk.API_FreeDriveMode(handle)    
	    return result   
	except Exception as e:
	    print(f"Exception occurred: {e}")	  
	    
def API_EndFreeDriveMode(handle):   
	sdk.API_EndFreeDriveMode.argtypes = [JTRHD]
	sdk.API_EndFreeDriveMode.restype = BOOL 
	try:
	    result = sdk.API_EndFreeDriveMode(handle)    
	    return result   
	except Exception as e:
	    print(f"Exception occurred: {e}")	  
	    
def API_ManualTeachStart(handle,num,direction,step_size):   
	sdk.API_ManualTeachStart.argtypes = [JTRHD,ctypes.c_int,ctypes.c_int,ctypes.c_float]
	sdk.API_ManualTeachStart.restype = BOOL 
	try:
	    result = sdk.API_ManualTeachStart(handle,num,direction,step_size)    
	    return result   
	except Exception as e:
	    print(f"Exception occurred: {e}")
	    
def API_ManualTeachEnd(handle,num,direction):   
	sdk.API_ManualTeachEnd.argtypes = [JTRHD,ctypes.c_int,ctypes.c_int]
	sdk.API_ManualTeachEnd.restype = BOOL 
	try:
	    result = sdk.API_ManualTeachEnd(handle,num,direction)    
	    return result   
	except Exception as e:
	    print(f"Exception occurred: {e}")	
	    
def API_Servoj(handle,servoj_param):   
	sdk.API_Servoj.argtypes = [JTRHD,ctypes.POINTER(ServojParam)]
	sdk.API_Servoj.restype = BOOL 
	try:
	    result = sdk.API_Servoj(handle,ctypes.byref(servoj_param))    
	    return result   
	except Exception as e:
	    print(f"Exception occurred: {e}")	
	    	
def API_Servoc(handle,servoc_param):   
	sdk.API_Servoc.argtypes = [JTRHD,ctypes.POINTER(ServocParam)]
	sdk.API_Servoc.restype = BOOL 
	try:
	    result = sdk.API_Servoc(handle,ctypes.byref(servoc_param))    
	    return result   
	except Exception as e:
	    print(f"Exception occurred: {e}")	     
	    
def API_Movej(handle,movej_param,is_block,timeout):   
	sdk.API_Movej.argtypes = [JTRHD,ctypes.POINTER(MovejParam),ctypes.c_bool,ctypes.c_int]
	sdk.API_Movej.restype = BOOL 
	try:
	    result = sdk.API_Movej(handle,ctypes.byref(movej_param),is_block,timeout)    
	    return result   
	except Exception as e:
	    print(f"Exception occurred: {e}")	
	    
def API_Movel(handle,movej_param,is_block,timeout):   
	sdk.API_Movel.argtypes = [JTRHD,ctypes.POINTER(MovelParam),ctypes.c_bool,ctypes.c_int]
	sdk.API_Movel.restype = BOOL 
	try:
	    result = sdk.API_Movel(handle,ctypes.byref(movej_param),is_block,timeout)    
	    return result   
	except Exception as e:
	    print(f"Exception occurred: {e}")	   
	    
def API_Movepc(handle,movepc_param,is_block=False,timeout=0):   
	sdk.API_Movepc.argtypes = [JTRHD,ctypes.POINTER(MovepcParam),ctypes.c_bool,ctypes.c_int]
	sdk.API_Movepc.restype = BOOL 
	try:
	    result = sdk.API_Movepc(handle,ctypes.byref(movepc_param),is_block,timeout)    
	    return result   
	except Exception as e:
	    print(f"Exception occurred: {e}")	
	    
def API_GetDI(handle,num):   
	sdk.API_GetDI.argtypes = [JTRHD,ctypes.c_int, ctypes.POINTER(IoStatus)]
	sdk.API_GetDI.restype = BOOL 
	io_status = IoStatus()
	try:
	    result = sdk.API_GetDI(handle,num,ctypes.byref(io_status))    
	    return result,io_status   
	except Exception as e:
	    print(f"Exception occurred: {e}")	 
	    
def API_GetDO(handle,num):   
	sdk.API_GetDO.argtypes = [JTRHD,ctypes.c_int, ctypes.POINTER(IoStatus)]
	sdk.API_GetDO.restype = BOOL 
	io_status = IoStatus()
	try:
	    result = sdk.API_GetDO(handle,num,ctypes.byref(io_status))    
	    return result,io_status   
	except Exception as e:
	    print(f"Exception occurred: {e}")	 
	    
def API_GetAllDI(handle):   
	sdk.API_GetAllDI.argtypes = [JTRHD,ctypes.POINTER(AllIoStatus)]
	sdk.API_GetAllDI.restype = BOOL 
	all_di_status = AllIoStatus()
	try:
	    result = sdk.API_GetAllDI(handle,ctypes.byref(all_di_status))    
	    return result,all_di_status   
	except Exception as e:
	    print(f"Exception occurred: {e}")	
	    
def API_GetAllDO(handle):   
	sdk.API_GetAllDO.argtypes = [JTRHD,ctypes.POINTER(AllIoStatus)]
	sdk.API_GetAllDO.restype = BOOL 
	all_do_status = AllIoStatus()
	try:
	    result = sdk.API_GetAllDO(handle,ctypes.byref(all_do_status))    
	    return result,all_do_status   
	except Exception as e:
	    print(f"Exception occurred: {e}")	  
	    
def API_SetDO(handle,num,status):   
	sdk.API_SetDO.argtypes = [JTRHD,ctypes.c_int,IoStatus]
	sdk.API_SetDO.restype = BOOL 
	try:
	    result = sdk.API_SetDO(handle,num,status)    
	    return result   
	except Exception as e:
	    print(f"Exception occurred: {e}")	 
	    
def API_SetAO(handle,num,value):   
	sdk.API_SetAO.argtypes = [JTRHD,ctypes.c_int,ctypes.c_float]
	sdk.API_SetAO.restype = BOOL 
	try:
	    result = sdk.API_SetAO(handle,num,value)    
	    return result   
	except Exception as e:
	    print(f"Exception occurred: {e}")	  
	    
def API_GetRobotStatus(handle):   
	sdk.API_GetRobotStatus.argtypes = [JTRHD,ctypes.POINTER(RobotStatus)]
	sdk.API_GetRobotStatus.restype = BOOL 
	robot_status = RobotStatus()
	try:
	    result = sdk.API_GetRobotStatus(handle,ctypes.byref(robot_status))    
	    return result,robot_status   
	except Exception as e:
	    print(f"Exception occurred: {e}")	    
	    
def API_GetRobotJointRad(handle):   
	sdk.API_GetRobotJointRad.argtypes = [JTRHD,ctypes.POINTER(JointRad)]
	sdk.API_GetRobotJointRad.restype = BOOL 
	joint_rad = JointRad()
	try:
	    result = sdk.API_GetRobotJointRad(handle,ctypes.byref(joint_rad))    
	    return result,joint_rad   
	except Exception as e:
	    print(f"Exception occurred: {e}")	 
	    
def API_GetRobotJointAngle(handle):   
	sdk.API_GetRobotJointAngle.argtypes = [JTRHD,ctypes.POINTER(JointAngle)]
	sdk.API_GetRobotJointAngle.restype = BOOL 
	joint_angle = JointAngle()
	try:
	    result = sdk.API_GetRobotJointAngle(handle,ctypes.byref(joint_angle))    
	    return result,joint_angle   
	except Exception as e:
	    print(f"Exception occurred: {e}") 
	    
def API_GetRobotTcpPosition(handle):   
	sdk.API_GetRobotTcpPosition.argtypes = [JTRHD,ctypes.POINTER(TcpPosition)]
	sdk.API_GetRobotTcpPosition.restype = BOOL 
	tcp_position = TcpPosition()
	try:
	    result = sdk.API_GetRobotTcpPosition(handle,ctypes.byref(tcp_position))    
	    return result,tcp_position   
	except Exception as e:
	    print(f"Exception occurred: {e}")	 
	    
def API_GetJointArriveStatus(handle,joint_rad):   
	sdk.API_GetJointArriveStatus.argtypes = [JTRHD,ctypes.POINTER(ArriveStatus),JointRad]
	sdk.API_GetJointArriveStatus.restype = BOOL 
	arrive_status = ArriveStatus()
	try:
	    result = sdk.API_GetJointArriveStatus(handle,ctypes.byref(arrive_status),joint_rad)    
	    return result,arrive_status   
	except Exception as e:
	    print(f"Exception occurred: {e}")	
	    
def API_GetTcpArriveStatus(handle,tcp_position):   
	sdk.API_GetTcpArriveStatus.argtypes = [JTRHD,ctypes.POINTER(ArriveStatus),TcpPosition]
	sdk.API_GetTcpArriveStatus.restype = BOOL 
	arrive_status = ArriveStatus()
	try:
	    result = sdk.API_GetTcpArriveStatus(handle,ctypes.byref(arrive_status),tcp_position)    
	    return result,arrive_status   
	except Exception as e:
	    print(f"Exception occurred: {e}")	
	    
def API_GetRunSpeed(handle):   
	sdk.API_GetRunSpeed.argtypes = [JTRHD,ctypes.POINTER(ctypes.c_int)]
	sdk.API_GetRunSpeed.restype = BOOL 
	speed = ctypes.c_int()
	try:
	    result = sdk.API_GetRunSpeed(handle,ctypes.byref(speed))    
	    return result,speed   
	except Exception as e:
	    print(f"Exception occurred: {e}")              
	         
def API_SetRunSpeed(handle,speed):   
	sdk.API_SetRunSpeed.argtypes = [JTRHD,ctypes.c_int]
	sdk.API_SetRunSpeed.restype = BOOL 
	try:
	    result = sdk.API_SetRunSpeed(handle,speed)    
	    return result   
	except Exception as e:
	    print(f"Exception occurred: {e}") 	   
	    
def API_ExecuteScript(handle,script_content):
	sdk.API_ExecuteScript.argtypes = [JTRHD,ctypes.c_char_p]
	sdk.API_ExecuteScript.restype = BOOL
	try:
	    result = sdk.API_ExecuteScript(handle,script_content)    
	    return result   
	except Exception as e:
	    print(f"Exception occurred: {e}")	 
	    
def API_GetVariableValue(handle,var_name):
	sdk.API_GetVariableValue.argtypes = [JTRHD,ctypes.c_char_p,ctypes.POINTER(VariableValue)]
	sdk.API_GetVariableValue.restype = BOOL
	value = VariableValue()
	try:
	    result = sdk.API_GetVariableValue(handle,var_name,ctypes.byref(value))    
	    return result,value   
	except Exception as e:
	    print(f"Exception occurred: {e}")			    
              	         
def API_SetOffset(handle,offset):   
	sdk.API_SetOffset.argtypes = [JTRHD,TrajectoryOffset]
	sdk.API_SetOffset.restype = BOOL 
	try:
	    result = sdk.API_SetOffset(handle,offset)    
	    return result   
	except Exception as e:
	    print(f"Exception occurred: {e}") 	
	    
def API_GetOffset(handle):   
	sdk.API_GetOffset.argtypes = [JTRHD,ctypes.POINTER(TrajectoryOffset)]
	sdk.API_GetOffset.restype = BOOL 
	offset = TrajectoryOffset()
	try:
	    result = sdk.API_GetOffset(handle,ctypes.byref(offset))    
	    return result,offset   
	except Exception as e:
	    print(f"Exception occurred: {e}")	        
                 	            	                     	            
def API_SendFile(handle,local_absolute_path_file_name,save_path,save_file_name):
	sdk.API_SendFile.argtypes = [JTRHD,ctypes.c_char_p,ctypes.c_char_p,ctypes.c_char_p]
	sdk.API_SendFile.restype = BOOL
	try:
	    result = sdk.API_SendFile(handle,local_absolute_path_file_name,save_path,save_file_name)    
	    return result   
	except Exception as e:
	    print(f"Exception occurred: {e}")	   
	    
def API_ExecuteFile(handle,remote_absolute_path_file_name):
	sdk.API_ExecuteFile.argtypes = [JTRHD,ctypes.c_char_p]
	sdk.API_ExecuteFile.restype = BOOL
	try:
	    result = sdk.API_ExecuteFile(handle,remote_absolute_path_file_name)    
	    return result   
	except Exception as e:
	    print(f"Exception occurred: {e}")	
	    
def API_GetCollisionLevel(handle):   
	sdk.API_GetCollisionLevel.argtypes = [JTRHD,ctypes.POINTER(CollisionLevel)]
	sdk.API_GetCollisionLevel.restype = BOOL 
	collision_level = CollisionLevel()
	try:
	    result = sdk.API_GetCollisionLevel(handle,ctypes.byref(collision_level))    
	    return result,collision_level   
	except Exception as e:
	    print(f"Exception occurred: {e}")              
	         
def API_SetCollisionLevel(handle,level):   
	sdk.API_SetCollisionLevel.argtypes = [JTRHD,CollisionLevel]
	sdk.API_SetCollisionLevel.restype = BOOL 
	try:
	    result = sdk.API_SetCollisionLevel(handle,level)    
	    return result   
	except Exception as e:
	    print(f"Exception occurred: {e}") 	    
	    
def API_OpenSerialPort(handle,param):   
	sdk.API_OpenSerialPort.argtypes = [JTRHD,ctypes.POINTER(UART_Params)]
	sdk.API_OpenSerialPort.restype = BOOL 
	try:
	    result = sdk.API_OpenSerialPort(handle,ctypes.byref(param))    
	    return result   
	except Exception as e:
	    print(f"Exception occurred: {e}") 	 
	    
def API_SendRtuCmd(handle,req,rsp,timeout):   
	sdk.API_SendRtuCmd.argtypes = [JTRHD,ctypes.POINTER(ModbusRTU_Frame),ctypes.POINTER(ModbusRTU_Frame),ctypes.c_int]
	sdk.API_SendRtuCmd.restype = BOOL 
	try:
	    result = sdk.API_SendRtuCmd(handle,ctypes.byref(req),ctypes.byref(rsp),timeout)    
	    return result   
	except Exception as e:
	    print(f"Exception occurred: {e}") 	
	    
def API_ModbusRtuRW(handle,req,rsp,timeout):   
	sdk.API_ModbusRtuRW.argtypes = [JTRHD,ctypes.POINTER(ModbusRTU_Request),ctypes.POINTER(ModbusRTU_Frame),ctypes.c_int]
	sdk.API_ModbusRtuRW.restype = BOOL 
	try:
	    result = sdk.API_ModbusRtuRW(handle,ctypes.byref(req),ctypes.byref(rsp),timeout)    
	    return result   
	except Exception as e:
	    print(f"Exception occurred: {e}") 	    
	    
def API_CloseSerialPort(handle):   
	sdk.API_CloseSerialPort.argtypes = [JTRHD]
	sdk.API_CloseSerialPort.restype = BOOL 
	try:
	    result = sdk.API_CloseSerialPort(handle)    
	    return result   
	except Exception as e:
	    print(f"Exception occurred: {e}") 		  
	    
def API_TcpPositionCalibration(handle,points):
	sdk.API_TcpPositionCalibration.argtypes = [JTRHD,ctypes.c_char_p]
	sdk.API_TcpPositionCalibration.restype = BOOL
	try:
	    result = sdk.API_TcpPositionCalibration(handle,points)    
	    return result   
	except Exception as e:
	    print(f"Exception occurred: {e}")	  
	    
def API_TcpDirectionCalibration(handle,points):
	sdk.API_TcpDirectionCalibration.argtypes = [JTRHD,ctypes.c_char_p]
	sdk.API_TcpDirectionCalibration.restype = BOOL
	try:
	    result = sdk.API_TcpDirectionCalibration(handle,points)    
	    return result   
	except Exception as e:
	    print(f"Exception occurred: {e}")	  
	    
def API_GetDragButtonStatus(handle):   
	sdk.API_GetDragButtonStatus.argtypes = [JTRHD,ctypes.POINTER(ToolButtonStatus)]
	sdk.API_GetDragButtonStatus.restype = BOOL 
	status = ToolButtonStatus()
	try:
	    result = sdk.API_GetDragButtonStatus(handle,ctypes.byref(status))    
	    return result,status   
	except Exception as e:
	    print(f"Exception occurred: {e}")		
	    
def API_GetPointSetButtonStatus(handle):   
	sdk.API_GetPointSetButtonStatus.argtypes = [JTRHD,ctypes.POINTER(ToolButtonStatus)]
	sdk.API_GetPointSetButtonStatus.restype = BOOL 
	status = ToolButtonStatus()
	try:
	    result = sdk.API_GetPointSetButtonStatus(handle,ctypes.byref(status))    
	    return result,status   
	except Exception as e:
	    print(f"Exception occurred: {e}")	    
	    
def API_GetRobotErrorCode(handle):   
	sdk.API_GetRobotErrorCode.argtypes = [JTRHD,ctypes.POINTER(ctypes.c_int)]
	sdk.API_GetRobotErrorCode.restype = BOOL 
	error_code = ctypes.c_int()
	try:
	    result = sdk.API_GetRobotErrorCode(handle,ctypes.byref(error_code))    
	    return result,error_code   
	except Exception as e:
	    print(f"Exception occurred: {e}")  	 
	    
def API_InverseKin(handle,tcp_pose,ref_joint_rad):   
	sdk.API_InverseKin.argtypes = [JTRHD,ctypes.POINTER(TcpPosition),ctypes.POINTER(JointRad),ctypes.POINTER(JointRad)]
	sdk.API_InverseKin.restype = BOOL 
	joint_rad = JointRad()
	try:
	    result = sdk.API_InverseKin(handle,ctypes.byref(tcp_pose),ctypes.byref(ref_joint_rad),ctypes.byref(joint_rad))    
	    return result,joint_rad   
	except Exception as e:
	    print(f"Exception occurred: {e}") 	
	    
def API_ForwardKin(handle,joint_rad):   
	sdk.API_ForwardKin.argtypes = [JTRHD,ctypes.POINTER(JointRad),ctypes.POINTER(TcpPosition)]
	sdk.API_ForwardKin.restype = BOOL 
	tcp_pose = TcpPosition()
	try:
	    result = sdk.API_ForwardKin(handle,ctypes.byref(joint_rad),ctypes.byref(tcp_pose))    
	    return result,tcp_pose   
	except Exception as e:
	    print(f"Exception occurred: {e}") 
	    
def API_PointDist(handle,p_from,p_to):   
	sdk.API_PointDist.argtypes = [JTRHD,ctypes.POINTER(TcpPosition),ctypes.POINTER(TcpPosition),ctypes.POINTER(ctypes.c_float)]
	sdk.API_PointDist.restype = BOOL 
	distance = ctypes.c_float()
	try:
	    result = sdk.API_PointDist(handle,ctypes.byref(p_from),ctypes.byref(p_to),ctypes.byref(distance))    
	    return result,distance   
	except Exception as e:
	    print(f"Exception occurred: {e}") 
	    
def API_PoseAdd(handle,p_from,p_to):   
	sdk.API_InverseKin.argtypes = [JTRHD,ctypes.POINTER(TcpPosition),ctypes.POINTER(TcpPosition),ctypes.POINTER(TcpPosition)]
	sdk.API_InverseKin.restype = BOOL 
	tcp_position = TcpPosition()
	try:
	    result = sdk.API_InverseKin(handle,ctypes.byref(p_from),ctypes.byref(p_to),ctypes.byref(tcp_position))    
	    return result,tcp_position   
	except Exception as e:
	    print(f"Exception occurred: {e}") 	  
	    
def API_PoseInv(handle,p_from):   
	sdk.API_PoseInv.argtypes = [JTRHD,ctypes.POINTER(TcpPosition),ctypes.POINTER(TcpPosition)]
	sdk.API_PoseInv.restype = BOOL 
	tcp_position = TcpPosition()
	try:
	    result = sdk.API_PoseInv(handle,ctypes.byref(p_from),ctypes.byref(tcp_position))    
	    return result,tcp_position   
	except Exception as e:
	    print(f"Exception occurred: {e}") 	
	    
def API_PoseSub(handle,p_to,p_from):   
	sdk.API_PoseSub.argtypes = [JTRHD,ctypes.POINTER(TcpPosition),ctypes.POINTER(TcpPosition),ctypes.POINTER(TcpPosition)]
	sdk.API_PoseSub.restype = BOOL 
	tcp_position = TcpPosition()
	try:
	    result = sdk.API_PoseSub(handle,ctypes.byref(p_to),ctypes.byref(p_from),ctypes.byref(tcp_position))    
	    return result,tcp_position   
	except Exception as e:
	    print(f"Exception occurred: {e}")	 
	    
def API_PoseTrans(handle,p_from,p_from_to):   
	sdk.API_PoseTrans.argtypes = [JTRHD,ctypes.POINTER(TcpPosition),ctypes.POINTER(TcpPosition),ctypes.POINTER(TcpPosition)]
	sdk.API_PoseTrans.restype = BOOL 
	tcp_position = TcpPosition()
	try:
	    result = sdk.API_PoseTrans(handle,ctypes.byref(p_from),ctypes.byref(p_from_to),ctypes.byref(tcp_position))    
	    return result,tcp_position   
	except Exception as e:
	    print(f"Exception occurred: {e}") 	 
	    
def API_Weavep(handle,parameter):   
	sdk.API_Weavep.argtypes = [JTRHD,ctypes.POINTER(WeavepParam)]
	sdk.API_Weavep.restype = BOOL 
	try:
	    result = sdk.API_Weavep(handle,ctypes.byref(parameter))    
	    return result   
	except Exception as e:
	    print(f"Exception occurred: {e}")	  
	    
def API_Weavec(handle,parameter):   
	sdk.API_Weavec.argtypes = [JTRHD,ctypes.POINTER(WeavecParam)]
	sdk.API_Weavec.restype = BOOL 
	try:
	    result = sdk.API_Weavec(handle,ctypes.byref(parameter))    
	    return result   
	except Exception as e:
	    print(f"Exception occurred: {e}")	   
	    
def API_ExtAxisMovej(handle,parameter):   
	sdk.API_ExtAxisMovej.argtypes = [JTRHD,ctypes.POINTER(ExtAxisMovejParam)]
	sdk.API_ExtAxisMovej.restype = BOOL 
	try:
	    result = sdk.API_ExtAxisMovej(handle,ctypes.byref(parameter))    
	    return result   
	except Exception as e:
	    print(f"Exception occurred: {e}")	 
	    
def API_ExtAxisMovepc(handle,parameter):   
	sdk.API_ExtAxisMovepc.argtypes = [JTRHD,ctypes.POINTER(ExtAxisMovepcParam)]
	sdk.API_ExtAxisMovepc.restype = BOOL 
	try:
	    result = sdk.API_ExtAxisMovepc(handle,ctypes.byref(parameter))    
	    return result   
	except Exception as e:
	    print(f"Exception occurred: {e}")		
	    
def API_GetRobotHomeJointRad(handle):   
	sdk.API_GetRobotHomeJointRad.argtypes = [JTRHD,ctypes.POINTER(JointRad)]
	sdk.API_GetRobotHomeJointRad.restype = BOOL 
	joint_rad = JointRad()
	try:
	    result = sdk.API_GetRobotHomeJointRad(handle,ctypes.byref(joint_rad))    
	    return result,joint_rad   
	except Exception as e:
	    print(f"Exception occurred: {e}")		 
	    
def API_ResetRobotError(handle):   
	sdk.API_ResetRobotError.argtypes = [JTRHD]
	sdk.API_ResetRobotError.restype = BOOL 
	try:
	    result = sdk.API_ResetRobotError(handle)    
	    return result   
	except Exception as e:
	    print(f"Exception occurred: {e}")	      
	    
def API_GetRobotRunTime(handle):   
	sdk.API_GetRobotRunTime.argtypes = [JTRHD,ctypes.POINTER(ctypes.c_long)]
	sdk.API_GetRobotRunTime.restype = BOOL 
	run_time = ctypes.c_long()
	try:
	    result = sdk.API_GetRobotRunTime(handle,ctypes.byref(run_time))    
	    return result,run_time   
	except Exception as e:
	    print(f"Exception occurred: {e}") 	 
	    
def API_GetPowerOffDelayTime(handle):   
	sdk.API_GetPowerOffDelayTime.argtypes = [JTRHD,ctypes.POINTER(ctypes.c_int)]
	sdk.API_GetPowerOffDelayTime.restype = BOOL 
	delay_time = ctypes.c_int()
	try:
	    result = sdk.API_GetPowerOffDelayTime(handle,ctypes.byref(delay_time))    
	    return result,delay_time   
	except Exception as e:
	    print(f"Exception occurred: {e}") 
	    
def API_EmergencyStop(handle):   
	sdk.API_EmergencyStop.argtypes = [JTRHD]
	sdk.API_EmergencyStop.restype = BOOL 
	try:
	    result = sdk.API_EmergencyStop(handle)    
	    return result   
	except Exception as e:
	    print(f"Exception occurred: {e}")	
	    
def API_ClearUnfinishedTrajectory(handle):   
	sdk.API_ClearUnfinishedTrajectory.argtypes = [JTRHD]
	sdk.API_ClearUnfinishedTrajectory.restype = BOOL 
	try:
	    result = sdk.API_ClearUnfinishedTrajectory(handle)    
	    return result   
	except Exception as e:
	    print(f"Exception occurred: {e}")	  
	    
def API_GetPointsInProgram(handle,program_file_name):   
	sdk.API_GetPointsInProgram.argtypes = [JTRHD,ctypes.c_char_p,ctypes.POINTER(PointsInProgram)]
	sdk.API_GetPointsInProgram.restype = BOOL
	points_info = PointsInProgram()  
	try:
	    result = sdk.API_GetPointsInProgram(handle,program_file_name,ctypes.byref(points_info))    
	    return result,points_info   
	except Exception as e:
	    print(f"Exception occurred: {e}")	
	    
def API_GetFirmwareVersion(handle):
	sdk.API_GetFirmwareVersion.argtypes = [JTRHD,ctypes.POINTER(VersionInfo)]
	sdk.API_GetFirmwareVersion.restype = BOOL
	firmware_version = VersionInfo()
	try:
	    result = sdk.API_GetFirmwareVersion(handle,ctypes.byref(firmware_version))    
	    return result,firmware_version   
	except Exception as e:
	    print(f"Exception occurred: {e}")	
	    
def API_SetMountedPose(handle,mounted_pose):   
	sdk.API_SetMountedPose.argtypes = [JTRHD,ctypes.c_int]
	sdk.API_SetMountedPose.restype = BOOL 
	try:
	    result = sdk.API_SetMountedPose(handle,mounted_pose)    
	    return result   
	except Exception as e:
	    print(f"Exception occurred: {e}") 	  

	    
def API_SetMountedAngle(handle,tiltAngle,baseRotationAngle):   
	sdk.API_SetMountedAngle.argtypes = [JTRHD,ctypes.c_float,ctypes.c_float]
	sdk.API_SetMountedAngle.restype = BOOL  
	try:
	    result = sdk.API_SetMountedAngle(handle,tiltAngle,baseRotationAngle)    
	    return result   
	except Exception as e:
	    print(f"Exception occurred: {e}")	 	    
	      	    	    	      	    	                              	    
def API_ModbusRtuRWEndTool(handle,req,rsp,timeout):   
	sdk.API_ModbusRtuRWEndTool.argtypes = [JTRHD,ctypes.POINTER(ModbusRTU_Request),ctypes.POINTER(ModbusRTU_Frame),ctypes.c_int]
	sdk.API_ModbusRtuRWEndTool.restype = BOOL 
	try:
	    result = sdk.API_ModbusRtuRWEndTool(handle,ctypes.byref(req),ctypes.byref(rsp),timeout)    
	    return result   
	except Exception as e:
	    print(f"Exception occurred: {e}") 	    	                     	       	             
