
echo ÕıÔÚÉèÖÃ...
adb shell hqsetprop persist.tbox.wakeup.interval 3600
adb shell hqsetprop persist.tbox.delay.sleep.time 1800
adb shell hqsetprop persist.tbox.can0.baud.rate.adaptive 0
adb shell hqsetprop persist.tbox.can1.baud.rate.adaptive 0
adb shell hqsetprop sync.at.once 1
adb shell sync

pause
