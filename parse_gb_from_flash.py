#!/usr/bin/python
# -*- coding: UTF-8 -*-
# auth: WuJian  20191010

import struct

FileName=r'D:\test\test_py\tbox_data.bin'


# 定位数据
class GbParse0x05:
    __locationed = 0
    __lat   = 0
    __longi = 0
    
    
    #定义构造方法
    def __init__(self, s, len):
        data = s
        idx = 0
        #print(data[idx:])
        self.__locationed = struct.unpack(">B", data[idx:idx+1])[0]
        idx += 1
        self.__longi = struct.unpack(">I", data[idx:idx+4])[0]
        idx += 4
        self.__lat = struct.unpack(">I", data[idx:idx+4])[0]
        idx += 4
        
    def display(self):
        print("0x05: location=%d, lat=%f, longi=%f" %(self.__locationed, self.__lat/1e6, self.__longi/1e6))
# 报警数据
class GbParse0x07:
    
    __bms_fault_list = []
    __monitor_fault_list = []
    __engine_fault_list = []
    __other_fault_list = []
    #定义构造方法
    def __init__(self, s, len):
        data = s
        idx = 0
        #print(data[idx:])
        # 最高报警等级
        self.__fault_level = struct.unpack(">B", data[idx:idx+1])[0]
        idx += 1
        # 通用报警标志
        self.__common_fault = struct.unpack(">I", data[idx:idx+4])[0]
        idx += 4
        # 可充电蓄能装置故障总数
        self.__bms_fault_num = struct.unpack(">B", data[idx:idx+1])[0]
        idx += 1
        if self.__bms_fault_num > 0:
            for i in range(self.__bms_fault_num):
                self.__bms_fault_list.append(struct.unpack(">I", data[idx:idx+4])[0])
                idx += 4
        # 电机故障总数
        self.__monitor_fault_num = struct.unpack(">B", data[idx:idx+1])[0]
        idx += 1
        if self.__monitor_fault_num > 0:
            for i in range(self.__monitor_fault_num):
                self.__monitor_fault_list.append(struct.unpack(">I", data[idx:idx+4])[0])
                idx += 4
        # 发动机故障总数
        self.__engine_fault_num = struct.unpack(">B", data[idx:idx+1])[0]
        idx += 1
        if self.__engine_fault_num > 0:
            for i in range(self.__engine_fault_num):
                self.__engine_fault_list.append(struct.unpack(">I", data[idx:idx+4])[0])
                idx += 4
        # 其他故障总数
        self.__other_fault_num = struct.unpack(">B", data[idx:idx+1])[0]
        idx += 1
        if self.__other_fault_num > 0:
            for i in range(self.__other_fault_num):
                self.__other_fault_list.append(struct.unpack(">I", data[idx:idx+4])[0])
                idx += 4
        
    def display(self):
        print("0x07: fault level=%d, common fault=0x%X, bms=%d, monitor=%d, engine=%d, other=%d" 
            %(self.__fault_level, self.__common_fault, self.__bms_fault_num, self.__monitor_fault_num, self.__engine_fault_num, self.__other_fault_num))

class GbMainParse:
    # 数据采集时间
    __time = ''
    # 数据块id
    __block_id = 0
    

    #定义构造方法
    def __init__(self, s, len):
        data = s
        idx  = 0
        y,m,d,h,min,s = struct.unpack("<BBBBBB", data[idx:idx+6])
        idx += 6
        len -= 6
        self.__time = str(2000+y)+'-'+str(m)+'-'+str(d)+' '+str(h)+':'+str(min)+':'+str(s)
        print(self.__time)
        
        # 解析各个数据块
        while len > 0:
            self.__block_id = struct.unpack("<B", data[idx:idx+1])[0]
            idx += 1
            print("__block_id=", self.__block_id)
            if self.__block_id == 0x05:
                self.__block = GbParse0x05(data[idx:], len)
                idx += 9
                len -= 9
            elif self.__block_id == 0x07:
                self.__block = GbParse0x07(data[idx:], len)
                idx += 9
                len -= 9
            elif self.__block_id == 0x01:
                self.__block = GbParse0x07(data[idx:], len)
                idx += 9
                len -= 9
                break
            self.__block.display()
            
        # 校验码 TODO
        

def main():
    with open(FileName, mode='rb') as fd:
        packet = fd.read(1024)
        while packet != '':
            data_len = struct.unpack("<H", packet[10:12])[0]
            print("data_len=", data_len)
            GbMainParse(packet[28:], data_len)
            break
            

if __name__ == '__main__':
    main()