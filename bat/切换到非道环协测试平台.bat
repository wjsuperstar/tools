@echo off

set MYIP=122.112.144.129
set MYPORT=6101
set MYVIN=HZHQFD02001052279

set /p note=你确定要切换平台吗？(y/n) 
if "%note%" == "y" (
adb shell hqsetprop persist.obd.chn0.main.ip %MYIP%
adb shell hqsetprop persist.obd.chn0.main.port %MYPORT%
adb shell hqsetprop persist.tbox.vin %MYVIN%
adb shell hqsetprop persist.obd.chn0.channel.type 15
adb shell sync
echo 切换服务器成功！！！
echo [%date% %time%] 切换服务器: %MYIP%:%MYPORT%, VIN: %MYVIN%  >> OptRecord.txt
)
pause
