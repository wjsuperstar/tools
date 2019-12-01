#!/system/bin/sh

#存储根路径，主要用于兼容SD卡和U盘（带最后的/号）
STORAGE_PATH=${1}

BTN_OK=1
BTN_NONE=0

#对话框唯一标识，在此用进程ID来充当
MsgBoxID="I"$$

TARGET_HD_VER=300014

#获取鸿泉属性
GetHQProp()
{
    val=$(hqgetprop $1)
    result=$?
    if [ result -eq 0 ]; then
        echo $val
        return 0
    fi
    return 1
}

#设置鸿泉属性
SetHQProp()
{
    key=$1
    val=$2
    hqsetprop $1 $2
}

#显示对话框（主要用于用户提示，及选择）
#$1: ID $2: ACTION $3: TITLE $4: CAPTION $5 BUTTON $6 PROCESSBAR $7 ICON
MsgBox()
{
    hqtoolbox @hqmsgbox -I $1 -a $2 -t $3 -c $4 -b $5 -p $6 -i $7
    return 0
}


#输出进程信息
PidStatusOut()
{
    val="/proc/"$1"/status"
    #Log "val=$val"
    cat $val >> ${STORAGE_PATH}pidstatus.txt
    echo "***************" >> ${STORAGE_PATH}pidstatus.txt
}

#输出内存信息
MeminfoOut()
{
    dumpsys meminfo | grep zui > /data/tmp/meminfo.txt
    echo "***************" >> /data/tmp/meminfo.txt
    cp /data/tmp/meminfo.txt ${STORAGE_PATH}
    
    #dumpsys meminfo >> ${STORAGE_PATH}meminfo.txt
    #echo "***************" >> ${STORAGE_PATH}meminfo.txt
    sync
}

#输出CPU信息
CpuinfoOut()
{
    dumpsys cpuinfo > /data/tmp/cpuinfo.txt
    echo "***************" >> /data/tmp/cpuinfo.txt
    cp /data/tmp/cpuinfo.txt ${STORAGE_PATH}
    
    #dumpsys cpuinfo >> ${STORAGE_PATH}cpuinfo.txt
    #echo "***************" >> ${STORAGE_PATH}cpuinfo.txt
    sync
}

#清空内存、CPU、进程日志信息
CleanDataOutTxt()
{
    echo "" > ${STORAGE_PATH}meminfo.txt
    echo "" > ${STORAGE_PATH}cpuinfo.txt
    echo "" > ${STORAGE_PATH}pidstatus.txt
}

#检测进程是否存在
PidExists()
{
    if [ -d /proc/$1 ];then 
        return 0
    fi
    return 1
}

#检查是否已经有一个拷贝进程
CheckUpgradePID()
{
   pid=$(GetHQProp "hq.lcd.naviupgrade.pid")
   
   #有则干掉
    if [ $pid -gt 0 ]; then
        kill -9 $pid
        Log "pid exists, kill -9 PID=$pid"
    fi
}

#检查目录是否存在(存在返回1 否则返回0)
CheckLocalPath()
{
    flag=1
    while(( "$flag" <= 5 ))
    do
        if [ ! -e $objLocalPath ]; then
            return 0
        else
            sleep 1
        fi
        let "flag++"
        Log "flag : $flag"
    done
    return 1
}

cpForce()
{
	if [ -e $1 ]; then
	    rm -f $2
		cp -f $1 $2.new
		sync
		mv -f $2.new $2
		chmod $3 $2
	fi
}

mkdirIfNotExists()
{	
	if [ ! -e $1 ]; then
		mkdir $1
		chmod $2 $1
	fi
}

createRamdisk()
{
	if [ ! -e "/vendor/ramdisk" ]; then
		mkdirIfNotExists /vendor/ramdisk 0777
	fi
	mount -t tmpfs -o size=$1 tmpfs /vendor/ramdisk
}

mkdirPrePare()
{	
	mkdirIfNotExists $1 0755
	mkdirIfNotExists $1/hq 0755
	mkdirIfNotExists $1/hq/bin 0755
	mkdirIfNotExists $1/hq/tool 0755
	mkdirIfNotExists $1/hq/etc 0755
	mkdirIfNotExists $1/hq/sh 0755
	mkdirIfNotExists $1/hq/drv 0755
	mkdirIfNotExists $1/hq/lib 0755
	mkdirIfNotExists $1/hq/update 0755
	mkdirIfNotExists $1/hq/plug 0755
	mkdirIfNotExists $1/hq/plug/can 0755
	mkdirIfNotExists $1/hq/property 0666
}

DoCopy()
{
cpForce /vendor/ramdisk/app/hq/bin/call $1/hq/bin/call 0755
cpForce /vendor/ramdisk/app/hq/bin/CAN $1/hq/bin/CAN 0755
cpForce /vendor/ramdisk/app/hq/bin/coprocess $1/hq/bin/coprocess 0755
#cpForce /vendor/ramdisk/app/hq/bin/DriveModel $1/hq/bin/DriveModel 0755
cpForce /vendor/ramdisk/app/hq/bin/EC20DataCall $1/hq/bin/EC20DataCall 0755
cpForce /vendor/ramdisk/app/hq/bin/EC20GnssAdapter $1/hq/bin/EC20GnssAdapter 0755
cpForce /vendor/ramdisk/app/hq/bin/EC20ModuleServer $1/hq/bin/EC20ModuleServer 0755
#cpForce /vendor/ramdisk/app/hq/bin/EC20Wifi $1/hq/bin/EC20Wifi 0755
#cpForce /vendor/ramdisk/app/hq/bin/ElectricFence $1/hq/bin/ElectricFence 0755
cpForce /vendor/ramdisk/app/hq/bin/FactorySelfTest $1/hq/bin/FactorySelfTest 0755
cpForce /vendor/ramdisk/app/hq/bin/FactorySetJit $1/hq/bin/FactorySetJit 0755
#cpForce /vendor/ramdisk/app/hq/bin/GnssAdapter $1/hq/bin/GnssAdapter 0755
cpForce /vendor/ramdisk/app/hq/bin/GPS $1/hq/bin/GPS 0755
cpForce /vendor/ramdisk/app/hq/bin/hqcomhub $1/hq/bin/hqcomhub 0755
#cpForce /vendor/ramdisk/app/hq/bin/hqfilesbak $1/hq/bin/hqfilesbak 0755
cpForce /vendor/ramdisk/app/hq/bin/hqinit $1/hq/bin/hqinit 0755
cpForce /vendor/ramdisk/app/hq/bin/hqtoolbox $1/hq/bin/hqtoolbox 0755
cpForce /vendor/ramdisk/app/hq/bin/hqupdate $1/hq/bin/hqupdate 0755
cpForce /vendor/ramdisk/app/hq/bin/hqverscan $1/hq/bin/hqverscan 0755
cpForce /vendor/ramdisk/app/hq/bin/hqfilescan $1/hq/bin/hqfilescan 0755
cpForce /vendor/ramdisk/app/hq/bin/Jt808 $1/hq/bin/Jt808 0755
#cpForce /vendor/ramdisk/app/hq/bin/ModuleServer $1/hq/bin/ModuleServer 0755
cpForce /vendor/ramdisk/app/hq/bin/BinDataExport $1/hq/bin/BinDataExport 0755
cpForce /vendor/ramdisk/app/hq/bin/McuLog $1/hq/bin/McuLog 0755
cpForce /vendor/ramdisk/app/hq/bin/McuUpdate $1/hq/bin/McuUpdate 0755
cpForce /vendor/ramdisk/app/hq/bin/ShortMsgManage $1/hq/bin/ShortMsgManage 0755
cpForce /vendor/ramdisk/app/hq/bin/RDC $1/hq/bin/RDC 0755
cpForce /vendor/ramdisk/app/hq/bin/Npv32960 $1/hq/bin/Npv32960 0755
cpForce /vendor/ramdisk/app/hq/bin/TCS $1/hq/bin/TCS 0755
cpForce /vendor/ramdisk/app/hq/bin/TestServer $1/hq/bin/TestServer 0755
#cpForce /vendor/ramdisk/app/hq/bin/UpdateExt $1/hq/bin/UpdateExt 0755
cpForce /vendor/ramdisk/app/hq/bin/OBDMethod $1/hq/bin/OBDMethod 0755
#cpForce /vendor/ramdisk/app/hq/bin/DriveModel $1/hq/bin/DriveModel 0755
#cpForce /vendor/ramdisk/app/hq/bin/hqfilesbak $1/hq/bin/hqfilesbak 0755
#cpForce /vendor/ramdisk/app/hq/bin/SixAxis $1/hq/bin/SixAxis 0755
#cpForce /vendor/ramdisk/app/hq/bin/Vtdr $1/hq/bin/Vtdr 0755
cpForce /vendor/ramdisk/app/hq/bin/TTS $1/hq/bin/TTS 0755

#cpForce /vendor/ramdisk/app/mobileap_cfg.xml /etc/mobileap_cfg.xml 0644

cpForce /vendor/ramdisk/app/rcS $1/rcS 0750
cpForce /vendor/ramdisk/app/hq/sh/hqinit.hrc $1/hq/sh/hqinit.hrc 0750
cpForce /vendor/ramdisk/app/hq/sh/emmc_format.sh $1/hq/sh/emmc_format.sh 0750
cpForce /vendor/ramdisk/app/hq/sh/emmc_check.sh $1/hq/sh/emmc_check.sh 0750
cpForce /vendor/ramdisk/app/hq/sh/emmc_repair.sh $1/hq/sh/emmc_repair.sh 0750
cpForce /vendor/ramdisk/app/hq/sh/ringstart.sh $1/hq/sh/ringstart.sh 0750
cpForce /vendor/ramdisk/app/hq/sh/ringstop.sh $1/hq/sh/ringstop.sh 0750
cpForce /vendor/ramdisk/app/hq/sh/voicecallstart.sh $1/hq/sh/voicecallstart.sh 0750
cpForce /vendor/ramdisk/app/hq/sh/voicecallstop.sh $1/hq/sh/voicecallstop.sh 0750
cpForce /vendor/ramdisk/app/hq/sh/rcS $1/hq/sh/rcS 0750


cpForce /vendor/ramdisk/app/hq/drv/RFDrvLib.ko $1/hq/drv/RFDrvLib.ko 0750
cpForce /vendor/ramdisk/app/hq/drv/DataCenter.ko $1/hq/drv/DataCenter.ko 0750
cpForce /vendor/ramdisk/app/hq/drv/hqkt.ko $1/hq/drv/hqkt.ko 0750
cpForce /vendor/ramdisk/app/hq/drv/hqxcu.ko $1/hq/drv/hqxcu.ko 0750
cpForce /vendor/ramdisk/app/hq/drv/hqspi.ko $1/hq/drv/hqspi.ko 0750


#cpForce /vendor/ramdisk/app/hq/etc/AxisPlugLoad.txt $1/hq/etc/AxisPlugLoad.txt 0644
cpForce /vendor/ramdisk/app/hq/etc/BackupConfig.txt $1/hq/etc/BackupConfig.txt 0644
cpForce /vendor/ramdisk/app/hq/etc/canfilter_load.txt $1/hq/etc/canfilter_load.txt 0644
#cpForce /vendor/ramdisk/app/hq/etc/canfilter_sanyi.txt $1/hq/etc/canfilter_sanyi.txt 0644
#cpForce /vendor/ramdisk/app/hq/etc/canfilter_dpe11k.txt $1/hq/etc/canfilter_dpe11k.txt 0644
cpForce /vendor/ramdisk/app/hq/etc/canfilter_higer.txt $1/hq/etc/canfilter_higer.txt 0644
cpForce /vendor/ramdisk/app/hq/etc/JL.dbc $1/hq/etc/JL.dbc 0644
cpForce /vendor/ramdisk/app/hq/etc/dc_ini.txt $1/hq/etc/dc_ini.txt 0644
cpForce /vendor/ramdisk/app/hq/etc/dc_perip_ini.txt $1/hq/etc/dc_perip_ini.txt 0644
cpForce /vendor/ramdisk/app/hq/etc/hqcomhub_ini.txt $1/hq/etc/hqcomhub_ini.txt 0644
cpForce /vendor/ramdisk/app/hq/etc/default.prop $1/hq/etc/default.prop 0644
cpForce /vendor/ramdisk/app/hq/etc/info.prop $1/hq/etc/info.prop 0644
cpForce /vendor/ramdisk/app/hq/etc/plug_load.txt $1/hq/etc/plug_load.txt 0644
#cpForce /vendor/ramdisk/app/hq/etc/dongpue11k.dbc $1/hq/etc/dongpue11k.dbc 0644
#cpForce /vendor/ramdisk/app/hq/etc/dongpu_em19.dbc $1/hq/etc/dongpu_em19.dbc 0644
cpForce /vendor/ramdisk/app/hq/etc/PhoneBook $1/hq/etc/PhoneBook 0644
#cpForce /vendor/ramdisk/app/hq/etc/DriveModelPlugCfg.txt $1/hq/etc/DriveModelPlugCfg.txt 0644
cpForce /vendor/ramdisk/app/hq/etc/ElectricFenceCfg.txt $1/hq/etc/ElectricFenceCfg.txt 0644
cpForce /vendor/ramdisk/app/hq/etc/j1939_config.txt $1/hq/etc/j1939_config.txt 0644
#cpForce /vendor/ramdisk/app/hq/etc/obdmethod.pubkey.pem $1/hq/etc/obdmethod.pubkey.pem 0644
#cpForce /vendor/ramdisk/app/hq/etc/SanYi.dbc $1/hq/etc/SanYi.dbc 0644
cpForce /vendor/ramdisk/app/hq/etc/JL.dbc $1/hq/etc/JL.dbc 0644

cpForce /vendor/ramdisk/app/hq/etc/GbosUpDownFilterCfg.txt $1/hq/etc/GbosUpDownFilterCfg.txt 0644
cpForce /vendor/ramdisk/app/hq/etc/transcan_config.txt $1/hq/etc/transcan_config.txt 0644
cpForce /vendor/ramdisk/app/hq/etc/CANDMCode.txt $1/hq/etc/CANDMCode.txt 0644
cpForce /vendor/ramdisk/app/hq/etc/faultconfig.txt $1/hq/etc/faultconfig.txt 0644
cpForce /vendor/ramdisk/app/hq/etc/KlFileTranPathCfg.txt $1/hq/etc/KlFileTranPathCfg.txt 0644
cpForce /vendor/ramdisk/app/hq/etc/EID.BIN $1/hq/etc/EID.BIN 0644
#cpForce /vendor/ramdisk/app/hq/etc/AxisPlugLoad.txt $1/hq/etc/AxisPlugLoad.txt 0644


#cpForce /vendor/ramdisk/app/hq/plug/PlugFenceDongPu.so $1/hq/plug/PlugFenceDongPu.so 0644
#cpForce /vendor/ramdisk/app/hq/plug/PlugSixAxisDongPu.so $1/hq/plug/PlugSixAxisDongPu.so 0644
cpForce /vendor/ramdisk/app/hq/plug/can/PlugFactoryTest.so $1/hq/plug/can/PlugFactoryTest.so 0644
cpForce /vendor/ramdisk/app/hq/plug/can/PlugHigerCommon.so $1/hq/plug/can/PlugHigerCommon.so 0644
cpForce /vendor/ramdisk/app/hq/plug/can/PlugHigerElectric.so $1/hq/plug/can/PlugHigerElectric.so 0644
cpForce /vendor/ramdisk/app/hq/plug/can/PlugHigerLimitSpeed.so $1/hq/plug/can/PlugHigerLimitSpeed.so 0644
cpForce /vendor/ramdisk/app/hq/plug/can/PlugHigerTradition.so $1/hq/plug/can/PlugHigerTradition.so 0644
cpForce /vendor/ramdisk/app/hq/plug/can/PlugHigerAebs.so $1/hq/plug/can/PlugHigerAebs.so 0644
#cpForce /vendor/ramdisk/app/hq/plug/PlugSanyhiTrunCorner.so $1/hq/plug/PlugSanyhiTrunCorner.so 0644
cpForce /vendor/ramdisk/app/hq/plug/can/PlugDBC.so $1/hq/plug/can/PlugDBC.so 0644
#cpForce /vendor/ramdisk/app/hq/plug/PlugSanyhiDriverModel.so $1/hq/plug/PlugSanyhiDriverModel.so 0644
#cpForce /vendor/ramdisk/app/hq/plug/PlugFenceSanyhi.so $1/hq/plug/PlugFenceSanyhi.so 0644
#cpForce /vendor/ramdisk/app/hq/plug/can/PlugTransCan.so $1/hq/plug/can/PlugTransCan.so 0644
#cpForce /vendor/ramdisk/app/hq/plug/can/PlugSany.so $1/hq/plug/can/PlugSany.so 0644
cpForce /vendor/ramdisk/app/hq/plug/can/PlugJ1939.so $1/hq/plug/can/PlugJ1939.so 0644
cpForce /vendor/ramdisk/app/hq/plug/can/PlugHigerObd.so $1/hq/plug/can/PlugHigerObd.so 0644
cpForce /vendor/ramdisk/app/hq/plug/can/PlugRecCanFrm.so $1/hq/plug/can/PlugRecCanFrm.so 0644
#cpForce /vendor/ramdisk/app/hq/plug/can/PlugDongPuE17.so $1/hq/plug/can/PlugDongPuE17.so 0644

cpForce /vendor/ramdisk/app/hq/tool/ssh.zip $1/hq/tool/ssh.zip 0644
cpForce /vendor/ramdisk/app/hq/sh/runssh.sh $1/hq/sh/runssh.sh 0750

cpForce /vendor/ramdisk/app/hq/sh/hqboot.sh $1/hq/sh/hqboot.sh 0750
cpForce /vendor/ramdisk/app/hq/lib/libse.so $1/hq/lib/libse.so 0750

}

CURR_HD_VER=$(hqgetprop ro.tbox.hardware.version)

if [ ${CURR_HD_VER} != ${TARGET_HD_VER} ]; then
    echo "ERROR HD .............."
    return
fi

if [ -e /etc/init.d/time_serviced ]; then
    mv /etc/init.d/time_serviced /etc/init.d/time_serviced_
fi

createRamdisk 32m

mkdirPrePare /media/card/back
mkdirPrePare /system
mkdirPrePare /vendor/app

rm -rf /vendor/ramdisk/app
unzip ${STORAGE_PATH}autoruntbox.zip -d /vendor/ramdisk/

if [ ! -e /usr/lib/libse.so ]; then
    echo "No libse.so file in TBOX" >> /vendor/data/libse.log
    if [ ! -e /vendor/ramdisk/app/hq/lib/libse.so ]; then
        echo "No libse.so file in 4GPackage" >> /vendor/data/libse.log
        rm -rf /vendor/ramdisk/
        rm -rf ${STORAGE_PATH}autoruntbox.zip
        sync
        exit 0
    fi
fi

# 修改hqboot.sh，对libse.so进行三备份检测
sed -i '/insmod \/vendor\/app\/hq\/drv\/RFDrvLib.ko/i\cpIfNotExists /vendor/app/hq/lib/libse.so /usr/lib/libse.so 0644 \
cpIfNotExists /system/hq/lib/libse.so /usr/lib/libse.so 0644 \
cpIfNotExists /media/card/back/hq/lib/libse.so /usr/lib/libse.so 0644' /vendor/ramdisk/app/hq/sh/hqboot.sh

DoCopy /media/card/back
DoCopy /system
DoCopy /vendor/app

cpForce /vendor/ramdisk/2B80.img /vendor/data/McuUpdate/2B80.new 0664

#新的远程更新程序需要在脚本里判断是否有MCU升级
if [ -e /vendor/data/McuUpdate/2B80.new ]; then
	SetHQProp persist.tbox.update.unit.mask 3
	echo "McuUpdate Exist" >> /vendor/data/remote_update.log
else
	SetHQProp persist.tbox.update.unit.mask 0
	echo "McuUpdate Not Exist" >> /vendor/data/remote_update.log
fi

sync

rm -rf /vendor/ramdisk/
rm -rf ${STORAGE_PATH}autoruntbox.zip

date >> /vendor/data/remote_update.log
uptime >> /vendor/data/remote_update.log

sync

touch /vendor/data/update_succeed.flag

