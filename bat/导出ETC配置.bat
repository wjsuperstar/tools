@echo off
rem set adbCmd=D:\tools\adb402\adb
set adbCmd=adb

set outPath=/vendor/app/hq/

%adbCmd% shell sync
%adbCmd% pull  %outPath%etc .

pause