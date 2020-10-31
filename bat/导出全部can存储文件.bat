@echo off
rem set adbCmd=E:\tools\adb402\adb
set adbCmd=adb

%adbCmd% shell sync
%adbCmd% pull  /media/card/data/SORT1 .
%adbCmd% pull  /media/card/data/SORT2 .
%adbCmd% pull  /media/card/data/SORT3 .

pause