@echo off
:Main
cls
set MYIP=
set /p MYIP=����IP��ַ(x.x.x.x): 
if defined MYIP (
adb shell hqsetprop persist.npv.chn0.main.ip %MYIP%
adb shell sync
echo [%date% %time%] ����IP: %MYIP% >> OptRecord.txt

) else (
    echo ����Ϊ�գ���������
    pause
    goto Main
)

:Main2
set /p MYPORT=���ö˿�(��8111): 
if defined MYPORT (
adb shell hqsetprop persist.npv.chn0.main.port %MYPORT%
adb shell sync
echo [%date% %time%] ����IP: %MYPORT% >> OptRecord.txt

) else (
    echo ����Ϊ�գ���������
    pause
    goto Main2
)

pause
