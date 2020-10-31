
echo ÕıÔÚÉèÖÃ...
adb shell hqsetprop persist.tbox.wakeup.interval 120
adb shell hqsetprop persist.jt808.chn0.delay.sleep.tick 120000
adb shell hqsetprop sync.at.once 1
adb shell sync

pause
