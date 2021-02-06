@echo off
rem set adbCmd=D:\tools\adb402\adb
set adbCmd=adb
set fileName=simple_can.txt
echo ==================%date%==================== >> %fileName%
%adbCmd% shell "hqgetprop |grep ro.tbox.id" >> %fileName%
echo -------------------------------------------- >> %fileName%
%adbCmd% shell "hqgetprop |grep can" >> %fileName%

pause