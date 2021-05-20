@echo off

set MYIP=122.112.203.25
set MYPORT=6099
set MYVIN=LGDCP91GXKA119325


set /p note=你确定要切换平台吗？(y/n) 
if "%note%" == "y" (
adb shell hqsetprop persist.obd.chn0.main.ip %MYIP%
adb shell hqsetprop persist.obd.chn0.main.port %MYPORT%
adb shell hqsetprop persist.tbox.vin %MYVIN%
adb shell hqsetprop persist.obd.chn0.channel.type 3
adb shell sync
echo 切换服务器成功！！！
echo [%date% %time%] 切换服务器: %MYIP%:%MYPORT%, VIN: %MYVIN%  >> OptRecord.txt
)
pause

设置vin：
string，0x04C2142A

obd通道1：
kPidGb17691ProtoType = 0x04c2041a, ///< BYTE 国六平台选择  2
kPidObdHost = 0x04ca142c, ///< String OBD IP地址  122.112.203.25
kPidObdPort = 0x04ca080c, ///< WORD OBD IP端口 6099
kPidObdReportDataStreamNums = 0x04c2041f, ///< BYTE OBD 数据流上报每包条数  2
kPidObdEncryptType = 0x04c2041d, ///< BYTE OBD 加密类型  1
kPidObdCollectInterval = 0x05c20420, ///< BYTE OBD 数据流上报间隔 10
kPidObdLoginMode = 0x05c20425, ///< BYTE OBD登入登出策略 0:ig,1: rev, 2: no limit

obd通道2:
kPidObdHostChn2 = 0x05ca1433, ///< MEM OBD第二通道IP地址 
kPidObdPortChn2 = 0x05ca0813, ///< WORD OBD第二通道端口 
kPidObdProtocolTypeChn2 = 0x05c2042f, ///< BYTE OBD第二通道协议类型 0
kPidObdEncryptTypeChn2 = 0x04c20431, ///< BYTE OBD第二通道 加密类型 1
kPidObdReportDataStreamNumsChn2 = 0x04c20432, ///< BYTE OBD第二通道 数据流上报每包条数 1
kPidObdCollectIntervalChn2 = 0x05c20433, ///< BYTE OBD 第二通道数据流采集间隔 30
kPidObdLoginModeChn2 = 0x05c20436, ///< BYTE OBD第二通道登入登出策略 2
kPidOBdSignatureChn2 = 0x05c20439, ///< BYTE OBD第二通道签名配置 0
    
    
