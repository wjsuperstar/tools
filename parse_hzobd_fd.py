#!/usr/bin/python
# -*- coding: UTF-8 -*-
# auth: WuJian  2020-05-14
# desc: 解析以字符串形式存储的杭州地标数据文件

import struct
import time
import datetime
import re
import os
import sys

print("使用格式： python xx.py 目录名(递归解析目录内的数据文件)")
print("解析目录:", sys.argv[1])

DirName =sys.argv[1]


# 以下元组是根据杭州地标协议定义
g_head_keys = ('start_symbol', 'cmd', 'vin',         'soft_ver',     'encrypt',       'data_len')
g_head_name = ('起始符',  '命令单元', '车辆识别号', '终端软件版本号', '数据加密方式',     '数据单元长度')

g_data0x01_keys = ('start_symbol', 'mil_status', 'dia_support', 'dia_ready',     'vin',           'soft_id',          'cvn',      'iupr',  'dm_count',    'dm_list')
g_data0x01_name = ('OBD诊断协议',  'MIL状态',    '诊断支持状态', '诊断就绪状态', '车辆识别码',   '软件标定识别号', '标定验证码', 'IUPR值', '故障码总数', '故障码列表')

g_data0x02_keys = ('veh_speed', 'atmospheric', 'actual_tor', 'friction_tor', 'engine_rev', 'fuel_flow',    'scr_up_nox',      'scr_down_nox',           'urea_tank_level', 'intake_flow', 'scr_up_temp', 'scr_down_temp', 'dpf_pressure', 'coolant_temp', 'oil_tank_level', 'gps_status', 'gps_long', 'gps_lat', 'odo')
g_data0x02_name = ('车速',      '大气压力',    '实际扭矩',     '摩擦扭矩',   '转速',     '发动机燃料流量', 'SCR上游NOx传感器输出值', 'SCR下游NOx传感器输出值', '尿素箱液位', '进气量', 'SCR入口温度',    'SCR出口温度', 'DPF压差',       '冷却液温度',     '油箱液位',      '定位状态',     '经度',    '纬度', '累计里程')
g_data0x02_fact = (0.00390625,   0.5,           1,                  1,        0.125,            0.05,            0.05,                  0.05,                       0.4,         0.05,      0.03125,           0.03125,      0.1,           1,                0.4,               1,        0.000001,  0.000001,  0.1 )
g_data0x02_offset = (0,          0,             -125,               -125,     0,                0,               -200,                  -200,                       0,            0,        -273,               -273,          0,           -40,                0,               0,         0,          0,       0)

g_data0x80_keys = ('tor_mode', 'acce_pedal', 'total_oil_consumption', 'urea_tank_temp', 'actual_urea_injection', 'total_urea_consumption', 'dpf_exh_temp')
g_data0x80_name = ('扭矩模式',  '油门踏板',    '累计油耗',           '尿素箱温度',       '实际尿素喷射量',     '累计尿素消耗',             'DPF排气温度')
g_data0x80_fact = (  1,              0.4,         0.5,                  1,                   0.01,                  1,                      0.03125)
g_data0x80_offset = (0,              0,           0,                    -40,                 0,                     0,                      -273)

g_data0x81_keys = ('total_run_time',     'instant_fuel', 'opacity',    'particulates',  'pm_k_value',    'manifold_temp', 'command_tor',  'hydraulics_pressure',  'hand.brake', 'foot.brake')
g_data0x81_name = ('发动机总运行时间',    '瞬时油耗',    '不透光度',     '颗粒物浓度',   '光吸收系数',   '进气歧管温度',   '指令扭矩',         '机油压力',          '手刹状态',    '脚刹状态')
g_data0x81_fact = (0.05,                    0.05,           0.1,            0.1,            0.01,             0.1,              1,              4,                  1,                  1)
g_data0x81_offset = (0,                     0,                0,            0,              0,                -40,            -125,              0,                  0,                  0)

g_data0x82_keys = (0x01,                   0x02,         0x03,          0x04,        0x05,            0x06,     0x07,      0x08,      0x09,       0x0A)
g_data0x82_name = ('后装传感器支持', '后装传感器就绪', 'GNSS天线状态', '小区信息', '联网信号强度',  '加速度', '角速度', '数据来源', '区域信息', 'GPS方向')


# 消息头
class GbParseHead:
    
    def __init__(self, s, len_out):
        self.__head_data = {}
        self.__head_desc = dict(zip(g_head_keys, g_head_name))

        data = s
        idx = 0
        #print(data[idx:])
        veh_value = struct.unpack(">2sB17sBBH", data[idx:idx+24])
        self.__head_data = dict(zip(g_head_keys, veh_value))
        idx += 24
        len_out[0] = idx

    def GetData(self):
        return self.__head_data
    def GetDesc(self):
        return self.__head_desc
    def GetDataLen(self):
        return self.__head_data["data_len"]
    def display(self):
        print("\n\n消息头:")
        for i in g_head_keys:
            print(self.__head_desc[i], self.__head_data[i], sep=':', end = ', ')

# 采集时间
class GbParseSimpleTime:
    
    def __init__(self, s, len_out):
        data = s
        idx = 0
        y,m,d,hh,mm,ss,no = struct.unpack(">BBBBBBH", data[idx:idx+8])
        self.__dt=datetime.datetime(2000+y, m, d, hh, mm, ss, 0)
        self.__serial_no = no
        idx += 8
        len_out[0] = idx

    def display(self):
        print("\n采集时间:", self.__dt.strftime('%Y-%m-%d %H:%M:%S'), "流水号:", self.__serial_no, end = ', ')
        
# OBD信息
class GbParse0x01:
    def __init__(self, s, len_out):
        self.__0x01_data = {}
        self.__0x01_desc = dict(zip(g_data0x01_keys, g_data0x01_name))

        data = s
        idx = 0
        #print(data[idx:])
        veh_value = struct.unpack(">BBHH17s18s18s36sB", data[idx:idx+96])
        self.__0x01_data = dict(zip(g_data0x01_keys, veh_value))
        idx += 96
        
        # 故障码列表
        engine_fault_num = self.__0x01_data['dm_count']
        fault_list = []
        if engine_fault_num > 0:
            for i in range(engine_fault_num):
                fault_list.append(struct.unpack(">I", data[idx:idx+4])[0])
                idx += 4
        self.__0x01_data['dm_list'] = fault_list
        
        len_out[0] = idx

    def GetData(self):
        return self.__0x01_data
    def GetDesc(self):
        return self.__0x01_desc
    def display(self):
        print("\nOBD信息:")
        for i in g_data0x01_keys:
            print(self.__0x01_desc[i], self.__0x01_data[i], sep=':', end = ', ')

# 基础数据流
class GbParse0x02:
    
    def __init__(self, s, len_out):
        self.__0x02_data = {}
        self.__0x02_desc = dict(zip(g_data0x02_keys, g_data0x02_name))
        self.__0x02_fact   = dict(zip(g_data0x02_keys, g_data0x02_fact))
        self.__0x02_offset = dict(zip(g_data0x02_keys, g_data0x02_offset))

        data = s
        idx = 0
        #print(data[idx:])
        veh_value = struct.unpack(">HBBBHHHHBHHHHBBBIII", data[idx:idx+37])
        self.__0x02_data = dict(zip(g_data0x02_keys, veh_value))
        idx += 37
        len_out[0] = idx

    def GetData(self):
        return self.__0x02_data
    def GetDesc(self):
        return self.__0x02_desc
    def display(self):
        print("\n基础数据流:")
        for i in g_data0x02_keys:
            print(self.__0x02_desc[i], self.__0x02_data[i]*self.__0x02_fact[i]+self.__0x02_offset[i], sep=':', end = ', ')

# 补充数据流
class GbParse0x80:
    
    def __init__(self, s, len_out):
        self.__0x80_data = {}
        self.__0x80_desc = dict(zip(g_data0x80_keys, g_data0x80_name))
        self.__0x80_fact   = dict(zip(g_data0x80_keys, g_data0x80_fact))
        self.__0x80_offset = dict(zip(g_data0x80_keys, g_data0x80_offset))
        
        data = s
        idx = 0
        #print(data[idx:])
        veh_value = struct.unpack(">BBIBIIH", data[idx:idx+17])
        self.__0x80_data = dict(zip(g_data0x80_keys, veh_value))
        idx += 17
        len_out[0] = idx

    def GetData(self):
        return self.__0x80_data
    def GetDesc(self):
        return self.__0x80_desc
    def display(self):
        print("\n补充数据流:")
        for i in g_data0x80_keys:
            print(self.__0x80_desc[i], self.__0x80_data[i]*self.__0x80_fact[i]+self.__0x80_offset[i], sep=':', end = ', ')

# 补充数据流2
class GbParse0x81:
    
    def __init__(self, s, len_out):
        self.__0x81_data = {}
        self.__0x81_desc = dict(zip(g_data0x81_keys, g_data0x81_name))
        self.__0x81_fact   = dict(zip(g_data0x81_keys, g_data0x81_fact))
        self.__0x81_offset = dict(zip(g_data0x81_keys, g_data0x81_offset))

        data = s
        idx = 0
        #print(data[idx:])
        veh_value = struct.unpack(">IHHHHHBBBB", data[idx:idx+18])
        self.__0x81_data = dict(zip(g_data0x81_keys, veh_value))
        idx += 18
        len_out[0] = idx

    def GetData(self):
        return self.__0x81_data
    def GetDesc(self):
        return self.__0x81_desc
    def display(self):
        print("\n补充数据流2:")
        for i in g_data0x81_keys:
            print(self.__0x81_desc[i], self.__0x81_data[i]*self.__0x81_fact[i]+self.__0x81_offset[i], sep=':', end = ', ')
# 终端信息
class GbParse0x82:
    
    def __init__(self, s, len_in, len_out):
        self.__0x82_data = {}
        self.__0x82_desc = dict(zip(g_data0x82_keys, g_data0x82_name))
        
        data = s
        idx = 0
        while idx < len_in:
            block_len = data[idx+1]
            self.__0x82_data[data[idx]] = data[idx+2:idx+2+block_len]
            idx += (block_len + 2)
        len_out[0] = idx
    def GetData(self):
        return self.__0x82_data
    def GetDesc(self):
        return self.g_data0x82_desc
    def display(self):
        print("\n终端信息:")
        for i in g_data0x82_keys:
            print(self.__0x82_desc[i], self.__0x82_data[i], sep=':', end = ', ')
            
class GbMainParse:
    
    __time_sec = 0
    #定义构造方法
    def __init__(self, s, tot_len):
        data = s
        tot_len -= 1    #去掉校验码
        idx = 0
        used_len = [0]
        self.one_pack = []
        #消息头
        self.one_pack.append(GbParseHead(data[idx:], used_len))
        tot_len -= used_len[0]
        idx += used_len[0]
        if tot_len == self.one_pack[0].GetDataLen():
            # 日期时间, 流水号
            self.one_pack.append(GbParseSimpleTime(data[idx:], used_len))
            tot_len -= used_len[0]
            idx += used_len[0]
            
            # 解析各个数据块
            while tot_len > 0:
                block_id = struct.unpack("<B", data[idx:idx+1])[0]
                idx += 1
                tot_len -= 1
                #print("\nblock_id=%d, idx=%d" % (block_id, idx))
                if block_id == 0x01:
                    self.one_pack.append(GbParse0x01(data[idx:], used_len))
                elif block_id == 0x02:
                    self.one_pack.append(GbParse0x02(data[idx:], used_len))
                elif block_id == 0x80:
                    self.one_pack.append(GbParse0x80(data[idx:], used_len))
                elif block_id == 0x81:
                    self.one_pack.append(GbParse0x81(data[idx:], used_len))
                elif block_id == 0x82:
                    #break
                    self.one_pack.append(GbParse0x82(data[idx:], tot_len, used_len))
                else:
                    print("Unkonw id, block_id=", block_id)
                    break
                idx += used_len[0]
                tot_len -= used_len[0]
                
                #print("\nused_len=", used_len[0], "idx=", idx, "hex_stream_len=", hex_stream_len)
                #break
        else:
            print("data len error, len by parse=%d, in param len=%d" % self.__data_len, data_unit_len)

    def display(self):
        for i in self.one_pack:
            i.display()
    def GetTimeSec(self):
        return self.__time_sec
    def GetTimeStr(self):
        return self.__dt.strftime('%Y-%m-%d %H:%M:%S')
            
def main():

    for root, dirs, files in os.walk(DirName):
        for name in files:
            file_name = os.path.join(root, name)
            print('-------------->open ', file_name)
            with open(file_name) as fd:
                for line in fd:
                    try:
                        data = re.search( r'(232302.*)', line).group(1)
                        if data:
                            # 将字符串转为bytes
                            hex_stream = b''
                            idx = 0
                            data = data.strip()
                            #print('len=', len(data))
                            #print(data)
                            while idx < len(data):
                                hex_stream += struct.pack(">B", int(data[idx:idx+2], 16))
                                idx += 2
                            #print("hex_stream_len=%d" % len(hex_stream))
                            #print(hex_stream)
                            obj = GbMainParse(hex_stream, len(hex_stream))
                            obj.display()
                    except AttributeError:
                        # 忽略不合法的数据
                        #print("invaid line.")
                        continue
                    #break #一行
            #break #一个文件
if __name__ == '__main__':
    main()