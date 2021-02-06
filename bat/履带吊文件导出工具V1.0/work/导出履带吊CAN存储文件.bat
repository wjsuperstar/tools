@echo off
set adbCmd=adb
set unzipCmd=..\7za.exe 

set SortName1=SORT1
set SortName2=SORT2
set SortName3=BACKUPS

%adbCmd% shell sync
echo 开始导出所有CAN数据存储文件：
%adbCmd% pull  /media/card/data/%SortName1% .
%adbCmd% pull  /media/card/data/%SortName2% .
%adbCmd% pull  /media/card/data/%SortName3% .

echo 导出文件成功，开始解压文件...

IF EXIST %SortName1%_X (
    rd /s /q %SortName1%_X
) ELSE (
    md %SortName1%_X
)

IF EXIST %SortName2%_X (
    rd /s /q %SortName2%_X
) ELSE (
    md %SortName2%_X
)

IF EXIST %SortName3%_X (
    rd /s /q %SortName3%_X
) ELSE (
    md %SortName3%_X
)

echo 解压%SortName1%目录到%SortName1%_X
%unzipCmd%  x -y -aoa %SortName1% -o%SortName1%_X

echo 解压%SortName2%目录到%SortName2%_X
md SORT1_X
%unzipCmd%  x -y -aoa %SortName2% -o%SortName2%_X

echo 解压%SortName3%目录到%SortName3%_X
md SORT1_X
%unzipCmd%  x -y -aoa %SortName3% -o%SortName3%_X

echo 解压成功...

pause