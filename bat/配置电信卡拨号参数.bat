@echo off
set /p note=��ȷ��Ҫ���øõ��ſ���(y/n) 
if "%note%" == "y" (
adb shell `echo -e -n "AT+QNVFW=\"/nv/item_files/modem/mmode/operator_name\",00\r\n" > /dev/smd8`
adb shell sync
echo ���óɹ���
)
pause
