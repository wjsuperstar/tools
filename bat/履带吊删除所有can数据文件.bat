@echo off
set /p note=你确定要删除所有数据吗？(y/n) 
if "%note%" == "y" (
adb shell hqstop CAN
adb shell rm -rf /media/card/data/SORT1/
adb shell rm -rf /media/card/data/SORT2/
adb shell rm -rf /media/card/data/BACKUPS/
adb shell hqstart CAN
echo 删除所有数据成功！！！
)
pause

