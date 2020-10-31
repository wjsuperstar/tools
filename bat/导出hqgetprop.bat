@echo off
rem set adbCmd=D:\tools\adb402\adb
set adbCmd=adb
set filename=hqgetprop.txt
echo ==================%date%==================== >> %filename%
%adbCmd% shell "hqgetprop |grep ro.tbox.id" >> %filename%
echo -------------------------------------------- >> %filename%
%adbCmd% shell hqgetprop >> %filename%

pause