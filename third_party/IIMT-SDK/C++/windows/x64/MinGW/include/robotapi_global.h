#ifndef ROBOTAPI_GLOBAL_H
#define ROBOTAPI_GLOBAL_H

//#include <QtCore/qglobal.h>

#ifdef _WIN32
    #if defined(ROBOTAPI_LIBRARY)
    #  define ROBOT_API_EXPORT extern "C" __declspec(dllexport)
    #else
    #  define ROBOT_API_EXPORT extern "C" __declspec(dllimport)
    #endif
#else
    #if defined(ROBOTAPI_LIBRARY)
    #  define ROBOT_API_EXPORT extern "C" __attribute__((visibility("default")))
    #else
    #  define ROBOT_API_EXPORT extern "C" __attribute__((visibility("default")))
    #endif
#endif
#ifndef BOOL
typedef int BOOL;
#endif
#ifndef    TRUE
#define    TRUE	1
#endif
#ifndef    FALSE
#define	   FALSE 0
#endif
#ifndef    NULL
#define	   NULL 0
#endif

#ifndef    ROBOT_MESSAGE_PACKAGE_SIZE
#define	   ROBOT_MESSAGE_PACKAGE_SIZE   868
#endif

#ifdef _WIN32
typedef long long JTRHD;
#else
typedef long JTRHD;
#endif

#pragma pack(1)
typedef struct {
    int  length;             //数据长度　        　　　4
    double target_pos[6];      //目标位姿　　　　　　6*8=48
    double target_v[6];        //目标速度　　　　　　6*8=48
    double target_acc[6];      //目标加速度　　　　　6*8=48
    double target_l[6];        //目标电流值　　　　　6*8=48
    double target_m[6];        //目标力矩　　　　　　6*8=48
    double actual_pos[6];      //当前位姿　　　　　　6*8=48
    double actual_v[6];        //当前速度　　　　　　6*8=48
    double actual_l[6];        //当前电流值　　　　　6*8=48
    double tool_x;             //工具末端-x        　　　8
    double tool_y;             //工具末端-y        　　　8
    double tool_z;             //工具末端-z        　　　8
    double tool_rx;            //工具末端-rx            8
    double tool_ry;            //工具末端-ry            8
    double tool_rz;            //工具末端-rz            8
    double tcp_force[6];       //工具力　　　　　　　6*8=48
    double tool_v[6];          //工具线速度　　　　　6*8=48
    double tcp_speed[6];       //工具坐标系速度矢量　6*8=48
    double DI_status;          //io状态                8
    double tool_io;            //末端io                8
    double motor_temp[6];      //电机温度　　　　　　6*8=48
    double Controller_time;    //控制周期　　　　　　　　　8
    double robot_mode;         //机器人模式　　　　　　　　8
    double join_mode[6];       //关节模式　　　　　　6*8=48
    double run_time;           //程序运行时间　　　　　　　8
    double robot_status;       //机器人状态　　　　　　　　8
    double reserved[16];       //保留字段　　　　　16*8=128
    double IsArriving;         //达位状态(运动１,停止0)　 8
    double heartbit;           //心跳　　　　　　　　　　　8
}RobotMessage;  //4+13*48+14*8+128=868

typedef struct
{
    double q[6];
    float a;
    float v;
    float t;
    float lookahead_time;
    float gain;
}ServojParam;

typedef struct
{
    double p[6];
    float a;
    float v;
    float t;
    float lookahead_time;
}ServocParam;

typedef struct
{
    double q[6];   //目标点关节参数,格式为 {0.0,1.57,0.0,-1.57,-1.57,0} ,单位 rad
    float v;       //关节速度,rad/s
    float a;       //关节加速度,rad/s^2
    float j;       //关节加加速度,rad/s^3
    float r;       //轨迹交融半径,mm
    float t;       //轨迹规划时间,系统保留参数接口,可不写
}MovejParam;

typedef struct
{
    double p[6];      //tcp参数,x,y,z 单位为m,rx,ry,rz单位为rad
    float v;          //速度
    float tool_v;     //工具速度
    float tool_a;     //工具加速度
    float r;          //交融半径,mm
}MovelParam;

typedef struct
{
    double passing_point[6];      //经过点,tcp参数，tcp参数,x,y,z 单位为m,rx,ry,rz单位为rad
    double end_point[6];      //结束点,tcp参数，tcp参数,x,y,z 单位为m,rx,ry,rz单位为rad
    float tool_v;     //工具速度
    float tool_a;     //工具加速度
    int circle;       //圆或圆弧 1:整圆 0:圆弧
    int count;        //圆次数
    float r;          //交融半径,mm
    int mode;         //模式 1:固定 0:无约束
    float reserve;    //保留字段
}MovepcParam;

typedef struct
{
    double  robotAngle[6];       //关节角度值
}JointAngle;

typedef struct
{
    double  robotRad[6];         //关节弧度值
}JointRad;

typedef struct
{
    double  robotTcp[6];         //机械臂末端位置姿态，x,y,z 单位为m,rx,ry,rz单位为rad
}TcpPosition;

typedef enum
{
    ROBOT_STATUS_UNKNOW=-1,
    ROBOT_POWEROFF=0, //0
    ROBOT_POWEROFF_2_POWERON,//1
    ROBOT_POWERON,//2
    ROBOT_POWERON_2_STANBY,//3
    ROBOT_STANDBY,//4
    ROBOT_STANDBY_2_MAUNTEACH,//5
    ROBOT_MAUNTEACH,//6
    ROBOT_MANUTEACH_2_MANUTEACHEND,//7
    ROBOT_MAUNTEACH_END,//8
    ROBOT_SINGLETARGETMOVE,//9
    ROBOT_PAUSE,
    ROBOT_STANBY_2_AUTORUN,//11
    ROBOT_AUTORUN,//---12
    ROBOT_FREEDRIVE,//13
    ROBOT_FREEDRIVE_END,//14
    ROBOT_STANDBY_2_RUNTARGET,//15
    ROBOT_RUNTARGET,//16
    ROBOT_STOP,//17
    ROBOT_EMERGENCY,//18
    ROBOT_ERROR,//19
    ROBOT_LOCAL_REMOTE,//20
    ROBOT_COLLISION,
}RobotStatus;

typedef  enum
{
    IO_STATUS_LOW = 0,
    IO_STATUS_HIGH
}IoStatus;

typedef enum
{
    ACTION_CLOSE = 0,
    ACTION_OPEN
}GripperAction;

typedef struct
{
    IoStatus  IoInfo[16];
}AllIoStatus;

typedef  enum
{
    ARRIVE_STATUS_ARRIVED = 0,
    ARRIVE_STATUS_NOT_ARRIVED,
    ARRIVE_STATUS_ERROR
}ArriveStatus;

typedef struct
{
    char description[64];
}ControllerVersion;

typedef struct
{
    char description[64];
}VersionInfo;

typedef struct
{
    char description[32];
}RobotModel;

typedef struct
{
    char description[32];
}SerialNumber;

typedef struct
{
    char description[32];
}RobotMode;

typedef struct
{
    char description[128];
}LoadedProgram;

typedef struct
{
    char description[128];
}LoadInstallation;

typedef struct
{
    char description[32];
}SafetyStatus;

typedef struct
{
    char description[32];
}ProgramRunning;

typedef struct
{
    char description[32];
}ProgramState;

typedef struct
{
    char description[32];
}ProgramSaved;

typedef struct
{
    char description[32];
}InRemoteControl;

typedef struct
{
    char description[32];
}OperationalMode;

typedef struct
{
    char description[32];
}UserRole;

typedef struct
{
    char version[32];         //版本信息
}SDK_Info;

typedef struct
{
    char description[512];
}ErrorInfo;

typedef struct
{
    char ip[32];
}ControllerIPv4;

typedef struct
{
    char ip[128];
}ControllerIPv6;

enum IIMT_BaudRate {
    Baud1200 = 1200,
    Baud2400 = 2400,
    Baud4800 = 4800,
    Baud9600 = 9600,
    Baud19200 = 19200,
    Baud38400 = 38400,
    Baud57600 = 57600,
    Baud115200 = 115200,
    UnknownBaud = -1
};

enum IIMT_DataBits {
    Data5 = 5,
    Data6 = 6,
    Data7 = 7,
    Data8 = 8,
    UnknownDataBits = -1
};

enum IIMT_Parity {
    NoParity = 0,
    EvenParity = 2,
    OddParity = 3,
    SpaceParity = 4,
    MarkParity = 5,
    UnknownParity = -1
};

enum IIMT_StopBits {
    OneStop = 1,
    OneAndHalfStop = 3,
    TwoStop = 2,
    UnknownStopBits = -1
};

enum IIMT_FlowControl {
    NoFlowControl,
    HardwareControl,
    SoftwareControl,
    UnknownFlowControl = -1
};

typedef struct   //串口参数结构体
{
    char SerialPortName[32];//串口名
    IIMT_BaudRate BaudRate; //波特率
    IIMT_DataBits DataBits; //数据位
    IIMT_Parity Parity;     //校验位
    IIMT_StopBits StopBits; //停止位
}UART_Params;

// Modbus RTU 报文帧（请求、响应通用）
typedef struct {
    unsigned char data[256];  // 报文数据（最大255字节）二进制数据，每个字节范围 0x00-0xFF
    unsigned short data_len;       // 实际报文长度,二进制数据的实际字节数
} ModbusRTU_Frame;

typedef struct
{
    unsigned char   slave_addr;     // 从站地址
    unsigned char   func_code;      // 功能码
    unsigned short  start_addr;     // 起始地址
    unsigned short  data_number;    // 数据数量（寄存器/线圈数量）
    unsigned char   data[250];      // 写入的数据
    unsigned char   data_len;       // 数据的实际字节长度
}ModbusRTU_Request;

typedef struct
{
    double x_offset;             //m
    double y_offset;             //m
    double z_offset;             //m
    double rx_offset;            //rad
    double ry_offset;            //rad
    double rz_offset;            //rad
}TrajectoryOffset;

typedef  enum
{
    COLLISION_LEVEL_ZERO = 0,
    COLLISION_LEVEL_ONE,
    COLLISION_LEVEL_TWO,
    COLLISION_LEVEL_THREE,
    COLLISION_LEVEL_FOUR,
    COLLISION_LEVEL_FIVE,
}CollisionLevel;

typedef  enum
{
    BUTTON_STATUS_ERROR = -1,    //状态不可用，比如机器人未上电释放抱闸
    BUTTON_STATUS_PRESS_DOWN = 0,//代表按钮按下
    BUTTON_STATUS_RELEASE        //代表按钮松开
}ToolButtonStatus;

typedef enum
{
    TRIANGLE_SWING =0,         //三角形
    CRESCENT_SWING,            //月牙形
    TRAPEZOID_SWING,           //梯形
    FORWARD_SPIN_SWING,        //正旋
    CLOCKWISE_CORKSCREW_SPIN_SWING,          //顺时针螺旋
    ANTICLOCKWISE_CORKSCREW_SPIN_SWING,      //逆时针螺旋
    L_TRIANGLE_SWING,                        //L三角
    L_FORWARD_SPIN_SWING                     //L正旋
}WeaveType;

typedef struct
{
    double target_point[6];      //目标点，tcp参数,x,y,z 单位为m,rx,ry,rz单位为rad
    float tool_v;     //工具速度
    float tool_a;     //工具加速度
    float r;          //交融半径,mm
    WeaveType   type;   //摆动类型
    float frequency;      //摆动频率,hz
    float range;          //摆动幅度,m
    int left_stay_time;   //单位 秒(s)
    int right_stay_time;  //单位 秒(s)
    double reserve1;      //保留参数1
    double reserve2;      //保留参数2
    int reserve3;         //保留参数3
    int reserve4;         //保留参数4
}WeavepParam;

typedef struct
{
    double passing_point[6];      //过渡点，tcp参数,x,y,z 单位为m,rx,ry,rz单位为rad
    double target_point[6];      //目标点，tcp参数,x,y,z 单位为m,rx,ry,rz单位为rad
    float tool_v;     //工具速度
    float tool_a;     //工具加速度
    float r;          //交融半径,mm
    int full_circle;  //0:弧拼接  1:整圆
    WeaveType   type;   //摆动类型
    float frequency;      //摆动频率,hz
    float range;          //摆动幅度,m
    int left_stay_time;   //单位 秒(s)
    int right_stay_time;  //单位 秒(s)
    double reserve1;      //保留参数1
    double reserve2;      //保留参数2
    int reserve3;         //保留参数3
    int reserve4;         //保留参数4
}WeavecParam;


typedef struct
{
    double p[6];   //目标点关节参数,格式为 {0.0,1.57,0.0,-1.57,-1.57,0} ,单位 rad
    double p_axis[4]; //扩展轴要设置的位置，分别对应1,2,3,4.大于4×PI=4×3.1415926表示不启动;
    float v;       //关节速度,rad/s
    float a;       //关节加速度,rad/s^2
    float j;       //关节加加速度,rad/s^3
    float r;       //轨迹交融半径,mm
    float t;       //轨迹规划时间,系统保留参数接口,可不写
}ExtAxisMovejParam;

typedef struct
{
    double passing_point[6];      //经过点,tcp参数，tcp参数,x,y,z 单位为m,rx,ry,rz单位为rad
    double end_point[6];      //结束点,tcp参数，tcp参数,x,y,z 单位为m,rx,ry,rz单位为rad
    double p_axis[4];         //扩展轴要设置的位置，分别对应1,2,3,4.大于4×PI=4×3.1415926表示不启动;
    float tool_v;     //工具速度
    float tool_a;     //工具加速度
    int circle;       //圆或圆弧 1:整圆 0:圆弧
    int count;        //圆次数
    float r;          //交融半径,mm
    int mode;         //模式 1:固定 0:无约束
    float reserve;    //保留字段
}ExtAxisMovepcParam;

typedef struct
{
    char description[1000]; //用';'分割的多个点的工具位姿和关节弧度,最多获取8个路点,每个点格式x,y,z,rx,ry,rz joint1,joint2,joint3,joint4,joint5,joint6
}PointsInProgram;

typedef struct
{
    char description[512];
}VariableValue;

typedef enum {
    FLOOR_MOUNTED = 0,
    SIDE_MOUNTED,
    INVERTED_MOUNTED,
}MountedPose;

#pragma pack()
//回调函数类型
//Robot数据信息回调函数
typedef void(*ROBOT_DATA_CALLBACK) (char *pBuffer, unsigned int ulBufSize, unsigned long ulUserData);

#endif // ROBOTAPI_GLOBAL_H

