# -*- coding: utf8 -*-
import codecs
import struct
from ctypes import *


class 整车数据包(BigEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('车辆状态', c_uint8),
        ('充电状态', c_uint8),
        ('运行模式', c_uint8),
        ('车速', c_uint16),
        ('累计里程', c_uint32),
        ('总电压', c_uint16),
        ('总电流', c_uint16),
        ('SOC', c_uint8),
        ('DCDC状态', c_uint8),
        ('档位', c_uint8),
        ('绝缘电阻', c_uint16),
        ('预留', c_uint16),
    ]

    def as_dict(self):
        return {key[0]: getattr(self, key[0]) for key in self._fields_}


class 发动机数据(BigEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('发动机状态', c_uint8),
        ('曲轴转速', c_uint16),
        ('燃料消耗率', c_uint16),
    ]

    def as_dict(self):
        return {key[0]: getattr(self, key[0]) for key in self._fields_}


class 驱动电机详细信息(BigEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('驱动电机序号', c_uint8),
        ('驱动电机状态', c_uint8),
        ('控制器温度', c_uint8),
        ('转速', c_uint16),
        ('转矩', c_uint16),
        ('温度', c_uint8),
        ('输入电压', c_uint16),
        ('母线电流', c_uint16),
    ]

    def as_dict(self):
        return {key[0]: getattr(self, key[0]) for key in self._fields_}


class 驱动电机数据(BigEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('驱动电机个数', c_uint8),
        ('驱动电机信息', 驱动电机详细信息 * 253),
    ]

    def as_dict(self):
        return {'驱动电机个数': self.驱动电机个数, '驱动电机信息': [info.as_dict() for i, info in enumerate(self.驱动电机信息) if i < self.驱动电机个数]}



class 实时数据包头(BigEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('数据采集时间', c_uint8 *6),
        ('信息类型标识', c_uint8),
    ]

    def __str__(self):
        s = f'{self.数据采集时间}, {self.信息类型标识}'


class 定位数据包(BigEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('reserved', c_uint8, 5),
        ('east', c_uint8, 1),
        ('south', c_uint8, 1),
        ('valid', c_uint8, 1),
        ('经度', c_uint32),
        ('纬度', c_uint32),
    ]

    def __str__(self):
        return f'valid: {self.valid}, {self.经度} / {self.维度}'

    def as_dict(self):
        return {key[0]: getattr(self, key[0]) for key in self._fields_}


class 极值数据(BigEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('最高电压电池子系统号', c_uint8),
        ('最高电压电池单体代号', c_uint8),
        ('电池单体电压最高值', c_uint16),

        ('最低电压电池子系统号', c_uint8),
        ('最低电压电池单体代号', c_uint8),
        ('电池单体电压最低值', c_uint16),

        ('最高温度子系统号', c_uint8),
        ('最高温度探针序号', c_uint8),
        ('最高温度值', c_uint8),

        ('最低温度子系统号', c_uint8),
        ('最低温度探针序号', c_uint8),
        ('最低温度值', c_uint8),
    ]

    def as_dict(self):
        return {key[0]: getattr(self, key[0]) for key in self._fields_}


def parser_line_to_json():
    txt = origin_txt[::]
    package = dict()

    xtxt = txt.split(' ')
    lineno, filename = xtxt[0].split('@')
    stream = codecs.decode(xtxt[-1].rstrip(), 'hex')

    package['origin_lineno'] = int(lineno)
    package['origin_filename'] = filename
    package['log_tsp'] = xtxt[1]
    package['cmd'] = stream[2]
    try:
        name_map = {
            1: "车辆登入",
            2: "实时信息上报",
            3: "补发信息上报",
            4: "车辆登出",
            5: "平台登入",
            6: "平台登出",
        }
        package['cmd_name'] = name_map[stream[2]]
    except KeyError:
        if 7 <= stream[2] <= 8:
            package['cmd_name'] = '终端数据预留'
        elif 9 <= stream[2] <= 0x7f:
            package['cmd_name'] = '上行数据系统预留'
        elif 0x80 <= stream[2] <= 0x82:
            package['cmd_name'] = '终端数据预留'
        elif 0x83 <= stream[2] <= 0xBF:
            package['cmd_name'] = '下行数据系统预留'
        elif 0xC0 <= stream[2] <= 0xFE:
            package['cmd_name'] = '平台交换自定义数据'
        else:
            package['cmd_name'] = '未定义'

    package['replay'] = stream[3]
    package['vin'] = stream[4:21].decode()
    package['tsp'] = list(stream[24:30])
    package['tsp'].append(0) # 附加一个毫秒值，便于后面的时间差计算
    package['tsp'][0] += 2000
    package['stream'] = codecs.encode(stream, 'hex').decode()

    if stream[2:4] == b'\x02\xfe':
        # 实时数据
        p = self._p32960.on_real(stream[30:-1])
    elif stream[2:4] == b'\x03\xfe':
        # 历史数据
        p = self._p32960.on_real(stream[30:-1])
    else:
        p = None

    package['payload'] = p

    if stream[3] == 0xfe:
        if self.log_date is None:
            self.log_date = list(stream[24:27])
        package['package_type'] = "请求"
    else:
        package['package_type'] = "应答"

    self.packages_list.append(package)


class P32960Parser:
    def __init__(self):
        pass

    def on_pack(self, pack):
        if pack.find(b'\xc8\xff\x20') == 0:
            # 登录数据
            #print('登录数据')
            pass
        elif pack.find(b'\xc8\xff\x21') == 0:
            # 实时数据
            package_32960 = {
                'tsp': list(struct.unpack("6B", pack[3: 9])),
                'payload': self.on_real(pack[9:])
            }
            return package_32960
        elif pack.find(b'\xc8\xff\x22') == 0:
            # 历史数据
            #print('历史数据')
            pass
        elif pack.find(b'\xc8\xff\x23') == 0:
            # 登出数据
            #print('登出数据')
            pass

    def on_real(self, pack):
        used = -1
        package = dict()
        if pack[0] == 0x01:
            #print('整车数据\n', codecs.encode(pack, 'hex').decode())
            header = 整车数据包()
            memmove(addressof(header), pack[1:], sizeof(整车数据包))
            package.update({"整车数据包": header.as_dict()})
            used = sizeof(整车数据包) + 1
        elif pack[0] == 0x02:
            #print('驱动电机数据\n', codecs.encode(pack, 'hex').decode())
            header = 驱动电机数据()
            count = pack[1]
            if count <= 253:
                memmove(addressof(header), pack[1:], 1 + count * sizeof(驱动电机详细信息))
                package.update({"驱动电机数据": header.as_dict()})
                used = 1 + 1 + count * sizeof(驱动电机详细信息)
            else:
                used = 1 + 1
        elif pack[0] == 0x03:
            #print('燃料电池数据\n', codecs.encode(pack, 'hex').decode())
            child = dict()
            child['燃料电池电压'] = struct.unpack(">H", pack[1:3])[0]
            child['燃料电池电流'] = struct.unpack(">H", pack[3:5])[0]
            child['燃料消耗率'] = struct.unpack(">H", pack[5:7])[0]
            child['温度探针数量'] = struct.unpack(">H", pack[7:9])[0]
            prob_count = 0 if child['温度探针数量'] > 0xfffe else child['温度探针数量']
            if prob_count == 0:
                child['探针温度值'] = list()
            else:
                child['探针温度值'] = list(pack[9: prob_count + 9])

            package.update({'燃料电池数据': child})
            used = 1 + 18 + prob_count
        elif pack[0] == 0x04:
            #print('发动机数据\n', codecs.encode(pack, 'hex').decode())
            header = 发动机数据()
            memmove(addressof(header), pack[1:], sizeof(发动机数据))
            package.update({"发动机数据": header.as_dict()})
            used = 1 + sizeof(发动机数据)
        elif pack[0] == 0x05:
            #print('车辆位置数据\n', codecs.encode(pack, 'hex').decode())
            header = 定位数据包()
            memmove(addressof(header), pack[1:], sizeof(定位数据包))
            package.update({"定位数据包": header.as_dict()})
            used = sizeof(定位数据包) + 1
        elif pack[0] == 0x06:
            #print('极值数据\n', codecs.encode(pack, 'hex').decode())
            header = 极值数据()
            memmove(addressof(header), pack[1:], sizeof(极值数据))
            package.update({"极值数据": header.as_dict()})
            used = sizeof(极值数据) + 1
        elif pack[0] == 0x07:
            #print('报警数据\n', codecs.encode(pack, 'hex').decode())
            child = dict()
            try:
                #if pack[2] != 0:
                #    print(pack)
                child['最高报警等级'] = pack[1]
                child['通用报警标志'] = struct.unpack(">I", pack[2:6])[0]
                used = 6

                count = pack[used]
                child['可充电储能装置故障总数'] = count
                if count == 0:
                    code_list = list()
                elif count <= 252:
                    bytes_count = count * 4
                    code_list = struct.unpack(f">{count}I", pack[used + 1: used + 1 + bytes_count])
                else:
                    code_list = list()
                    count = 0
                child['可充电储能装置故障代码列表'] = code_list
                used += count * 4 + 1

                count = pack[used]
                child['驱动电机故障总数'] = count
                if count == 0:
                    code_list = list()
                elif count <= 252:
                    bytes_count = count * 4
                    code_list = struct.unpack(f">{count}I", pack[used + 1: used + 1 + bytes_count])
                else:
                    code_list = list()
                    count = 0
                child['驱动电机故障代码列表'] = code_list
                used += count * 4 + 1

                count = pack[used]
                child['发电机故障总数'] = count
                if count == 0:
                    code_list = list()
                elif count <= 252:
                    bytes_count = count * 4
                    code_list = struct.unpack(f">{count}I", pack[used + 1: used + 1 + bytes_count])
                else:
                    code_list = list()
                    count = 0
                child['发机故障代码列表'] = code_list
                used += count * 4 + 1

                count = pack[used]
                child['其他故障总数'] = count
                if count == 0:
                    code_list = list()
                elif count <= 252:
                    bytes_count = count * 4
                    code_list = struct.unpack(f">{count}I", pack[used + 1: used + 1 + bytes_count])
                else:
                    code_list = list()
                    count = 0
                child['其他故障代码列表'] = code_list
                used += count * 4 + 1
            except:
                child['解析出错'] = True
            package.update({"报警数据": child})
        elif pack[0] == 0x08:
            #print('可充电储能装置电压数据\n', codecs.encode(pack, 'hex').decode())
            info = dict()
            sys_cnt = pack[1]
            if sys_cnt <= 250:
                info['子系统个数'] = sys_cnt
                idx = 2
                used = 2
                info['子系统'] = sub_sys_list = list()
                for i in range(sys_cnt):
                    child = dict()
                    try:
                        child['解析成功'] = True
                        child['储能子系统号'] = pack[i * idx + 2]
                        child['储能子系统电压'] = struct.unpack(">H", pack[i * idx + 3: i * idx + 5])[0]
                        child['储能子系统电流'] = struct.unpack(">H", pack[i * idx + 5: i * idx + 7])[0]
                        child['单体总数'] = struct.unpack(">H", pack[i * idx + 7: i * idx + 9])[0]
                        child['本帧起始电池序号'] = struct.unpack(">H", pack[i * idx + 9: i * idx + 11])[0]
                        child['本帧电池总数'] = sub_sys_bat_count = pack[i * idx + 11]
                        child['单体电压'] = list(struct.unpack(f">{sub_sys_bat_count}H", pack[i * idx + 12: i * idx + 12 + sub_sys_bat_count * 2]))
                        used += 10 + sub_sys_bat_count * 2
                    except (struct.error, IndexError):
                        used = -1
                        child['解析成功'] = False
                    finally:
                        sub_sys_list.append(child)
                        if used != -1:
                            break
                package.update({"可充电储能装置电压数据": info})
            else:
                used = 2
        elif pack[0] == 0x09:
            #print('可充电储能装置温度数据\n', codecs.encode(pack, 'hex').decode())
            info = dict()
            sys_cnt = pack[1]
            if sys_cnt <= 250:
                info['子系统个数'] = sys_cnt
                idx = 2
                used = 2
                info['子系统'] = sub_sys_list = list()
                for i in range(sys_cnt):
                    child = dict()
                    try:
                        child['储能子系统号'] = sub_sys_no = pack[i * idx + 2]
                        child['探针数量'] = sub_sys_probe_count = struct.unpack(">H", pack[i * idx + 3: i * idx + 5])[0]
                        used += 3 + sub_sys_probe_count
                        child['单体温度'] = sub_temp = list(map(lambda x: x - 40, list(pack[i * idx + 5: i * idx + 5 + sub_sys_probe_count])))
                    except (struct.error, IndexError):
                        used = -1
                        child['解析成功'] = False
                    finally:
                        sub_sys_list.append(child)
                        if used == -1:
                            break
                package.update({"可充电储能装置温度数据": info})
            else:
                used = 2
        if used < 0:
            return package

        if len(pack) > used and len(pack) - used > 10:
            p = self.on_real(pack[used:])
            package.update(**p)

        return package
