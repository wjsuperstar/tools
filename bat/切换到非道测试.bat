@echo off

set MYIP=202.96.122.219
set MYPORT=2047
set MYVIN=LGDCP91GXKA119325


set /p note=��ȷ��Ҫ�л�ƽ̨��(y/n) 
if "%note%" == "y" (
adb shell hqsetprop persist.obd.chn0.main.ip %MYIP%
adb shell hqsetprop persist.obd.chn0.main.port %MYPORT%
adb shell hqsetprop persist.tbox.vin %MYVIN%
adb shell hqsetprop persist.obd.chn0.channel.type 15
adb shell hqsetprop persist.obd.chn0.wait.data.mode 0

adb shell sync
echo �л��������ɹ�������
echo [%date% %time%] �л�������: %MYIP%:%MYPORT%, VIN: %MYVIN%  >> OptRecord.txt
)
pause
