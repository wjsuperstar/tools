@echo off

echo ��д����������ϵ磡������д����������ϵ磡������д����������ϵ磡����

echo (1) �������...
adb push tbox.zip /vendor/data/tbox.zip
IF %ERRORLEVEL% NEQ 0 goto failed
adb shell mv /vendor/data/tbox.zip /vendor/data/autoruntbox.zip
IF %ERRORLEVEL% NEQ 0 goto failed
adb shell rm -f /vendor/data/update_succeed.flag
IF %ERRORLEVEL% NEQ 0 goto failed
echo (2) ��ʼ��д����...
:G4Loop
set /a num+=5
if %num% GEQ 50 set /a num=50
echo ��д���� %num%%%
rem ��ʱ2��
choice /t 2 /d y /n >nul
rem ��ѯ�����ɹ���־
for /f "tokens=1-3 delims=:" %%a in ('adb shell ls /vendor/data/update_succeed.flag') do (
set g4FileFlg=%%c
)
if "%g4FileFlg%" == " No such file or directory" goto G4Loop

:McuLoop
set /a num+=5
if %num% GEQ 90 set /a num=95
echo ��д���� %num%%%
rem ��ʱ2��
choice /t 2 /d y /n >nul
for /f "tokens=1-3 delims=_" %%a in ('adb shell ls /vendor/data/McuUpdate/tbox*') do (
set McuFileFlg=%%b
)

if "%McuFileFlg%" EQU "mcu" goto McuLoop

echo ��д���� 100%%
echo ~~~~~~~~~~~~~~~~~~~~~��д�ɹ�~~~~~~~~~~~~~~~~~~~~~
echo (3) �����豸...
adb shell hqsetprop tbox.reset.device 1
adb shell hqsetprop sync.at.once 1

echo �밴���������
pause>nul
exit 0

:failed
echo ������������������������дʧ�ܣ���������������������
echo �밴���������
pause>nul
exit 1
