#ifndef ROBOTAPI_H
#define ROBOTAPI_H

#include "robotapi_global.h"
ROBOT_API_EXPORT void API_HelloWorld();   //测试接口

ROBOT_API_EXPORT BOOL API_Login(const char* ip, int port,JTRHD& handle);  //登录，建立连接
ROBOT_API_EXPORT BOOL API_Logout(JTRHD& handle); //注销，断开连接

ROBOT_API_EXPORT BOOL API_SetDebugMode(JTRHD handle,const BOOL is_debug);   //设置是否调试模式
ROBOT_API_EXPORT BOOL API_GetDebugMode(JTRHD handle,BOOL& is_debug);   //获取是否调试模式
ROBOT_API_EXPORT BOOL API_GetErrorInfo(JTRHD handle,ErrorInfo* info);   //获取错误信息描述

//机械臂状态指令
ROBOT_API_EXPORT BOOL API_PowerOn(JTRHD handle);  //机器人上电
ROBOT_API_EXPORT BOOL API_ReleaseBrake(JTRHD handle);  //机器人释放抱闸
ROBOT_API_EXPORT BOOL API_PowerOff(JTRHD handle);  //机器人掉电
ROBOT_API_EXPORT BOOL API_Play(JTRHD handle); //启动
ROBOT_API_EXPORT BOOL API_Stop(JTRHD handle); // 停止
ROBOT_API_EXPORT BOOL API_Pause(JTRHD handle); // 暂停

ROBOT_API_EXPORT BOOL API_LoadProgram(JTRHD handle,const char* program_file_name); //加载程序
ROBOT_API_EXPORT BOOL API_LoadInstallation(JTRHD handle,const char* installation_file_name); //加载安装配置

ROBOT_API_EXPORT BOOL API_Shutdown(JTRHD handle);//关闭控制器
ROBOT_API_EXPORT BOOL API_Running(JTRHD handle,ProgramRunning* program_running);  //运行状态查询
ROBOT_API_EXPORT BOOL API_IsProgramSaved(JTRHD handle,ProgramSaved* program_saved);//查询程序是否保存
ROBOT_API_EXPORT BOOL API_IsInRemoteControl(JTRHD handle,InRemoteControl* in_remote_control);   //查询是否为远程控制
ROBOT_API_EXPORT BOOL API_Popup(JTRHD handle,const char* popup_text);//弹框
ROBOT_API_EXPORT BOOL API_ClosePopup(JTRHD handle);//关闭弹框
ROBOT_API_EXPORT BOOL API_AddToLog(JTRHD handle,const char* log_text);//将日志消息添加到日志历史记录
ROBOT_API_EXPORT BOOL API_GetControllerVersion(JTRHD handle,ControllerVersion* controller_version);//获取机器人上安装的软件的版本信息
ROBOT_API_EXPORT BOOL API_GetVersion(JTRHD handle,VersionInfo* version);//获取版本号
ROBOT_API_EXPORT BOOL API_GetRobotModel(JTRHD handle,RobotModel* robot_model);//获取机器人型号
ROBOT_API_EXPORT BOOL API_GetSerialNumber(JTRHD handle,SerialNumber* serial_number);//获取序列号
ROBOT_API_EXPORT BOOL API_GetRobotMode(JTRHD handle,RobotMode* robot_mode);//获取机器人模式
ROBOT_API_EXPORT BOOL API_GetLoadedProgram(JTRHD handle,LoadedProgram* loaded_program);//获取哪一个程序被加载
ROBOT_API_EXPORT BOOL API_GetSafetyStatus(JTRHD handle,SafetyStatus* safety_status);//获取安全状态
ROBOT_API_EXPORT BOOL API_GetProgramState(JTRHD handle,ProgramState* program_state);//获取程序状态
ROBOT_API_EXPORT BOOL API_GetOperationalMode(JTRHD handle,OperationalMode* operational_mode);//获取操作模式
ROBOT_API_EXPORT BOOL API_SetOperationalMode(JTRHD handle,const char* operational_mode);//设置操作模式
ROBOT_API_EXPORT BOOL API_ClearOperationalMode(JTRHD handle);//清除操作模式

ROBOT_API_EXPORT BOOL API_FreeDriveMode(JTRHD handle); //自由拖动模式
ROBOT_API_EXPORT BOOL API_EndFreeDriveMode(JTRHD handle); // 结束自由拖动模式
ROBOT_API_EXPORT BOOL API_ManualTeachStart(JTRHD handle,int num,int direction,float step_size = 0.0);  //手动示教
ROBOT_API_EXPORT BOOL API_ManualTeachEnd(JTRHD handle,int num,int direction);  //结束示教
ROBOT_API_EXPORT BOOL API_Servoj(JTRHD handle,ServojParam* parameter);  //需单独配置建立链接
ROBOT_API_EXPORT BOOL API_Servoc(JTRHD handle,ServocParam* parameter);  //需单独配置建立链接
ROBOT_API_EXPORT BOOL API_Movej(JTRHD handle,MovejParam* parameter,bool is_block=true,int timeout=30);//timeout:默认值30s,is_block为true时有效
ROBOT_API_EXPORT BOOL API_Movel(JTRHD handle,MovelParam* parameter,bool is_block=true,int timeout=30);
ROBOT_API_EXPORT BOOL API_Movepc(JTRHD handle,MovepcParam* parameter,bool is_block=false,int timeout=0);

ROBOT_API_EXPORT BOOL API_GetDI(JTRHD handle,int num,IoStatus& status); //获取IO输入口状态 num:0~15
ROBOT_API_EXPORT BOOL API_GetDO(JTRHD handle,int num,IoStatus& status); //获取IO输出口状态 num:0~15
ROBOT_API_EXPORT BOOL API_GetAllDI(JTRHD handle,AllIoStatus* status); //一次获取所有IO输入口状态 num:0~15
ROBOT_API_EXPORT BOOL API_GetAllDO(JTRHD handle,AllIoStatus* status); //一次获取所有IO输出口状态 num:0~15
ROBOT_API_EXPORT BOOL API_SetDO(JTRHD handle,int num,IoStatus status); //设置IO输出口状态 num:0~15 status:0 or 1
ROBOT_API_EXPORT BOOL API_SetAO(JTRHD handle,int num,float value);
ROBOT_API_EXPORT BOOL API_GetRobotStatus(JTRHD handle,RobotStatus& status); //获取机器人状态
ROBOT_API_EXPORT BOOL API_GetRobotJointRad(JTRHD handle,JointRad* joint_rad); //获取关节弧度
ROBOT_API_EXPORT BOOL API_GetRobotJointAngle(JTRHD handle,JointAngle* joint_angle); //获取关节角度
ROBOT_API_EXPORT BOOL API_GetRobotTcpPosition(JTRHD handle,TcpPosition* position);   //获取工具位置
ROBOT_API_EXPORT BOOL API_GetJointArriveStatus(JTRHD handle,ArriveStatus& status,JointRad joint_rad); //获取关节达位状态
ROBOT_API_EXPORT BOOL API_GetTcpArriveStatus(JTRHD handle,ArriveStatus& status,TcpPosition position); //获取Tcp达位状态

ROBOT_API_EXPORT BOOL API_GetRunSpeed(JTRHD handle,int& speed); //获取运行速度
ROBOT_API_EXPORT BOOL API_SetRunSpeed(JTRHD handle,int speed);  //设置运行速度(范围 1~100)
ROBOT_API_EXPORT BOOL API_ExecuteScript(JTRHD handle,const char* script_content); //远程执行脚本,由于执行脚本的时间由脚本内容决定，该接口立即返回。

//ROBOT_API_EXPORT BOOL API_GetVariableValue(JTRHD handle,const char* var_name, double& value); //获取变量值
ROBOT_API_EXPORT BOOL API_GetVariableValue(JTRHD handle,const char* var_name, VariableValue* value); //获取变量值描述
ROBOT_API_EXPORT BOOL API_SetOffset(JTRHD handle,TrajectoryOffset offset); //设置轨迹偏移量
ROBOT_API_EXPORT BOOL API_GetOffset(JTRHD handle,TrajectoryOffset* offset); //获取轨迹偏移量

ROBOT_API_EXPORT BOOL API_SendFile(JTRHD handle,const char* local_absolute_path_file_name,const char* save_path,const char* save_file_name);
ROBOT_API_EXPORT BOOL API_ExecuteFile(JTRHD handle,const char* remote_absolute_path_file_name); //远程执行文件,输入对端绝对路径文件名。脚本文件不能带tree如movej而不是treemovej

ROBOT_API_EXPORT BOOL API_ControlGripper(JTRHD handle,int index,GripperAction action);//index 1表示配置的第一个

ROBOT_API_EXPORT BOOL API_GetCollisionLevel(JTRHD handle,CollisionLevel& level);//level 碰撞等级，取值范围[0,5],0:关闭碰撞。碰撞阈值 1:10N,2:20N,3:30,4:40N,5:50N
ROBOT_API_EXPORT BOOL API_SetCollisionLevel(JTRHD handle,const CollisionLevel level);//level 碰撞等级，取值范围[0,5],0:关闭碰撞。碰撞阈值 1:10N,2:20N,3:30,4:40N,5:50N

ROBOT_API_EXPORT BOOL API_OpenSerialPort(JTRHD handle,const UART_Params* param);  //打开串口
ROBOT_API_EXPORT BOOL API_SendRtuCmd(JTRHD handle,const ModbusRTU_Frame* req,ModbusRTU_Frame* rsp,int timeout=2);//发生RTU指令 timeout:超时时间,默认值2s
ROBOT_API_EXPORT BOOL API_ModbusRtuRW(JTRHD handle,const ModbusRTU_Request* req,ModbusRTU_Frame* rsp,int timeout=2); //Modbus RTU 读写操作
ROBOT_API_EXPORT BOOL API_CloseSerialPort(JTRHD handle);


ROBOT_API_EXPORT BOOL API_TcpPositionCalibration(JTRHD handle,const char* points);//points分号(;)分割的多个点(关节位置)信息形如:xxx,xxx,xxx,xxx,xxx,xxx;xxx,xxx,xxx,xxx,xxx,xxx;...,只能4个点或6个点
ROBOT_API_EXPORT BOOL API_TcpDirectionCalibration(JTRHD handle,const char* points);//points分号(;)分割的多个点(关节位置)信息形如:xxx,xxx,xxx,xxx,xxx,xxx;xxx,xxx,xxx,xxx,xxx,xxx;...,只能3个点
ROBOT_API_EXPORT BOOL API_GetDragButtonStatus(JTRHD handle,ToolButtonStatus& status);
ROBOT_API_EXPORT BOOL API_GetPointSetButtonStatus(JTRHD handle,ToolButtonStatus& status);
ROBOT_API_EXPORT BOOL API_GetRobotErrorCode(JTRHD handle,int& error_code);
//tcp_pose:笛卡尔空间位姿值,ref_joint_rad:逆解计算用的参考关节空间位置(单位:弧度),result:关节空间位置计算结果(单位:弧度)
ROBOT_API_EXPORT BOOL API_InverseKin(JTRHD handle,const TcpPosition* tcp_pose,const JointRad* ref_joint_rad,JointRad* result);
ROBOT_API_EXPORT BOOL API_ForwardKin(JTRHD handle,const JointRad* joint_rad,TcpPosition* result);
ROBOT_API_EXPORT BOOL API_PointDist(JTRHD handle,const TcpPosition* p_from,const TcpPosition* p_to,float& distance);
ROBOT_API_EXPORT BOOL API_PoseAdd(JTRHD handle,const TcpPosition* p_from,const TcpPosition* p_to,TcpPosition* result);
ROBOT_API_EXPORT BOOL API_PoseInv(JTRHD handle,const TcpPosition* p_from,TcpPosition* result);
ROBOT_API_EXPORT BOOL API_PoseSub(JTRHD handle,const TcpPosition* p_to,const TcpPosition* p_from,TcpPosition* result);
ROBOT_API_EXPORT BOOL API_PoseTrans(JTRHD handle,const TcpPosition* p_from,const TcpPosition* p_from_to,TcpPosition* result);

ROBOT_API_EXPORT BOOL API_Weavep(JTRHD handle,WeavepParam* parameter);
ROBOT_API_EXPORT BOOL API_Weavec(JTRHD handle,WeavecParam* parameter);
ROBOT_API_EXPORT BOOL API_ExtAxisMovej(JTRHD handle,ExtAxisMovejParam* parameter);
ROBOT_API_EXPORT BOOL API_ExtAxisMovepc(JTRHD handle,ExtAxisMovepcParam* parameter);

ROBOT_API_EXPORT BOOL API_GetRobotHomeJointRad(JTRHD handle,JointRad* joint_rad);//获取机器人零位关节弧度
ROBOT_API_EXPORT BOOL API_ResetRobotError(JTRHD handle);  //错误复位
ROBOT_API_EXPORT BOOL API_GetRobotRunTime(JTRHD handle,long& run_time);//获取机器人运行时间 run_time 单位:秒
ROBOT_API_EXPORT BOOL API_GetPowerOffDelayTime(JTRHD handle,int& delay_time);//获取机器人下电延迟时间 delay_time 单位:毫秒
ROBOT_API_EXPORT BOOL API_EmergencyStop(JTRHD handle); //机器人急停
ROBOT_API_EXPORT BOOL API_ClearUnfinishedTrajectory(JTRHD handle);//清除未完成的轨迹

ROBOT_API_EXPORT BOOL API_GetPointsInProgram(JTRHD handle,const char* program_file_name,PointsInProgram* points);
ROBOT_API_EXPORT BOOL API_GetFirmwareVersion(JTRHD handle,VersionInfo* firmware_version);
ROBOT_API_EXPORT BOOL API_SetMountedPose(JTRHD handle,const MountedPose mounted_type);
ROBOT_API_EXPORT BOOL API_SetMountedAngle(JTRHD handle,const float tiltAngle,const float baseRotationAngle);
ROBOT_API_EXPORT BOOL API_ModbusRtuRWEndTool(JTRHD handle,const ModbusRTU_Request* req,ModbusRTU_Frame* rsp,int timeout=2); //Modbus RTU 末端读写操作

#endif // ROBOTAPI_H
