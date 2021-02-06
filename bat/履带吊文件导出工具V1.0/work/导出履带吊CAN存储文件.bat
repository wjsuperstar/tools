@echo off
set adbCmd=adb
set unzipCmd=..\7za.exe 

set SortName1=SORT1
set SortName2=SORT2
set SortName3=BACKUPS

%adbCmd% shell sync
echo ��ʼ��������CAN���ݴ洢�ļ���
%adbCmd% pull  /media/card/data/%SortName1% .
%adbCmd% pull  /media/card/data/%SortName2% .
%adbCmd% pull  /media/card/data/%SortName3% .

echo �����ļ��ɹ�����ʼ��ѹ�ļ�...

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

echo ��ѹ%SortName1%Ŀ¼��%SortName1%_X
%unzipCmd%  x -y -aoa %SortName1% -o%SortName1%_X

echo ��ѹ%SortName2%Ŀ¼��%SortName2%_X
md SORT1_X
%unzipCmd%  x -y -aoa %SortName2% -o%SortName2%_X

echo ��ѹ%SortName3%Ŀ¼��%SortName3%_X
md SORT1_X
%unzipCmd%  x -y -aoa %SortName3% -o%SortName3%_X

echo ��ѹ�ɹ�...

pause