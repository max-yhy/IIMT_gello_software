import enum
import ctypes
import platform

#检测操作系统类型
if platform.system() ==  "Windows":
	JTRHD = ctypes.c_longlong
else:
	JTRHD = ctypes.c_long
BOOL = ctypes.c_int

class ErrorInfo(ctypes.Structure):
    _fields_ = [
        ("description", ctypes.c_char * 512),
    ]
    
class ProgramRunning(ctypes.Structure):
    _fields_ = [
        ("description", ctypes.c_char * 32),
    ]  
    
class ProgramSaved(ctypes.Structure):
    _fields_ = [
        ("description", ctypes.c_char * 32),
    ]
  
class InRemoteControl(ctypes.Structure):
    _fields_ = [
        ("description", ctypes.c_char * 32),
    ]  
  
class ControllerVersion(ctypes.Structure):
    _fields_ = [
        ("description", ctypes.c_char * 64),
    ] 
    
class VersionInfo(ctypes.Structure):
    _fields_ = [
        ("description", ctypes.c_char * 64),
    ]  
    
class RobotModel(ctypes.Structure):
    _fields_ = [
        ("description", ctypes.c_char * 32),
    ] 
    
class SerialNumber(ctypes.Structure):
    _fields_ = [
        ("description", ctypes.c_char * 32),
    ] 
    
class RobotMode(ctypes.Structure):
    _fields_ = [
        ("description", ctypes.c_char * 32),
    ] 
    
class LoadedProgram(ctypes.Structure):
    _fields_ = [
        ("description", ctypes.c_char * 128),
    ]  
    
class SafetyStatus(ctypes.Structure):
    _fields_ = [
        ("description", ctypes.c_char * 32),
    ]  
                 
class ProgramState(ctypes.Structure):
    _fields_ = [
        ("description", ctypes.c_char * 32),
    ]
    
class OperationalMode(ctypes.Structure):
    _fields_ = [
        ("description", ctypes.c_char * 32),
    ]    
  
class ServojParam(ctypes.Structure):
    _fields_ = [
        ("q",ctypes.c_double*6),
        ("a",ctypes.c_float),
        ("v",ctypes.c_float),
        ("t",ctypes.c_float),
        ("lookahead_time",ctypes.c_float),
        ("gain",ctypes.c_float)
    ] 
    
class ServocParam(ctypes.Structure):
    _fields_ = [
        ("p",ctypes.c_double*6),
        ("a",ctypes.c_float),
        ("v",ctypes.c_float),
        ("t",ctypes.c_float),
        ("lookahead_time",ctypes.c_float)
    ]     
        
class MovejParam(ctypes.Structure):
    _fields_ = [
        ("q",ctypes.c_double*6),
        ("v",ctypes.c_float),
        ("a",ctypes.c_float),
        ("j",ctypes.c_float),
        ("r",ctypes.c_float),
        ("t",ctypes.c_float)
    ] 
    
class MovelParam(ctypes.Structure):
    _fields_ = [
        ("p",ctypes.c_double*6),
        ("v",ctypes.c_float),
        ("tool_v",ctypes.c_float),
        ("tool_a",ctypes.c_float),
        ("r",ctypes.c_float),
    ] 
    
class MovepcParam(ctypes.Structure):
    _fields_ = [
        ("passing_point",ctypes.c_double*6), 
        ("end_point",ctypes.c_double*6),  
        ("tool_v",ctypes.c_float), 
        ("tool_a",ctypes.c_float), 
        ("circle",ctypes.c_int),
        ("count",ctypes.c_int), 
        ("r",ctypes.c_int),
        ("mode",ctypes.c_int),
        ("reserve",ctypes.c_float)
    ] 
       
class IoStatus(ctypes.c_int):
    IO_STATUS_LOW = 0
    IO_STATUS_HIGH = 1
  
  
class AllIoStatus(ctypes.Structure):
    _fields_ = [
        ("IoInfo", IoStatus * 16),
    ]   
    
class RobotStatus(ctypes.c_int):
    ROBOT_STATUS_UNKNOW=-1
    ROBOT_POWEROFF=0
    ROBOT_POWEROFF_2_POWERON=1
    ROBOT_POWERON=2
    ROBOT_POWERON_2_STANBY=3
    ROBOT_STANDBY=4
    ROBOT_STANDBY_2_MAUNTEACH=5
    ROBOT_MAUNTEACH=6
    ROBOT_MANUTEACH_2_MANUTEACHEND=7
    ROBOT_MAUNTEACH_END=8
    ROBOT_SINGLETARGETMOVE=9
    ROBOT_PAUSE=10
    ROBOT_STANBY_2_AUTORUN=11
    ROBOT_AUTORUN=12
    ROBOT_FREEDRIVE=13
    ROBOT_FREEDRIVE_END=14
    ROBOT_STANDBY_2_RUNTARGET=15
    ROBOT_RUNTARGET=16
    ROBOT_STOP=17
    ROBOT_EMERGENCY=18
    ROBOT_ERROR=19
    ROBOT_LOCAL_REMOTE=20
    ROBOT_COLLISION=21    
 
class JointRad(ctypes.Structure):
    _fields_ = [
        ("robotRad", ctypes.c_double * 6),
    ]
        
class JointAngle(ctypes.Structure):
    _fields_ = [
        ("robotAngle", ctypes.c_double * 6),
    ] 
     
class TcpPosition(ctypes.Structure):
    _fields_ = [
        ("robotTcp", ctypes.c_double * 6),
    ] 
    def __eq__(self, other):
        if not isinstance(other, TcpPosition):
            return False
        return all(abs(a - b) <= 1e-6 for a, b in zip(self.robotTcp, other.robotTcp)) 
      
class ArriveStatus(ctypes.c_int):
    ARRIVE_STATUS_ARRIVED = 0
    ARRIVE_STATUS_NOT_ARRIVED = 1
    ARRIVE_STATUS_ERROR = 2        
    
class TrajectoryOffset(ctypes.Structure):
    _fields_ = [
        ("x_offset",ctypes.c_double),
        ("y_offset",ctypes.c_double),
        ("z_offset",ctypes.c_double),
        ("rx_offset",ctypes.c_double),
        ("ry_offset",ctypes.c_double),
        ("rz_offset",ctypes.c_double)
    ] 
    
class CollisionLevel(ctypes.c_int):
    COLLISION_LEVEL_ZERO = 0
    COLLISION_LEVEL_ONE = 1
    COLLISION_LEVEL_TWO = 2
    COLLISION_LEVEL_THREE = 3
    COLLISION_LEVEL_FOUR = 4
    COLLISION_LEVEL_FIVE = 5   
        
class IIMT_BaudRate(ctypes.c_int):
    Baud1200 = 1200
    Baud2400 = 2400
    Baud4800 = 4800
    Baud9600 = 9600
    Baud19200 = 19200
    Baud38400 = 38400
    Baud57600 = 57600
    Baud115200 = 115200
    UnknownBaud = -1


class IIMT_DataBits(ctypes.c_int):
    Data5 = 5
    Data6 = 6
    Data7 = 7
    Data8 = 8
    UnknownDataBits = -1

class IIMT_Parity(ctypes.c_int):
    NoParity = 0
    EvenParity = 2
    OddParity = 3
    SpaceParity = 4
    MarkParity = 5
    UnknownParity = -1

class IIMT_StopBits(ctypes.c_int):
    OneStop = 1
    OneAndHalfStop = 3
    TwoStop = 2
    UnknownStopBits = -1

class IIMT_FlowControl(ctypes.c_int):
    NoFlowControl = 0
    HardwareControl = 1
    SoftwareControl = 2
    UnknownFlowControl = -1

class UART_Params(ctypes.Structure):
    _fields_ = [
        ("SerialPortName", ctypes.c_char * 32),
        ("BaudRate",IIMT_BaudRate),
        ("DataBits",IIMT_DataBits),
        ("Parity",IIMT_Parity),
        ("StopBits",IIMT_StopBits)
    ]
    
class ModbusRTU_Frame(ctypes.Structure):
	_fields_ = [
        ("data", ctypes.c_ubyte * 256),
        ("data_len", ctypes.c_ushort)
    ]

class ModbusRTU_Request(ctypes.Structure):
	_fields_ = [
        ("slave_addr", ctypes.c_ubyte),
        ("func_code", ctypes.c_ubyte),
        ("start_addr", ctypes.c_ushort),
        ("data_number", ctypes.c_ushort),
        ("data", ctypes.c_ubyte * 250),
        ("data_len", ctypes.c_ushort)
    ]
    
class ToolButtonStatus(ctypes.c_int):
    BUTTON_STATUS_ERROR = -1
    BUTTON_STATUS_PRESS_DOWN = 0
    BUTTON_STATUS_RELEASE = 1

class WeaveType(ctypes.c_int):
    TRIANGLE_SWING =0
    CRESCENT_SWING =1
    TRAPEZOID_SWING =2
    FORWARD_SPIN_SWING =3
    CLOCKWISE_CORKSCREW_SPIN_SWING =4
    ANTICLOCKWISE_CORKSCREW_SPIN_SWING =5
    L_TRIANGLE_SWING =6
    L_FORWARD_SPIN_SWING =7
    
class WeavepParam(ctypes.Structure):
	_fields_ = [
        ("target_point", ctypes.c_double * 6),
        ("tool_v",ctypes.c_float),
        ("tool_a",ctypes.c_float),
        ("r",ctypes.c_float),
        ("type",WeaveType),
        ("frequency", ctypes.c_float),
        ("range",ctypes.c_float),
        ("left_stay_time",ctypes.c_int),
        ("right_stay_time",ctypes.c_int),
        ("reserve1", ctypes.c_double),
        ("reserve2",ctypes.c_double),
        ("reserve3",ctypes.c_int),
        ("reserve4",ctypes.c_int)
    ]   
    
class WeavecParam(ctypes.Structure):
	_fields_ = [
        ("passing_point", ctypes.c_double * 6),
        ("target_point", ctypes.c_double * 6),
        ("tool_v",ctypes.c_float),
        ("tool_a",ctypes.c_float),
        ("r",ctypes.c_float),
        ("full_circle",ctypes.c_int),
        ("type",WeaveType),
        ("frequency", ctypes.c_float),
        ("range",ctypes.c_float),
        ("left_stay_time",ctypes.c_int),
        ("right_stay_time",ctypes.c_int),
        ("reserve1", ctypes.c_double),
        ("reserve2",ctypes.c_double),
        ("reserve3",ctypes.c_int),
        ("reserve4",ctypes.c_int)
    ]      
    
class ExtAxisMovejParam(ctypes.Structure):
	_fields_ = [
        ("p", ctypes.c_double * 6),
        ("p_axis", ctypes.c_double * 4),
        ("v",ctypes.c_float),
        ("a",ctypes.c_float),
        ("j",ctypes.c_float),
        ("r",ctypes.c_float),
        ("t",ctypes.c_float)
    ]

    
class ExtAxisMovepcParam(ctypes.Structure):
	_fields_ = [
        ("passing_point", ctypes.c_double * 6),
        ("end_point", ctypes.c_double * 6),
        ("p_axis", ctypes.c_double * 4),
        ("tool_v",ctypes.c_float),
        ("tool_a",ctypes.c_float),
        ("circle",ctypes.c_int),
        ("count",ctypes.c_int),
        ("r",ctypes.c_float),
        ("mode",ctypes.c_int),
        ("reserve",ctypes.c_float),
    ]    
    
class PointsInProgram(ctypes.Structure):
    _fields_ = [
        ("description", ctypes.c_char * 1000),
    ]   
    
class VariableValue(ctypes.Structure):
    _fields_ = [
        ("description", ctypes.c_char * 512),
    ]      
    
class MountedPose:
    FLOOR_MOUNTED = 0
    SIDE_MOUNTED = 1
    INVERTED_MOUNTED = 2  
