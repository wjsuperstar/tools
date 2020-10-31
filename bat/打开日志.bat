
echo ’˝‘⁄…Ë÷√...
adb shell hqsetprop persist.debug.Npv32960.trace 1
adb shell hqsetprop persist.debug.Jt808.trace 1
adb shell hqsetprop persist.debug.OBD.method.trace 1
adb shell hqsetprop persist.tbox.mculog.levelmask 255
adb shell hqsetprop persist.debug.mculog.trace 1
adb shell hqsetprop persist.debug.mqtt.proxy.trace 1
adb shell hqsetprop persist.debug.universal.socket.trace 1
adb shell hqsetprop persist.debug.ec20.module.server.trace 1
rem adb shell hqsetprop persist.npv.chn0.log.max.file.size.KB 4096
rem adb shell hqsetprop persist.npv.chn0.log.max.file.count   20
adb shell sync

pause


hqsetprop persist.debug.Npv32960.trace 1
hqsetprop persist.npv.chn%d.log.max.file.count 20

