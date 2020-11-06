import os
import re
import sys
import struct
import parse_gb32960


class SqParse0x80:
    def key_desc(self):
        return  {1: '动力电池高压使能', 2: '24VDCDC使能', 3: '电动助力转向系统使能', 4: '电动助力制动系统使能',
                 5: 'PTC接触器使能', 6: '动力电池禁止充电使能', 7 :'空调压缩机使能', 8: '集成控制器高压接触器使能',
                 9: '电机使能', 10: '锁车功能激活状态', 11: '车速限制状态', 12: '电机工作模式',
                 13: 'PTC接触器状态', 14: '主正接触器状态', 15: '辅机高压接触器状态', 16: '空调压缩机高压接触器状态',
                 17: '动力电池负极放电接触器状态', 18: '动力电池绝缘故障状态', 19: '动力电池充电模式', 20: '动力电池充电正1接触器状态',
                 21: '动力电池充电负1接触器状态', 22: '电池冷却系统模式设定', 23: 'BTMS工作模式', 24: '主继电器状态'}

    def __init__(self, s, len_out):
        data = s
        idx = 1
        total = len(data)

        self.__data = dict()
        self.__data.update({'总数': data[0]})
        for i in range(data[0]):
            if idx < total:
                data_id, time_offset, val = struct.unpack(">H2B", data[idx:idx + 4])
                idx += 4
                self.__data.update({self.key_desc()[data_id] : 'offset100ms:%d, val:%d' % (time_offset, val)})
        len_out[0] = idx

    def as_dict(self):
        return self.__data

class SqParse0x81:
    def __init__(self, s, len_out):
        data = s
        idx = 1
        total = len(data)

        self.__data = dict()
        self.__data.update({'总数': data[0]})
        for i in range(data[0]):
            if idx < total:
                data_id, time_offset, val = struct.unpack(">H2B", data[idx:idx + 4])
                idx += 4
                self.__data.update({'数据类型%d' % data_id : 'offset100ms:%d, val:%d' % (time_offset, val)})
        len_out[0] = idx

    def as_dict(self):
        return self.__data

class SqParse0x82(SqParse0x80):
    def key_desc(self):
        return {1: '整车运行状态', 2: '整车故障状态', 3: '整车挡位', 4: '电机控制系统运行状态',
                5: '电机控制系统故障状态', 6: '电池管理系统工作状态', 7: '电池管理系统故障状态', 8: 'BMS充电状态',
                9: 'BTMS系统工作状态', 10: 'BTMS故障状态', 11: 'DCAC_S工作状态', 12: 'DCAC_S故障状态',
                13: 'DCAC_B工作状态', 14: 'DCAC_B故障状态', 15: 'ACCM工作状态', 16: 'ACCM故障状态',
                17: 'DCDC工作状态', 18: 'DCDC故障状态'}


class SqParse0x83(SqParse0x80):
    def key_desc(self):
        return {1: '加速踏板开度', 2: '制动踏板开度', 3: '车辆启动状态', 4: '运行模式',
                5: '充电状态', 6: 'DC-DC状态', 7: '整车最高故障等级', 8: '请求档位',
                9: '电机运行状态', 10: '驱动电机总个数', 11: '驱动电机序列号', 12: '电机温度',
                13: '电机控制器温度', 14: '动力电池SOC', 15: '动力电池最高电压单体模块号', 16: '动力电池最低电压单体模块号',
                17: '动力电池模块最高温度', 18: '动力电池最高温度模块号', 19: '动力电池模块最高温度探针序号', 20: '动力电池模块最低温度',
                21: '动力电池最低温度模块号', 22: '动力电池模块最低温度探针序号', 23: '可充电储能子系统个数', 24: '可充电储能子系统号',
                25: '电压帧序号', 26: '电压帧包编号', 27: '温度帧序号', 28: '温度帧包编号',
                29: '第X个探针的温度', 30: '第Y个探针的温度', 31: '第Z个探针的温度', 32: '第U个探针的温度',
                33: '第V个探针的温度', 34: '第W个探针的温度'}

class SqParse0x84:
    def key_desc(self):
        return {1: '整车车速', 2: '电机控制器直流侧电流', 3: '电机控制器直流侧电压', 4: '电机转速',
                5: '电机扭矩', 6: '动力电池电压', 7: '动力电池电流', 8: '动力电池单体最高电压',
                9: '动力电池最高电压单体号', 10: '动力电池单体最低电压', 11: '动力电池最低电压单体号', 12: '池总能量能耗',
                13: '动力电池正端对地电阻', 14: '动力电池负端对地电阻', 15: '子系统电池单体总数', 16: '子系统温度探针总数',
                17: '第X个单体的电压', 18: '第Y个单体的电压', 19: '第Z个单体的电压'}

    def __init__(self, s, len_out):
        data = s
        idx = 1
        total = len(data)

        self.__data = dict()
        self.__data.update({'总数': data[0]})
        for i in range(data[0]):
            if idx < total:
                data_id, time_offset, val = struct.unpack(">HBH", data[idx:idx + 5])
                idx += 5
                self.__data.update({self.key_desc()[data_id]  : 'offset100ms:%d, val:%d' % (time_offset, val)})
        len_out[0] = idx

    def as_dict(self):
        return self.__data

class SqParse0x85(SqParse0x80):
    def key_desc(self):
        return {1: '制动力状态', 2: '驱动力状态', 3: '温度差异报警', 4: 'B电池高温报警',
                5: '总电压过压报警', 6: '总电压欠压报警', 7: 'SOC低报警', 8: '单体电池过压报警',
                9: '单体电池欠压报警', 10: 'SOC过高报警', 11: 'SOC跳变报警', 12: '电池系统不匹配报警',
                13: '电池单体一致性差报警', 14: '绝缘报警', 15: 'DC-DC温度报警', 16: '制动系统报警',
                17: 'DC-DC状态报警', 18: '驱动电机控制器温度报警', 19: '高压互锁状态报警', 20: '驱动电机温度报警',
                21: '电池过充报警', 22: 'BMS温度差异报警', 23: 'BMS电池高温报警', 24: 'BMS制动系统报警',
                25: 'BMS总电压欠压报警', 26: 'BMSSOC低报警', 27: 'BMS单体电池过压报警', 28: 'BMS单体电池欠压报警',
                29: 'BMSSOC过高报警', 30: 'BMSSOC跳变报警', 31: 'BMS可充电储能系统不匹配报警', 32: 'BMS电池单体一致性差报警',
                33: 'BMS绝缘报警', 34: 'BMS高压互锁状态报警', 35: 'BMS电池过充报警', 36: '电芯过放故障',
                37: '电芯低温报警', 38: '电池包火灾报警', 39: '脉冲放电电流超限报警', 40: '脉冲回充电流超限报警',
                41: '电流传感器故障', 42: '低压供电电压异常报警', 43: 'SOC差异过大报警', 44: '加热膜加热回路故障',
                45: '电池包自保护故障', 46: 'ACAN通讯故障', 47: 'BMS内部通信故障', 48: '加热膜或TMS接触器故障无法闭合报警',
                49: '加热膜或TMS接触器故障无法断开报警', 50: '主负接触器无法闭合故障报警', 51: '主负接触器无法断开故障报警', 52: '直流充电A正接触器无法闭合故障报警',
                53: '直流充电A正接触器无法断开故障报警', 54: '直流充电A负接触器无法闭合故障报警', 55: '直流充电A负接触器无法断开故障报警', 56: '插枪连接信号异常',
                57: '充电时放电电流过大', 58: '充电电流超限报警', 59: '充电插座NTC故障', 60: '充电插座过温报警'}

class SqParse0x87:
    def key_desc(self):
        return {1: '累计运行里程'}

    def __init__(self, s, len_out):
        data = s
        idx = 1
        total = len(data)

        self.__data = dict()
        self.__data.update({'总数': data[0]})
        for i in range(data[0]):
            if idx < total:
                data_id, time_offset, val = struct.unpack(">HBI", data[idx:idx + 7])
                idx += 7
                self.__data.update({self.key_desc()[data_id] : 'offset100ms:%d, val:%d' % (time_offset, val)})
        len_out[0] = idx

    def as_dict(self):
        return self.__data


class SqParseMsg(parse_gb32960.MainParseMsg):
    def __init__(self):
        super().__init__()
        #self.__data = data
    def parse_custom_msg(self, cmd, data):
        package = dict()
        if cmd == 0xEF:
            idx = 0
            tot_len = len(data)
            used_len = [0]
            package.update(parse_gb32960.GbParseTime(data, used_len).as_dict())
            idx += used_len[0]
            while idx < tot_len:
                # print(data[idx:])
                block_id = struct.unpack(">B", data[idx:idx + 1])[0]
                idx += 1
                # print("\nblock_id=%d, idx=%d" % (block_id, idx))
                if block_id == 0x80:
                    package.update({'四状态枚举量': SqParse0x80(data[idx:], used_len).as_dict()})
                elif block_id == 0x81:
                    package.update({'八状态枚举量': SqParse0x81(data[idx:], used_len).as_dict()})
                elif block_id == 0x82:
                    package.update({'十六状态枚举量': SqParse0x82(data[idx:], used_len).as_dict()})
                elif block_id == 0x83:
                    package.update({'八位模拟数据': SqParse0x83(data[idx:], used_len).as_dict()})
                elif block_id == 0x84:
                    package.update({'十六位模拟数据': SqParse0x84(data[idx:], used_len).as_dict()})
                elif block_id == 0x85:
                    package.update({'一位开关量': SqParse0x85(data[idx:], used_len).as_dict()})
                elif block_id == 0x86:
                    package.update({'诊断类信号': SqParse0x81(data[idx:], used_len).as_dict()})
                elif block_id == 0x87:
                    package.update({'其他信号': SqParse0x87(data[idx:], used_len).as_dict()})
                else:
                    print('Unkonw id, block_id=', block_id)
                    break

                idx += used_len[0]

            return package


def main():
    print("使用格式： python xx.py 目录名(待解析文件放入该目录即可，文件编码确保是UTF8格式)")
    if len(sys.argv)-1 == 0:
        print('命令执行需要参数，见使用格式说明')
        return
    DirName = sys.argv[1]
    print("解析目录:", DirName)
    for root, dirs, files in os.walk(DirName):
        for name in files:
            file_name = os.path.join(root, name)
            print('-------------->Parse file:', file_name)
            with open(file_name, encoding='UTF-8') as fd:
                for line in fd:
                    try:
                        result = re.search(r'\D(2323.*)\D', line)
                        if result:
                            data = result.group(1).strip()
                            print(data)
                            obj = SqParseMsg()
                            package = obj.parse_main_msg(bytes.fromhex(data))
                            print(package)
                            #break
                    except UnicodeDecodeError:
                        print("UnicodeDecodeError")
                        pass
            #break #一个文件

if __name__ == '__main__':
    main()