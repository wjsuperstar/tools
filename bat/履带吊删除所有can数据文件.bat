@echo off
set /p note=��ȷ��Ҫɾ������������(y/n) 
if "%note%" == "y" (
adb shell hqstop CAN
adb shell rm -rf /media/card/data/SORT1/
adb shell rm -rf /media/card/data/SORT2/
adb shell rm -rf /media/card/data/BACKUPS/
adb shell hqstart CAN
echo ɾ���������ݳɹ�������
)
pause

