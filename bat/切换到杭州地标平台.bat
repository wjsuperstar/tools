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
