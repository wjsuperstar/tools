#!/usr/bin/python
# -*- coding: UTF-8 -*-
# auth: WuJian  20191217
# desc: 解析陕汽can存储报文

import struct
import sys

print(sys.argv[0])
print(sys.argv[1])
print(sys.argv[2])
FileName=sys.argv[1]
ParseFlg=sys.argv[2]
DataLen = 18

g_can_keys = ("can_id", "can_time", "can_len", "can_type", "can_fmt", "can_data")
g_can_name = ('CAN ID', '时间', '数据长度', '帧类型', '帧格式', '帧数据')

class ParseOne:
    def __init__(self, s, tot_len):
        self.__can_data = {}
        self.__can_data_desc = dict(zip(g_can_keys, g_can_name))

        data = s
        idx = 0
        
        if tot_len == DataLen:
            id,h,m,s,ms,f,data = struct.unpack(">IBBBHB8s", data[idx:idx+DataLen])
            self.__can_data[g_can_keys[idx]] = hex(id);
            idx += 1
            
            self.__can_data[g_can_keys[idx]] = hex(h)[2:]+':'+hex(m)[2:]+':'+hex(s)[2:]+' '+str(ms);
            idx += 1
            self.__can_sec = int(hex(h)[2:], 10)*3600+int(hex(m)[2:], 10)*60+int(hex(s)[2:], 10);
            
            self.__can_data[g_can_keys[idx]] = f & 0x0f;
            idx += 1
            
            if (f >> 4) == 0:
                self.__can_data[g_can_keys[idx]] = u"标准帧";
            else:
                self.__can_data[g_can_keys[idx]] = u"扩展帧";
            idx += 1
            
            if (f >> 4) == 0:
                self.__can_data[g_can_keys[idx]] = u"数据帧";
            else:
                self.__can_data[g_can_keys[idx]] = u"远程帧";
            idx += 1
            data_list = [hex(i) for i in data]
            self.__can_data[g_can_keys[idx]] = ' '.join(data_list);
            idx += 1
        else:
            print("data len error.")
    
    def GetTime(self):
        return self.__can_data['can_time']    
    def GetSec(self):
        return self.__can_sec
    def GetData(self):
        return self.__can_data
    def GetDesc(self):
        return self.__can_data_desc
    def display(self):
        print("\nCAN数据:")
        for i in g_can_keys:
            print(self.__can_data_desc[i], self.__can_data[i], sep=':', end = ', ')

def main():
    count = 0
    last_sec = 0
    last_time = ''
    with open(FileName, mode='rb') as fd:
        packet = fd.read(DataLen)
        while len(packet) >= DataLen:
            count += 1
            #print("\n\n\n读取第%d条:" % count)
            #print(packet)
            obj = ParseOne(packet, len(packet))
            packet = fd.read(DataLen)
            
            if ParseFlg == 'display':
                obj.display()
            elif ParseFlg == 'check' and last_sec > 0 and obj.GetSec()-last_sec > 1:
                print("---------> time diff more than 1 sec, cur_time=", obj.GetTime(), "last_time:", last_time)
                print(obj.GetSec(), last_sec)
            last_time= obj.GetTime()
            last_sec = obj.GetSec()
            
            
if __name__ == '__main__':
    main()