@echo off
:Main
cls
set MYIP=
set /p MYIP=设置IP地址(x.x.x.x): 
if defined MYIP (
adb shell hqsetprop persist.npv.chn0.main.ip %MYIP%
adb shell sync
echo [%date% %time%] 设置IP: %MYIP% >> OptRecord.txt

) else (
    echo 输入为空，重新输入
    pause
    goto Main
)

:Main2
set /p MYPORT=设置端口(如8111): 
if defined MYPORT (
adb shell hqsetprop persist.npv.chn0.main.port %MYPORT%
adb shell sync
echo [%date% %time%] 设置IP: %MYPORT% >> OptRecord.txt

) else (
    echo 输入为空，重新输入
    pause
    goto Main2
)

pause
