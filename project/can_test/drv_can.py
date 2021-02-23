from ctypes import *
import time

# CAN1，CAN2取值
USB_CAN1 = 3
USB_CAN2 = 4
# 波特率
BAUD_250K = 1
BAUD_500K = 0

class VciCfg(Structure):
    _fields_ = [('AccCode', c_ulong),
                ('AccMask', c_ulong),
                ('Reserved', c_ulong),
                ('Filter', c_ubyte),
                ('Timing0', c_ubyte),
                ('Timing1', c_ubyte),
                ('Mode', c_ubyte)]


class VciCanObj(Structure):
    _fields_ = [('ID', c_uint),
                ('TimeStamp', c_uint),
                ('TimeFlag', c_byte),
                ('SendType', c_byte),
                ('RemoteFlag', c_byte),
                ('ExternFlag', c_byte),
                ('DataLen', c_byte),
                ('Data', c_ubyte*8),
                ('Reserved', c_ubyte*3)]

# 周立功CAN设备驱动类
class ZlgCanDev:
    def __init__(self, baud = BAUD_500K, chn = USB_CAN1, lib_path="ControlCAN.dll"):
        self.__baud     = baud
        self.__chn      = chn
        self.__lib_path = lib_path
        self.__opened   = False
        # 初始化can属性
        self.__vic = VciCfg()
        self.__vic.AccCode = 0x00000000
        self.__vic.AccMask = 0xffffffff
        self.__vic.Filter = 0
        self.__vic.Timing0 = self.__baud
        self.__vic.Timing1 = 0x1c
        self.__vic.Mode = 0
        # 初始化can帧结构
        self.__vco = VciCanObj()
        self.__vco.ID = 0
        self.__vco.SendType = 0   #发送格式：0:正常发送 1:单次正常发送 2:自发自收 3.单次自发自收
        self.__vco.RemoteFlag = 0 #帧格式：0：数据帧 1：远程帧
        self.__vco.ExternFlag = 0 #帧类型：0：标准帧 1为扩展帧
        self.__vco.DataLen = 8
        
        self.__vco_rcv = VciCanObj()
        

    def open(self):
        if not self.__opened:
            self.__canLib = windll.LoadLibrary('ControlCAN.dll')
            ret = self.__canLib.VCI_OpenDevice(self.__chn, 0, 0)
            if ret == 1:
                print("open can dev success.")
            else:
                print("open can dev fail.")
            #print("chn=%d, baud=%d" % (self.__chn, self.__baud))
            self.__canLib.VCI_InitCAN(self.__chn, 0, 0, pointer(self.__vic))
            self.__canLib.VCI_StartCAN(self.__chn, 0, 0)
            self.__canLib.VCI_ClearBuffer(self.__chn, 0, 0)

            self.__opened = True
        return self.__opened

    def write(self, id, data, send_type = 0):
        ret = 0
        if self.open():
            self.__vco.ID  = id
            if id > 0x7ff:
                self.__vco.ExternFlag = 1
            else:
                self.__vco.ExternFlag = 0
            
            self.__vco.DataLen = len(data)
            if self.__vco.DataLen > 8:
                self.__vco.DataLen = 8
            
            for i in range(self.__vco.DataLen):
                self.__vco.Data[i]    = data[i]
            self.__vco.SendType= send_type
            #返回实际发送成功的帧数
            #print('id=', hex(id), 'data=', data)
            ret =  self.__canLib.VCI_Transmit(self.__chn, 0, 0, pointer(self.__vco), 1)
        return ret
    # 返回元组(帧个数，帧id，帧内容)
    def read(self):
        id   = ''
        data = []
        ret  = self.__canLib.VCI_Receive(self.__chn, 0, 0, pointer(self.__vco_rcv), 1, 500)
        if ret > 0:
            id = self.__vco_rcv.ID
            data = list(self.__vco_rcv.Data)
        return (ret, id, data)

def main():
    co = ZlgCanDev()
    for i in range(100):
        data = [1, 4, 7, 2, 5, 8, 3, 6]
        co.write(0x1234, data)
        time.sleep(0.001)
    
    for i in range(1000):
        ret, id, data = co.read()
        if ret > 0:
            print("ID=", id, "len=", len(data), "data=", data)
        time.sleep(0.01)

if __name__ == '__main__':
    main()