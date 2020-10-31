
echo ÕıÔÚÉèÖÃ...
adb shell hqsetprop persist.tbox.vin TESTHXOBD00000001
adb shell hqsetprop persist.obd.chn0.main.ip 202.102.101.217
adb shell hqsetprop persist.obd.chn0.main.port 60705

adb shell sync
pause
