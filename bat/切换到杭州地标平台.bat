@echo off

set MYIP=122.112.203.25
set MYPORT=6099
set MYVIN=LGDCP91GXKA119325


set /p note=��ȷ��Ҫ�л�ƽ̨��(y/n) 
if "%note%" == "y" (
adb shell hqsetprop persist.obd.chn0.main.ip %MYIP%
adb shell hqsetprop persist.obd.chn0.main.port %MYPORT%
adb shell hqsetprop persist.tbox.vin %MYVIN%
adb shell hqsetprop persist.obd.chn0.channel.type 3
adb shell sync
echo �л��������ɹ�������
echo [%date% %time%] �л�������: %MYIP%:%MYPORT%, VIN: %MYVIN%  >> OptRecord.txt
)
pause

����vin��
string��0x04C2142A

obdͨ��1��
kPidGb17691ProtoType = 0x04c2041a, ///< BYTE ����ƽ̨ѡ��  2
kPidObdHost = 0x04ca142c, ///< String OBD IP��ַ  122.112.203.25
kPidObdPort = 0x04ca080c, ///< WORD OBD IP�˿� 6099
kPidObdReportDataStreamNums = 0x04c2041f, ///< BYTE OBD �������ϱ�ÿ������  2
kPidObdEncryptType = 0x04c2041d, ///< BYTE OBD ��������  1
kPidObdCollectInterval = 0x05c20420, ///< BYTE OBD �������ϱ���� 10
kPidObdLoginMode = 0x05c20425, ///< BYTE OBD����ǳ����� 0:ig,1: rev, 2: no limit

obdͨ��2:
kPidObdHostChn2 = 0x05ca1433, ///< MEM OBD�ڶ�ͨ��IP��ַ 
kPidObdPortChn2 = 0x05ca0813, ///< WORD OBD�ڶ�ͨ���˿� 
kPidObdProtocolTypeChn2 = 0x05c2042f, ///< BYTE OBD�ڶ�ͨ��Э������ 0
kPidObdEncryptTypeChn2 = 0x04c20431, ///< BYTE OBD�ڶ�ͨ�� �������� 1
kPidObdReportDataStreamNumsChn2 = 0x04c20432, ///< BYTE OBD�ڶ�ͨ�� �������ϱ�ÿ������ 1
kPidObdCollectIntervalChn2 = 0x05c20433, ///< BYTE OBD �ڶ�ͨ���������ɼ���� 30
kPidObdLoginModeChn2 = 0x05c20436, ///< BYTE OBD�ڶ�ͨ������ǳ����� 2
kPidOBdSignatureChn2 = 0x05c20439, ///< BYTE OBD�ڶ�ͨ��ǩ������ 0
    
    
