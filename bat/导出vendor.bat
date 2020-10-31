@echo off
rem set adbCmd=D:\tools\adb402\adb
set adbCmd=adb

%adbCmd% shell sync
%adbCmd% pull  /vendor .

pause