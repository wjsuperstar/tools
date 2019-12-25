@echo off
set fileName=Npv32960

set fileTime=0
set fileTimeLast=0
echo 初始化：%fileTime% %fileTimeLast%
:Loop
choice /t 1 /d y /n >nul

if not exist %fileName% (goto loop)

for /f "skip=4 tokens=1-3 delims= " %%a in ('dir %fileName%') do (
set fileTime=%%b
goto Break
) 
:Break

rem echo 比较：%fileTime% %fileTimeLast%
if %fileTime% gtr %fileTimeLast% (
echo 开始导入...
adb push %fileName% /vendor/app/hq/bin
adb shell chmod 777 /vendor/app/hq/bin/%fileName%
echo 导入成功!!! [%date% %time%]
adb shell killall -9 %fileName%
set fileTimeLast=%fileTime%
)

goto loop

pause