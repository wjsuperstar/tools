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
