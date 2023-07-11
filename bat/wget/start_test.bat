@echo off

echo 开始测试...
set url1=http://124.115.177.250:9010/official/file/test_dome1.mp4
set url2=http://124.115.177.250:9010/official/file/test_dome2.mp4
set dst_file=test_dome.mp4
set WGET=wget.exe --limit-rate=200k -t 10 -S
rem delay_time表示文件下载间隔：
set delay_time=60

:Loop

rem download url1
set /a num+=1
echo 测试次数:%num%
%WGET% %url1% -O %dst_file%
IF %ERRORLEVEL% NEQ 0 goto Failed
for /f "delims= " %%a in ('md5sum %dst_file%') do (
set md5val=%%a
)
echo md5val:%md5val%
if "%md5val%" == "7ffe4934b13fc9b600b2930353618206" (
echo MD5校验成功！
) else (
echo "MD5校验失败(current md5=7ffe4934b13fc9b600b2930353618206)！"
goto Failed
)
choice /t %delay_time% /d y /n >nul

rem download url2
set /a num+=1
echo 测试次数:%num%
%WGET% %url2% -O %dst_file%
IF %ERRORLEVEL% NEQ 0 goto Failed
for /f "delims= " %%a in ('md5sum %dst_file%') do (
set md5val=%%a
)
echo md5val:%md5val%
if "%md5val%" == "3be9e4080f8b09218830ce5ecf38ee9f" (
echo MD5校验成功！
) else (
echo "MD5校验失败(current md5=3be9e4080f8b09218830ce5ecf38ee9f)！"
goto Failed
)
choice /t %delay_time% /d y /n >nul


goto loop

:Failed
ping 192.168.100.1 -n 3
ping 8.8.8.8 -n 3
echo 下载异常，请保持现场，立即联系相关开发分析！！！！！！！！！！

pause