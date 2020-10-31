echo ÕıÔÚÉèÖÃ...
adb shell hqsetprop persist.tbox.can0.baud.rate.adaptive 0
adb shell hqsetprop persist.tbox.can1.baud.rate.adaptive 0
adb shell hqsetprop sync.at.once 1
adb shell sync
pause
