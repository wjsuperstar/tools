import os
import re
import sys, getopt
import struct
import parse_gb32960
import json
from parse_sq_zc45t import *

def load_json(file_name):
    try:
        with open(file_name, encoding='utf-8') as fw:
            return json.load(fw)
    except FileNotFoundError:
        return None

class SqParse0x80:
    def __init__(self, s, len_out, factor_offset):
        data = s
        idx = 1
        total = len(data)

        self.__data = dict()
        self.__data.update({'总数': data[0]})
        for i in range(data[0]):
            if idx < total:
                data_id, time_offset, val = struct.unpack(">H2B", data[idx:idx + 4])
                idx += 4
                data_id = str(data_id)
                if factor_offset:
                    self.__data.update({data_id: '%d, %d' % (
                    time_offset, val * factor_offset[data_id][0] + factor_offset[data_id][1])})
                else:
                    self.__data.update({data_id: '%d, %d' % (time_offset, val)})
        len_out[0] = idx

    def as_dict(self):
        return self.__data

class SqParse0x81(SqParse0x80):
    def __init__(self, s, len_out, factor_offset):
        super().__init__(s, len_out, factor_offset)
class SqParse0x82(SqParse0x80):
    def __init__(self, s, len_out, factor_offset):
        super().__init__(s, len_out, factor_offset)
class SqParse0x83(SqParse0x80):
    def __init__(self, s, len_out, factor_offset):
        super().__init__(s, len_out, factor_offset)
class SqParse0x85(SqParse0x80):
    def __init__(self, s, len_out, factor_offset):
        super().__init__(s, len_out, factor_offset)

class SqParse0x84:
    def __init__(self, s, len_out, factor_offset):
        data = s
        idx = 1
        total = len(data)

        self.__data = dict()
        self.__data.update({'总数': data[0]})
        for i in range(data[0]):
            if idx < total:
                data_id, time_offset, val = struct.unpack(">HBH", data[idx:idx + 5])
                idx += 5
                data_id = str(data_id)
                if factor_offset:
                    self.__data.update({data_id: '%d, %d' % (
                    time_offset, val * factor_offset[data_id][0] + factor_offset[data_id][1])})
                else:
                    self.__data.update({data_id: '%d, %d' % (time_offset, val)})
        len_out[0] = idx

    def as_dict(self):
        return self.__data

class SqParse0x86:
    def __init__(self, s, len_out, factor_offset):
        data = s
        idx = 1
        total = len(data)

        self.__data = dict()
        self.__data.update({'总数': data[0]})
        for i in range(data[0]):
            if idx < total:
                data_id, time_offset, val = struct.unpack(">HB5s", data[idx:idx + 8])
                idx += 8
                data_id = str(data_id)
                self.__data.update({data_id: '%d, %s' % (time_offset, val.hex())})
        len_out[0] = idx

    def as_dict(self):
        return self.__data

class SqParse0x87:
    def __init__(self, s, len_out, factor_offset):
        data = s
        idx = 1
        total = len(data)

        self.__data = dict()
        self.__data.update({'总数': data[0]})
        for i in range(data[0]):
            if idx < total:
                data_id, time_offset, val = struct.unpack(">HBI", data[idx:idx + 7])
                idx += 7
                data_id = str(data_id)
                if factor_offset:
                    self.__data.update({data_id: '%d, %d' % (time_offset, val * factor_offset[data_id][0] + factor_offset[data_id][1])})
                else:
                    self.__data.update({data_id: '%d, %d' % (time_offset, val)})
        len_out[0] = idx

    def as_dict(self):
        return self.__data

class SqParse0x88:
    def __init__(self, s, len_out, factor_offset):
        data = s
        idx = 1
        total = len(data)

        self.__data = dict()
        self.__data.update({'总数': data[0]})
        for i in range(data[0]):
            if idx < total:
                data_len = data[idx+1]
                data_id, tmp, time_offset, val = struct.unpack(">BBB%ds" % data_len, data[idx:idx+data_len+3])
                idx += (data_len+3)
                data_id = str(data_id)
                self.__data.update({data_id: '%d, %s' % (time_offset, val.hex())})
        len_out[0] = idx

    def as_dict(self):
        return self.__data

class SqParseMsg(parse_gb32960.MainParseMsg):
    def __init__(self):
        super().__init__()
        self._cfg = load_json('parse_cfg.json')

    def parse_custom_msg(self, cmd, data):
        package = dict()
        if cmd == 0xEF or cmd == 0xF0:
            idx = 0
            tot_len = len(data)
            used_len = [0]
            package.update(parse_gb32960.GbParseTime(data, used_len).as_dict())
            idx += used_len[0]
            while idx < tot_len:
                # print(data[idx:])
                block_id = struct.unpack(">B", data[idx:idx + 1])[0]
                idx += 1
                try:
                    factor_offset = self._cfg[hex(block_id)]
                except KeyError:
                    factor_offset = None
                #factor_offset = None
                #print(block_id, data[idx:].hex())
                if block_id == 0x80:
                    package.update({'四状态枚举量': SqParse0x80(data[idx:], used_len, None).as_dict()})
                elif block_id == 0x81:
                    package.update({'八状态枚举量': SqParse0x81(data[idx:], used_len, None).as_dict()})
                elif block_id == 0x82:
                    package.update({'十六状态枚举量': SqParse0x82(data[idx:], used_len, None).as_dict()})
                elif block_id == 0x83:
                    package.update({'八位模拟数据': SqParse0x83(data[idx:], used_len, factor_offset).as_dict()})
                elif block_id == 0x84:
                    package.update({'十六位模拟数据': SqParse0x84(data[idx:], used_len, factor_offset).as_dict()})
                elif block_id == 0x85:
                    package.update({'一位开关量': SqParse0x85(data[idx:], used_len, None).as_dict()})
                elif block_id == 0x86:
                    package.update({'诊断类信号': SqParse0x86(data[idx:], used_len, None).as_dict()})
                elif block_id == 0x87:
                    package.update({'其他信号': SqParse0x87(data[idx:], used_len, None).as_dict()})
                elif block_id == 0x88:
                    package.update({'字符型信号': SqParse0x88(data[idx:], used_len, None).as_dict()})
                else:
                    print('Unkonw id, block_id=', hex(block_id))
                    break

                idx += used_len[0]
        elif cmd == 0xFB:
                obj = Parse45tCustomMsg()
                package = obj.parse(data)
        return package

def analyse_data(package):
    result = True
    cnt = 0
    if package['消息头']['命令标识'] == 0xef:
        send_data = load_json('can_data.json')
        data_cfg  = load_json('sig_id_map.json')
        data = package['自定义数据']
        print('自定义数据0xEF', data['时间'], '检测结果:')
        for k, v in data.items():
            if type(v) is dict:
                for i, j in v.items():
                    try:
                        result      = False
                        send_val    = send_data[data_cfg[k][i]]  # can报文发送值
                        upload_val  = int(j.split(',')[1].strip())
                        cnt += 1
                        if send_val != upload_val:
                            #cnt += 1
                            print('Test Fail %d:' % cnt, k, '类型编号:', i, 'CAN报文模拟值:%d, 网络上报值:%d' % (send_val, upload_val))
                        else:
                            print('Test success %d:' % cnt, k, data_cfg[k][i], '类型编号:', i, 'CAN报文模拟值:%d, 网络上报值:%d' % (send_val, upload_val))
                    except KeyError:
                        continue
    return result

def display_help():
    print('xx.py -d 目录名 -a 动作')
    print('目录里放入待解析文件(.txt或.log)，文件编码确保是UTF8格式, 程序会逐个文件解析')
    print('动作：0表示打印；1表示分析0xEF自定义数据跟实际值是否一致，依赖两个配置文件：can_data.json dbc信号实际值，sig_id_map.json dbc信号与网络协议里类型编号映射表')
def parse_cmd_param():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hd:a:", ["dir=", "action="])
    except getopt.GetoptError:
        display_help()
        sys.exit(-1)

    a = None
    b = 0
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            display_help()
            sys.exit(0)
        elif opt in ("-d", "--dir"):
            a = arg
        elif opt in ("-a", "--action"):
            b = int(arg)
    if a is None:
        display_help()
        sys.exit(-1)

    return a, b

def main():
    DirName, analyse = parse_cmd_param()
    for root, dirs, files in os.walk(DirName):
        for name in files:
            file_name = os.path.join(root, name)
            if file_name.endswith('.txt') or file_name.endswith('.log'):
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
                                if analyse == 0:
                                    print(package)
                                else:
                                    analyse_data(package)
                                #break
                        except UnicodeDecodeError:
                            print("UnicodeDecodeError")
                            pass
            else:
                print('跳过非法后缀文件: ', file_name)
            #break #一个文件

if __name__ == '__main__':
    main()