#!/usr/bin/python
# -*- coding: UTF-8 -*-
# auth: WuJian  20191225
# desc: 解析以字符串形式存储的32960国标数据文件

import struct
import time
import datetime
import re
import os
import sys

print("使用格式： python xx.py 目录名 解析标志")
print("解析目录:", sys.argv[1])
print("解析标志(1表示显示解析结果，2表示检测数据是否丢失):", sys.argv[2])
DirName =sys.argv[1]
ParseFlg=sys.argv[2]

# 以下元组是根据GB32960协议定义，不可更改。
g_head_keys = ('start_symbol', 'cmd', 'vin',         'soft_ver',     'encrypt',       'data_len')
g_head_name = ('起始符',  '命令单元', '车辆识别号', '终端软件版本号', '数据加密方式',     '数据单元长度')

g_gps_keys = ("locationed", "longi", "lat")
g_gps_name = ("定位状态", "经度", "纬度")

g_fault_keys = ("fault_level", "common_fault", "bms_num", "bms_list", "motor_num", "motor_list", "engine_num", "engine_list", "other_num", "other_list")
g_fault_name = ("最高报警等级", "通用报警标志", "可充电蓄能装置故障总数", "可充电蓄能装置故障代码列表", "电机故障总数", "电机故障代码列表", 
                "发动机故障总数", "发动机故障列表", "其他故障总数", "其他故障列表")

g_vehicle_keys = ("vehicle_stat", "charge_stat", "run_mode", "speed", "odo", "tot_volt", "tot_curr", "soc", "dcdc_stat", "gear", "resistance", "accel_pedal", "brake_pedal")
g_vehicle_name = ('车辆状态', '充电状态', '运行模式', '车速', '累计里程', '总电压', '总电流', 'SOC', 'DCDC', '档位', '绝缘电阻', '加速踏板', '制动踏板')

g_motor_keys = ("index", "status", "ctl_temp", "rev", "tor", "temp", "volt", "curr")
g_motor_name = ("驱动电机序号", "驱动电机状态", "驱动电控温度", "驱动电机转速", "驱动电机转矩", "驱动电机温度", "电控输入电压", "电控母线电流")

g_bms_volt_keys = ("sys_no", "volt", "curr", "tot_num", "start_idx", "now_num", "volt_list")
g_bms_volt_name = ("可充电储能子系统号", "可充电储能装置电压", "可充电储能装置电流", "单体蓄电池总数", "本帧起始电池序号", "本帧单体电池总数", "单体电池电压值")

g_bms_temp_keys = ("sys_no", "tot_num", "temp_list")
g_bms_temp_name = ("可充电储能子系统号", "温度探针个数", "温度探针值")

g_extreme_keys = ("max_volt_sys", "max_volt_idx", "max_volt_val", "min_volt_sys", "min_volt_idx", "min_volt_val",
                  "max_temp_sys", "max_temp_idx", "max_temp_val", "min_temp_sys", "min_temp_idx", "min_temp_val",)
g_extreme_name = ("最高电压电池子系统", "最高电压电池单体代号", "电池单体电压最高值", "最低电压电池子系统", "最低电压电池单体代号", "电池单体电压最低值", 
                  "最高温度子系统", "最高温度探针序号", "最高温度值", "最低温度子系统号", "最低温度探索针序号", "最低温度值")

g_engine_keys = ("status", "crank_rev", "cons_rate")
g_engine_name = ("发动机状态", "曲轴转速", "燃料消耗率")

g_fuel_bat_keys = ("volt", "curr", "consu_rate", "temp_num", "temp_list", "hydro_temp", 
                   "hydro_temp_no", "hydro_concent", "hydro_concent_no", "hydor_press", "hydor_press_no", "dcdc_stat")
g_fuel_bat_name = ("燃料电池电压", "燃料电池电流", "燃料消耗率", "燃料电池温度探针总数", "探针温度值列表", "氢气系统中最高温度", 
              "氢气系统中最高温度探针代号", "氢气系统中最高浓度", "氢气系统中最高浓度传感器代号", "氢气最高压力", "氢气最高压力传感器代号", "高压DC/DC状态")

# 定位数据
class GbParse0x05:
    
    def __init__(self, s, len_out):
        self.__gps_data = {}
        self.__gps_desc = dict(zip(g_gps_keys, g_gps_name))

        data = s
        idx = 0
        #print(data[idx:])
        tmp_values = struct.unpack(">BII", data[idx:idx+9])
        self.__gps_data = dict(zip(g_gps_keys, tmp_values))
        idx += 9
        self.__gps_data[g_gps_keys[1]] /= 1e6
        self.__gps_data[g_gps_keys[2]] /= 1e6
        
        len_out[0] = idx

    def GetData(self):
        return self.__gps_data
    def GetDesc(self):
        return self.__gps_desc
    def display(self):
        print("定位数据:")
        for i in g_gps_keys:
            print(self.__gps_desc[i], self.__gps_data[i], sep=':', end = ', ')

# 报警数据
class GbParse0x07:
    
    #定义构造方法
    def __init__(self, s, len_out):
        self.__fault_data = {}
        self.__fault_desc = dict(zip(g_fault_keys, g_fault_name))

        data = s
        idx = 0
        #print(data[idx:])
        # 最高报警等级
        tmp_values = struct.unpack(">BIB", data[idx:idx+6])
        idx += 6
        self.__fault_data = dict(zip(g_fault_keys, tmp_values))

        fault_list = []
        # 可充电蓄能装置故障总数
        bms_fault_num = self.__fault_data['bms_num']
        if bms_fault_num > 0:
            for i in range(bms_fault_num):
                fault_list.append(struct.unpack(">I", data[idx:idx+4])[0])
                idx += 4
        self.__fault_data['bms_list'] = fault_list
        fault_list.clear()

        # 电机故障总数
        monitor_fault_num = struct.unpack(">B", data[idx:idx+1])[0]
        idx += 1
        if monitor_fault_num > 0:
            fault_list = []
            for i in range(monitor_fault_num):
                fault_list.append(struct.unpack(">I", data[idx:idx+4])[0])
                idx += 4
        self.__fault_data['motor_num'] = monitor_fault_num
        self.__fault_data['motor_list'] = fault_list
        fault_list.clear()
        # 发动机故障总数
        engine_fault_num = struct.unpack(">B", data[idx:idx+1])[0]
        idx += 1
        if engine_fault_num > 0:
            fault_list = []
            for i in range(engine_fault_num):
                fault_list.append(struct.unpack(">I", data[idx:idx+4])[0])
                idx += 4
        self.__fault_data['engine_num'] = engine_fault_num
        self.__fault_data['engine_list'] = fault_list
        fault_list.clear()
        # 其他故障总数
        other_fault_num = struct.unpack(">B", data[idx:idx+1])[0]
        idx += 1
        if other_fault_num > 0:
            fault_list = []
            for i in range(other_fault_num):
                fault_list.append(struct.unpack(">I", data[idx:idx+4])[0])
                idx += 4
        self.__fault_data['other_num'] = other_fault_num
        self.__fault_data['other_list'] = fault_list
        fault_list.clear()

        len_out[0] = idx

    def GetData(self):
        return self.__fault_data
    def GetDesc(self):
        return self.__fault_desc
    def display(self):
        print("\n报警数据:")
        for i in g_fault_keys:
            print(self.__fault_desc[i], self.__fault_data[i], sep=':', end = ', ')
# 整车数据
class GbParse0x01:
    
    def __init__(self, s, len_out):
        self.__vehicle_data = {}
        self.__vehicle_desc = dict(zip(g_vehicle_keys, g_vehicle_name))

        data = s
        idx = 0
        #print(data[idx:])
        veh_value = struct.unpack(">BBBHIHHBBBHBB", data[idx:idx+20])
        self.__vehicle_data = dict(zip(g_vehicle_keys, veh_value))

        idx += 20
        len_out[0] = idx

    def GetData(self):
        return self.__vehicle_data
    def GetDesc(self):
        return self.__vehicle_desc
    def display(self):
        print("\n整车数据:")
        for i in g_vehicle_keys:
            print(self.__vehicle_desc[i], self.__vehicle_data[i], sep=':', end = ', ')

# 电机数据
class GbParse0x02:
    
    def __init__(self, s, len_out):
        self.__motor_data = []
        self.__motor_desc = dict(zip(g_motor_keys, g_motor_name))

        data = s
        idx = 0
        #print(data[idx:])
        motor_num = struct.unpack(">B", data[idx:idx+1])[0]
        idx += 1
        motor_value = []
        for i in range(motor_num):
            motor_value = struct.unpack(">BBBHHBHH", data[idx:idx+12])
            self.__motor_data.append(dict(zip(g_motor_keys, motor_value)))
            idx += 12
        len_out[0] = idx

    def GetData(self):
        return self.__motor_data
    def GetDesc(self):
        return self.__motor_desc
    def display(self):
        for motor_idx in range(len(self.__motor_data)):
            print("\n电机%d数据:" % (motor_idx+1))
            for i in g_motor_keys:
                print(self.__motor_desc[i], self.__motor_data[motor_idx][i], sep=':', end = ', ')

# 单体电压
class GbParse0x08:
    
    def __init__(self, s, len_out):
        self.__bms_volt_data = []
        self.__bms_volt_desc = dict(zip(g_bms_volt_keys, g_bms_volt_name))

        data = s
        idx = 0
        #print(data[idx:])
        sys_num = struct.unpack(">B", data[idx:idx+1])[0]
        idx += 1
        for sys_idx in range(sys_num):
            tmp_values = struct.unpack(">BHHHHB", data[idx:idx+10])
            self.__bms_volt_data.append(dict(zip(g_bms_volt_keys, tmp_values)))
            idx += 10
            volt_list = {}
            start = self.__bms_volt_data[sys_idx]["start_idx"]
            for i in range(self.__bms_volt_data[sys_idx]["now_num"]):
                volt_list[ start + i] = struct.unpack(">H", data[idx:idx+2])[0]
                idx += 2
            self.__bms_volt_data[sys_idx]["volt_list"] = volt_list
        len_out[0] = idx
    def GetData(self):
        return self.__bms_volt_data
    def GetDesc(self):
        return self.__bms_volt_desc
    def display(self):
        for no in range(len(self.__bms_volt_data)):
            print("\n子系统单体电压数据(总数%d):" % len(self.__bms_volt_data))
            for i in g_bms_volt_keys:
                print(self.__bms_volt_desc[i], self.__bms_volt_data[no][i], sep=':', end = ', ')

# 温度探针
class GbParse0x09:
    
    def __init__(self, s, len_out):
        self.__bms_temp_data = []
        self.__bms_temp_desc = dict(zip(g_bms_temp_keys, g_bms_temp_name))

        data = s
        idx = 0
        #print(data[idx:])
        sys_num = struct.unpack(">B", data[idx:idx+1])[0]
        idx += 1
        for sys_idx in range(sys_num):
            tmp_values = struct.unpack(">BH", data[idx:idx+3])
            self.__bms_temp_data.append(dict(zip(g_bms_temp_keys, tmp_values)))
            idx += 3
            temp_list = {}
            for i in range(self.__bms_temp_data[sys_idx]["tot_num"]):
                temp_list[i+1] = struct.unpack(">B", data[idx:idx+1])[0]
                idx += 1
            self.__bms_temp_data[sys_idx]["temp_list"] = temp_list

        len_out[0] = idx
    def GetData(self):
        return self.__bms_temp_data
    def GetDesc(self):
        return self.__bms_temp_desc
    def display(self):
        for no in range(len(self.__bms_temp_data)):
            print("\n子系统温度探针数据(总数%d):" % len(self.__bms_temp_data))
            for i in g_bms_temp_keys:
                print(self.__bms_temp_desc[i], self.__bms_temp_data[no][i], sep=':', end = ', ')

# 极值数据
class GbParse0x06:
    
    def __init__(self, s, len_out):
        self.__extreme_data = {}
        self.__extreme_desc = dict(zip(g_extreme_keys, g_extreme_name))

        data = s
        idx = 0
        #print(data[idx:])
        tmp_values = struct.unpack(">BBHBBHBBBBBB", data[idx:idx+14])
        self.__extreme_data = dict(zip(g_extreme_keys, tmp_values))
        idx += 14
        len_out[0] = idx

    def GetData(self):
        return self.__extreme_data
    def GetDesc(self):
        return self.__extreme_desc
    def display(self):
        print("\n极值数据:")
        for i in g_extreme_keys:
            print(self.__extreme_desc[i], self.__extreme_data[i], sep=':', end = ', ')

# 发动机数据
class GbParse0x04:
    
    def __init__(self, s, len_out):
        self.__engine_data = {}
        self.__engine_desc = dict(zip(g_engine_keys, g_engine_name))

        data = s
        idx = 0
        #print(data[idx:])
        tmp_values = struct.unpack(">BHH", data[idx:idx+5])
        self.__engine_data = dict(zip(g_engine_keys, tmp_values))
        idx += 5
        
        len_out[0] = idx

    def GetData(self):
        return self.__engine_data
    def GetDesc(self):
        return self.__engine_desc
    def display(self):
        print("\n发动机数据:")
        for i in g_engine_keys:
            print(self.__engine_desc[i], self.__engine_data[i], sep=':', end = ', ')

# 燃料电池数据
class GbParse0x03:
    
    def __init__(self, s, len_out):
        self.__fuel_bat_data = {}
        self.__fuel_bat_desc = dict(zip(g_fuel_bat_keys, g_fuel_bat_name))

        data = s
        idx = 0
        #print(data[idx:])
        tmp_values = struct.unpack(">HHHH", data[idx:idx+8])
        self.__fuel_bat_data = dict(zip(g_fuel_bat_keys, tmp_values))
        idx += 8

        key_idx = 3
        temp_num = self.__fuel_bat_data[g_fuel_bat_keys[key_idx]] 
        key_idx += 1
        temp_list = []
        if temp_num > 0:
            for i in range(temp_num):
                temp_list.append(struct.unpack(">B", data[idx:idx+1])[0])
                idx += 1
        self.__fuel_bat_data[g_fuel_bat_keys[key_idx]] = temp_list
        key_idx += 1

        tmp_values = struct.unpack(">HBHBHBB", data[idx:idx+10])
        idx += 10
        for i in range(len(tmp_values)):
            self.__fuel_bat_data[g_fuel_bat_keys[key_idx]] = tmp_values[i]
            key_idx += 1

        len_out[0] = idx

    def GetData(self):
        return self.__fuel_bat_data
    def GetDesc(self):
        return self.__fuel_bat_desc
    def display(self):
        print("\n燃料电池数据:")
        for i in g_fuel_bat_keys:
            print(self.__fuel_bat_desc[i], self.__fuel_bat_data[i], sep=':', end = ', ')

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
            
class GbMainParse:
    
    __time_sec = 0
    #定义构造方法
    def __init__(self, s, tot_len, flg):
               
        hex_stream = bytes.fromhex(data[4:tot_len-2]);#跳过2323，去掉校验码
        hex_stream_len=len(hex_stream)
        idx = 0
        # 消息id
        self.__cmd = int(data[idx:idx+2], 16)
        idx += 4
        # vin
        tmp_vin = data[idx:idx+34]
        self.__vin = ''
        for i in range(0, len(tmp_vin), 2):
            self.__vin += chr(int(tmp_vin[i:i+2], 16))
        idx += 34
        # 加密
        self.__encrypt = int(data[idx:idx+2], 16)
        idx += 2
        # 数据长度
        self.__data_len = int(data[idx:idx+4], 16)
        idx += 4
        data_unit_len -= idx
        data_unit_len = data_unit_len//2

        if self.__data_len == data_unit_len:
            # 日期时间
            self.__dt_sec = 0
            y = int(data[idx:idx+2], 16)
            idx += 2
            m = int(data[idx:idx+2], 16)
            idx += 2
            d = int(data[idx:idx+2], 16)
            idx += 2
            hh = int(data[idx:idx+2], 16)
            idx += 2
            mm = int(data[idx:idx+2], 16)
            idx += 2
            ss = int(data[idx:idx+2], 16)
            idx += 2
            self.__dt=datetime.datetime(2000+y, m, d, hh, mm, ss, 0)
            #print(self.__dt.strftime('%Y-%m-%d %H:%M:%S'))
            self.__time_sec = time.mktime(self.__dt.timetuple())
            
            # 解析各个数据块
            idx = 0
            used_len = [0]
            self.one_pack = []
            while hex_stream_len > 0:
                block_id = struct.unpack("<B", hex_stream[idx:idx+1])[0]
                idx += 1
                hex_stream_len -= 1
                #print("\nblock_id=%d, idx=%d" % (block_id, idx))
                if block_id == 0x01:
                    self.one_pack.append(GbParse0x01(hex_stream[idx:], used_len))
                elif block_id == 0x02:
                    self.one_pack.append(GbParse0x02(hex_stream[idx:], used_len))
                elif block_id == 0x03:
                    self.one_pack.append(GbParse0x03(hex_stream[idx:], used_len))
                elif block_id == 0x04:
                    self.one_pack.append(GbParse0x04(hex_stream[idx:], used_len))
                elif block_id == 0x05:
                    self.one_pack.append(GbParse0x05(hex_stream[idx:], used_len))
                elif block_id == 0x06:
                    self.one_pack.append(GbParse0x06(hex_stream[idx:], used_len))
                elif block_id == 0x07:
                    self.one_pack.append(GbParse0x07(hex_stream[idx:], used_len))
                elif block_id == 0x08:
                    self.one_pack.append(GbParse0x08(hex_stream[idx:], used_len))
                elif block_id == 0x09:
                    self.one_pack.append(GbParse0x09(hex_stream[idx:], used_len))
                else:
                    print("Unkonw id, block_id=", block_id)
                    break
                
                idx += used_len[0]
                hex_stream_len -= used_len[0]

    def display(self):
        for i in self.one_pack:
            i.display()
    def GetTimeSec(self):
        return self.__time_sec
    def GetTimeStr(self):
        return self.__dt.strftime('%Y-%m-%d %H:%M:%S')
            
def main():
    last_time = 0
    for root, dirs, files in os.walk(DirName):
        for name in files:
            file_name = os.path.join(root, name)
            print('-------------->open ', file_name)
            with open(file_name) as fd:
                for line in fd:
                    try:
                        data = re.search( r'(23230[23].*)', line).group(1)
                        data = data.strip()
                        obj = GbMainParse(data, len(data))
                        if ParseFlg == '1':
                            obj.display()
                        elif ParseFlg == '2':
                            #### 检测数据 start #####
                            now = obj.GetTimeSec();
                            if last_time == 0:
                                last_time = now
                            elif now - last_time > 1:
                                print("=> time offset more than", now-last_time, ";curr=", now, ",last=", last_time)
                                print("=> fmt time: cur =", obj.GetTimeStr(), "last=", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(last_time)))
                            last_time = now
                            #### 检测数据 end #####
                        else:
                            print("param error, ParseFlg=%s" % ParseFlg)
                    except AttributeError:
                        # 忽略不合法的数据
                        continue
            #break #一个文件
if __name__ == '__main__':
    main()