@echo off

echo ��ʼ����...
set url1=http://124.115.177.250:9010/official/file/test_dome1.mp4
set url2=http://124.115.177.250:9010/official/file/test_dome2.mp4
set dst_file=test_dome.mp4
set WGET=wget.exe --limit-rate=200k -t 10 -S
rem delay_time��ʾ�ļ����ؼ����
set delay_time=60

:Loop

rem download url1
set /a num+=1
echo ���Դ���:%num%
%WGET% %url1% -O %dst_file%
IF %ERRORLEVEL% NEQ 0 goto Failed
for /f "delims= " %%a in ('md5sum %dst_file%') do (
set md5val=%%a
)
echo md5val:%md5val%
if "%md5val%" == "7ffe4934b13fc9b600b2930353618206" (
echo MD5У��ɹ���
) else (
echo "MD5У��ʧ��(current md5=7ffe4934b13fc9b600b2930353618206)��"
goto Failed
)
choice /t %delay_time% /d y /n >nul

rem download url2
set /a num+=1
echo ���Դ���:%num%
%WGET% %url2% -O %dst_file%
IF %ERRORLEVEL% NEQ 0 goto Failed
for /f "delims= " %%a in ('md5sum %dst_file%') do (
set md5val=%%a
)
echo md5val:%md5val%
if "%md5val%" == "3be9e4080f8b09218830ce5ecf38ee9f" (
echo MD5У��ɹ���
) else (
echo "MD5У��ʧ��(current md5=3be9e4080f8b09218830ce5ecf38ee9f)��"
goto Failed
)
choice /t %delay_time% /d y /n >nul


goto loop

:Failed
ping 192.168.100.1 -n 3
ping 8.8.8.8 -n 3
echo �����쳣���뱣���ֳ���������ϵ��ؿ���������������������������

pause