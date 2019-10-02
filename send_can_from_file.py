import time
import csv
from ctypes import *

VCI_DEV_USBCAN1 = 3
VCI_DEV_USBCAN2 = 4

VCI_DEV_BAUD = 1 # 0 : 500k, 1 : 250k 
FileName=r'D:\tools\python368\1111.csv'
#FileName=r'playback.txt'
FileFormat="csv"   #txt, csv

class _VCI_INIT_CONFIG(Structure):
    _fields_ = [('AccCode', c_ulong),
                ('AccMask', c_ulong),
                ('Reserved', c_ulong),
                ('Filter', c_ubyte),
                ('Timing0', c_ubyte),
                ('Timing1', c_ubyte),
                ('Mode', c_ubyte)]


class _VCI_CAN_OBJ(Structure):
    _fields_ = [('ID', c_uint),
                ('TimeStamp', c_uint),
                ('TimeFlag', c_byte),
                ('SendType', c_byte),
                ('RemoteFlag', c_byte),
                ('ExternFlag', c_byte),
                ('DataLen', c_byte),
                ('Data', c_byte*8),
                ('Reserved', c_byte*3)]


vic = _VCI_INIT_CONFIG()
vic.AccCode = 0x00000000
vic.AccMask = 0xffffffff
vic.Filter = 0
vic.Timing0 = VCI_DEV_BAUD
vic.Timing1 = 0x1c
vic.Mode = 0

vco = _VCI_CAN_OBJ()
#vco.ID = 0x1810d4f4
vco.SendType = 0   #发送格式：0:正常发送 1:单次正常发送 2:自发自收 3.单次自发自收
vco.RemoteFlag = 0 #帧格式：0：数据帧 1：远程帧
vco.ExternFlag = 0 #帧类型：0：标准帧 1为扩展帧
vco.DataLen = 8
vco.Data = (0x1, 0x4c, 0x01, 0x2, 0x4c, 0x01, 0x02, 0x00)

canLib = windll.LoadLibrary('ControlCAN.dll')
print('打开设备: %d' % (canLib.VCI_OpenDevice(VCI_DEV_USBCAN1, 0, 0)))
print('初始化: %d' % (canLib.VCI_InitCAN(VCI_DEV_USBCAN1, 0, 0, pointer(vic))))
print('启动: %d' % (canLib.VCI_StartCAN(VCI_DEV_USBCAN1, 0, 0)))
print('清空缓冲区: %d' % (canLib.VCI_ClearBuffer(VCI_DEV_USBCAN1, 0, 0)))

can_id   = []
can_data = []

def parse_csv():
    with open(FileName) as csvfile:
        csv_reader = csv.reader(csvfile)  # 使用csv.reader读取csvfile中的文件
        header = next(csv_reader)  # 读取第一行每一列的标题
        for row in csv_reader:  # 将csv 文件中的数据保存到can_data中
            can_id.append(row[3])
            can_data.append(row[7])
def parse_txt():
    with open(FileName) as fd:
        next(fd)
        for row in fd:
            td = row.split(r"  ")
            #print(td[6], td[12])
            can_id.append(td[6])
            can_data.append(td[12][1:])

if FileFormat == "csv":
    parse_csv()
elif FileFormat == "txt":
    parse_txt()

for i in range(len(can_id)):
    time.sleep(0.01);
    #vco.ID = eval(can_id[i])
    vco.ID = int(can_id[i], 16)
    d = can_data[i].split(" ")
    print("id=", can_id[i], "data=", d)
    for j in range(8):
        vco.Data[j] = int(d[j], 16)

    print('发送: %d' % (canLib.VCI_Transmit(VCI_DEV_USBCAN1, 0, 0, pointer(vco), 1)))

