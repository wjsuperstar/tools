@echo off
set /p note=你确定要配置该电信卡吗？(y/n) 
if "%note%" == "y" (
adb shell `echo -e -n "AT+QNVFW=\"/nv/item_files/modem/mmode/operator_name\",00\r\n" > /dev/smd8`
adb shell sync
echo 配置成功！
)
pause
