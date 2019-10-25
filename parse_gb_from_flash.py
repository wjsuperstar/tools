#!/usr/bin/python
# -*- coding: UTF-8 -*-
# auth: WuJian  20191024
# desc: 解析车讯二代flash保存的国标数据文件

import struct

FileName=r'D:\test\test_py\tbox_data.bin'


# 以下元组是根据GB32960协议定义，不可更改。
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

# 定位数据
class GbParse0x05:
    __gps_data = {}
    __gps_desc = {}
    def __init__(self, s, len_out):
        self.__gps_desc = dict(zip(g_gps_keys, g_gps_name))

        data = s
        idx = 0
        #print(data[idx:])
        tmp_values = struct.unpack(">BII", data[idx:idx+9])
        self.__gps_data = dict(zip(g_gps_keys, tmp_values))
        idx += 9

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
    __fault_data = {}
    __fault_desc = {}
    #定义构造方法
    def __init__(self, s, len_out):
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
    __vehicle_data = {}
    __vehicle_desc = {}
    def __init__(self, s, len_out):
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
    __motor_data = []
    __motor_desc = {}
    def __init__(self, s, len_out):
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
    __bms_volt_data = []
    __bms_volt_desc = {}

    def __init__(self, s, len_out):
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
            print("\n子系统%d单体电压数据:" % (no+1))
            for i in g_bms_volt_keys:
                print(self.__bms_volt_desc[i], self.__bms_volt_data[no][i], sep=':', end = ', ')

# 温度探针
class GbParse0x09:
    __bms_temp_data = []
    __bms_temp_desc = {}

    def __init__(self, s, len_out):
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
            print("\n子系统%d温度探针数据:" % (no+1))
            for i in g_bms_temp_keys:
                print(self.__bms_temp_desc[i], self.__bms_temp_data[no][i], sep=':', end = ', ')

# 极值数据
class GbParse0x06:
    __extreme_data = {}
    __extreme_desc = {}
    def __init__(self, s, len_out):
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
        print("极值数据:")
        for i in g_extreme_keys:
            print(self.__extreme_desc[i], self.__extreme_data[i], sep=':', end = ', ')

class GbMainParse:
    # 数据采集时间
    __time = ''
    # 数据块id
    __block_id = 0
    
    #定义构造方法
    def __init__(self, s, tot_len):
        data = s
        idx  = 0
        y,m,d,h,min,s = struct.unpack("<BBBBBB", data[idx:idx+6])
        idx += 6
        tot_len -= 6
        self.__time = str(2000+y)+'-'+str(m)+'-'+str(d)+' '+str(h)+':'+str(min)+':'+str(s)
        print("\n\n\n数据采集时间:", self.__time)
        
        # 解析各个数据块
        used_len = [0]
        while tot_len > 0:
            #print(data[idx:])
            self.__block_id = struct.unpack("<B", data[idx:idx+1])[0]
            idx += 1
            tot_len -= 1
            #print("\n__block_id=%d, idx=%d" % (self.__block_id, idx))
            if self.__block_id == 0x05:
                self.__block = GbParse0x05(data[idx:], used_len)
            elif self.__block_id == 0x07:
                self.__block = GbParse0x07(data[idx:], used_len)
            elif self.__block_id == 0x01:
                self.__block = GbParse0x01(data[idx:], used_len)
            elif self.__block_id == 0x02:
                self.__block = GbParse0x02(data[idx:], used_len)
            elif self.__block_id == 0x08:
                self.__block = GbParse0x08(data[idx:], used_len)    
            elif self.__block_id == 0x09:
                self.__block = GbParse0x09(data[idx:], used_len)
            elif self.__block_id == 0x06:
                self.__block = GbParse0x06(data[idx:], used_len)
            elif self.__block_id == 0x03:
                pass
            elif self.__block_id == 0x04:
                pass
            
            idx += used_len[0]
            tot_len -= used_len[0]
            self.__block.display()
            #print("\nused_len=", used_len[0], "idx=", idx, "tot_len=", tot_len)
    
        
def main():
    count = 0
    with open(FileName, mode='rb') as fd:
        packet = fd.read(1024)
        while packet != '':
            count += 1
            data_len = struct.unpack("<H", packet[10:12])[0] - 28
            print("\ndata_len=%d, count=%d" % (data_len, count))
            GbMainParse(packet[28:], data_len)
            packet = fd.read(1024)
            #break
            

if __name__ == '__main__':
    main()