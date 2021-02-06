@echo off
:Main
cls
set str=
set /p str=请输入任意字符，或直接回车：
if defined str (
    echo 变量 str 的值不为空
) else echo 变量 str 为空值
pause

goto Main