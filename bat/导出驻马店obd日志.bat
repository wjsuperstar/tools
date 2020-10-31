@echo off
rem set adbCmd=D:\tools\adb402\adb
set adbCmd=adb


set outType=/media/card/data/UniversalSocket
rem set outType=EC20DataCall
rem set outType=EC20ModuleServer
rem set outType=jt808
rem set outType=Npv32960

%adbCmd% shell sync
%adbCmd% pull  %outType% .

pause