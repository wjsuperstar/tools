@echo off

echo 烧写过程中请勿断电！！！烧写过程中请勿断电！！！烧写过程中请勿断电！！！

echo (1) 导入程序...
adb push tbox.zip /vendor/data/tbox.zip
IF %ERRORLEVEL% NEQ 0 goto failed
adb shell mv /vendor/data/tbox.zip /vendor/data/autoruntbox.zip
IF %ERRORLEVEL% NEQ 0 goto failed
adb shell rm -f /vendor/data/update_succeed.flag
IF %ERRORLEVEL% NEQ 0 goto failed
echo (2) 开始烧写程序...
:G4Loop
set /a num+=5
if %num% GEQ 50 set /a num=50
echo 烧写进度 %num%%%
rem 延时2秒
choice /t 2 /d y /n >nul
rem 查询升级成功标志
for /f "tokens=1-3 delims=:" %%a in ('adb shell ls /vendor/data/update_succeed.flag') do (
set g4FileFlg=%%c
)
if "%g4FileFlg%" == " No such file or directory" goto G4Loop

:McuLoop
set /a num+=5
if %num% GEQ 90 set /a num=95
echo 烧写进度 %num%%%
rem 延时2秒
choice /t 2 /d y /n >nul
for /f "tokens=1-3 delims=_" %%a in ('adb shell ls /vendor/data/McuUpdate/tbox*') do (
set McuFileFlg=%%b
)

if "%McuFileFlg%" EQU "mcu" goto McuLoop

echo 烧写进度 100%%
echo ~~~~~~~~~~~~~~~~~~~~~烧写成功~~~~~~~~~~~~~~~~~~~~~
echo (3) 重启设备...
adb shell hqsetprop tbox.reset.device 1
adb shell hqsetprop sync.at.once 1

echo 请按任意键结束
pause>nul
exit 0

:failed
echo ！！！！！！！！！！！烧写失败！！！！！！！！！！！
echo 请按任意键结束
pause>nul
exit 1
