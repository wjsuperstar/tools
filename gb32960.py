#!/usr/bin/python
# -*- coding: UTF-8 -*-
# auth: WuJian  20191010

import re

FileName=r'D:\test\test_py\npv_data.txt'

class GbParse0xF1:
    #定义私有属性,私有属性在类外部无法直接进行访问
    __event_cmd = 0
    __event_serial = 0
    __event_opt = 0  #3进区域，4出区域
    __event_time = 0
    __event_longi = 0
    __event_lat = 0
    __event_line_no = 0
    __event_speed = 0
    
    #定义构造方法
    def __init__(self, str):
        data = str
        idx = 0
        self.__event_cmd = int(data[idx:idx+4], 16)
        idx += 4
        self.__event_serial = int(data[idx:idx+8], 16)
        idx += 8
        self.__event_opt = int(data[idx:idx+2], 16)
        idx += 4
        self.__event_time = int(data[idx:idx+8], 16)
        idx += 8
        self.__event_longi = int(data[idx:idx+8], 16)
        idx += 8
        self.__event_lat = int(data[idx:idx+8], 16)
        idx += 8
        self.__event_line_no = int(data[idx:idx+8], 16)
        idx += 16
        self.__event_speed = int(data[idx:idx+2], 16)
        idx += 2
    
    def GetGpsPoint(self):
        print("%f,%f"%(self.__event_lat/1e6, self.__event_longi/1e6))
    
    def display(self):
        print("Ctx: sub=%X, serial=%d, opt=%d, time=%d, longi=%d, lat=%d, lineno=%d, speed=%d" %(self.__event_cmd, self.__event_serial, self.__event_opt, 
        self.__event_time, self.__event_longi, self.__event_lat, self.__event_line_no, self.__event_speed))

class Gb32960Parse:
    #定义私有属性,私有属性在类外部无法直接进行访问
    __cmd = 0
    __vin = ''
    __encrypt = 0  #0x01：数据不加密；0x02：数据经过RSA算法加密；0x03:数据经过AES128位算法加密
    __data_len = 0
    
    #定义构造方法
    def __init__(self, str):
        data = str
        idx = 4
        self.__cmd = int(data[idx:idx+2], 16)
        idx += 4
        
        tmp_vin = data[idx:idx+34]
        for i in range(0, len(tmp_vin), 2):
            self.__vin += chr(int(tmp_vin[i:i+2], 16))
        idx += 34
        
        self.__encrypt = int(data[idx:idx+2], 16)
        idx += 2
        
        self.__data_len = int(data[idx:idx+4], 16)
        idx += 4
        
        #以下是0xF1的自定义内容
        self.__data_f1 = GbParse0xF1(data[idx:])
        
        # 校验码 TODO
        
    def display(self):
        print("Ctx: cmd=%X, vin=%s, encry=%d, len=%d" %(self.__cmd, self.__vin, self.__encrypt, self.__data_len))
        self.__data_f1.display()
    
    def GetGpsPoint(self):
        self.__data_f1.GetGpsPoint()

def main():
    with open(FileName) as fd:
        for line in fd:
            try:
                data = re.search( r'(2323.*)', line).group(1)
                #print(data)
                #Gb32960Parse(data).GetGpsPoint()
                Gb32960Parse(data).display()
            except AttributeError:
                # 忽略不合法的数据
                continue

if __name__ == '__main__':
    main()