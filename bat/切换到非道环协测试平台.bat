@echo off

set MYIP=122.112.144.129
set MYPORT=6101
set MYVIN=HZHQFD02001052279

set /p note=��ȷ��Ҫ�л�ƽ̨��(y/n) 
if "%note%" == "y" (
adb shell hqsetprop persist.obd.chn0.main.ip %MYIP%
adb shell hqsetprop persist.obd.chn0.main.port %MYPORT%
adb shell hqsetprop persist.tbox.vin %MYVIN%
adb shell hqsetprop persist.obd.chn0.channel.type 15
adb shell sync
echo �л��������ɹ�������
echo [%date% %time%] �л�������: %MYIP%:%MYPORT%, VIN: %MYVIN%  >> OptRecord.txt
)
pause
