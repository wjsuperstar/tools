
set adbCmd=D:\tools\adb401\adb.exe


%adbCmd% shell rm /vendor/data/factory.flag
%adbCmd% shell hqsetprop persist.tbox.runningmode 0
%adbCmd% shell sync

echo �밴�������ʼ�����

pause>nul

