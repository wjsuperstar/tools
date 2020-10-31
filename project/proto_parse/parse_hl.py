# -*- coding: UTF-8 -*-
# auth: WuJian  20201029
# desc: 解析以字符串形式存储的华菱英泰斯特协议数据文件
import sys
import os
import re
import time
import datetime
import codecs
import struct
from ctypes import *

class MsgHead(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('消息ID', c_uint8),
        ('消息体属性', c_uint8),
        ('消息体长度', c_uint16),
        ('流水号', c_uint16),
        ('识别码', c_char*17),
    ]

    def as_dict(self):
        return {key[0]: getattr(self, key[0]) for key in self._fields_}

class Msg0x83Head(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('数据采集时间', c_uint8*6),
        ('数据项个数', c_uint8),
       # ('数据项ID', c_uint8),
       # ('数据项长度', c_uint16),
    ]

    def as_dict(self):
        return {key[0]: getattr(self, key[0]) for key in self._fields_}

# 定位数据
class Msg0x83Body0x01(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('定位状态', c_uint8),
        ('经度', c_uint32),
        ('纬度', c_uint32),
        ('速度', c_uint16),
        ('方向', c_uint16),
        ('里程', c_uint32),
    ]

    def as_dict(self):
        return {key[0]: getattr(self, key[0]) for key in self._fields_}
# 车辆数据
class Msg0x83Body0x40(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('摩擦扭矩', c_uint8),
        ('机油温度', c_uint16),
        ('水温', c_uint16),
        ('机油压力', c_uint16),
        ('相对进气压力', c_uint16),
        ('绝对增压压力', c_uint16),
        ('进气温度', c_uint16),
        ('电瓶电压', c_uint16),
        ('大气压力', c_uint16),
        ('ECU里程', c_uint32),
        ('油门', c_uint8),
        ('负载百分比', c_uint8),
        ('单程油耗', c_uint16),
        ('总油耗', c_uint32),
        ('瞬时油耗', c_uint16),
        ('车速', c_uint16),
        ('发动机扭矩状态', c_uint16),
        ('扭矩百分比', c_uint8),
        ('发动机转速', c_uint16),
        ('当前档位', c_uint16),
        ('氮氧值', c_uint16),
        ('尿素液位', c_uint8),
        ('发动机运行总时间', c_uint32),
    ]

    def as_dict(self):
        return {key[0]: getattr(self, key[0]) for key in self._fields_}
# 锁车状态
class Msg0x83Body0x41(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('协议类型', c_uint8),
        ('ECU通信状态', c_uint8),
        ('ECU故障状态', c_uint8),
        ('ECU锁车状态', c_uint16),
        ('ECU限制模式', c_uint8),
    ]

    def as_dict(self):
        return {key[0]: getattr(self, key[0]) for key in self._fields_}

# 平台通用应答
class MsgCommonAck0x00(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('原消息ID', c_uint8),
        ('原消息序号', c_uint16),
        ('消息结果(0成功)', c_uint16),
    ]

    def as_dict(self):
        return {key[0]: getattr(self, key[0]) for key in self._fields_}

# 锁车控制
class MsgLockCtrl(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('协议类型', c_uint8),
        ('锁车命令', c_uint16),
    ]

    def as_dict(self):
        cxt = {0: '华菱锁车', 0x4D: '启用防拆', 0xCC: '关闭防拆', 0xE7: '限制转速', 0xD7: '限制扭矩', 0xF7: '切断喷油', 0xC3: '解锁', 0xCF: '查询'}
        return {key[0]: cxt[getattr(self, key[0])] for key in self._fields_}

# 锁车控制应答
class MsgLockCtrlAck(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('协议类型', c_uint8),
        ('ECU和终端的通信状态', c_uint8),
        ('ECU的故障状态', c_uint8),
        ('锁车功能开启', c_uint16, 2),
        ('是否收到解/锁车命令', c_uint16, 2),
        ('锁车类型', c_uint16, 2),
        ('初始化状态', c_uint8, 2),
        ('限制模式', c_uint8),
    ]

    def as_dict(self):
        return {key[0]: getattr(self, key[0]) for key in self._fields_}

# 转义处理
def ConvertMsg(data):
    packet = list()
    crc = 0
    i = 0
    while i < len(data):
        if data[i] == 0x22 and data[i+1] == 0x02:
            packet.append(0x23)
            crc = crc ^ 0x23
            i += 2
        elif data[i] == 0x22 and data[i+1] == 0x01:
            packet.append(0x22)
            crc = crc ^ 0x22
            i += 2
        else:
            packet.append(data[i])
            crc = crc ^ data[i]
            i += 1
    return bytes(packet), crc

def bcd2byte(bcd):
    return ((bcd & 0xf0) >> 4) * 10 + (bcd & 0x0f)

def ParseMsg(data):
    package = dict()
    data = data[1:-1]  # 剥离标识符23
    data, crc = ConvertMsg(data)
    if crc == 0:
        header = MsgHead()
        memmove(addressof(header), data, sizeof(MsgHead))
        package.update({"消息头": header.as_dict()})
        idx = sizeof(MsgHead)
        if header.消息ID == 0x83:
            y, m, d, hh, mm, ss, cnt = struct.unpack("<BBBBBBB", data[idx:idx + 7])
            idx += 7
            pack_time = datetime.datetime(2000 + bcd2byte(y), bcd2byte(m), bcd2byte(d), bcd2byte(hh), bcd2byte(mm), bcd2byte(ss), 0)
            package.update({"采集时间": pack_time.strftime('%Y-%m-%d %H:%M:%S')})
            for _ in range(cnt):
                if data[idx] == 0x01:
                    idx += 3
                    tmp = Msg0x83Body0x01()
                    memmove(addressof(tmp), data[idx:], sizeof(Msg0x83Body0x01))
                    package.update({"定位数据": tmp.as_dict()})
                    idx += sizeof(Msg0x83Body0x01)
                elif data[idx] == 0x40:
                    idx += 3
                    tmp = Msg0x83Body0x40()
                    memmove(addressof(tmp), data[idx:], sizeof(Msg0x83Body0x40))
                    package.update({"车辆数据": tmp.as_dict()})
                    idx += sizeof(Msg0x83Body0x40)
                elif data[idx] == 0x41:
                    idx += 3
                    tmp = Msg0x83Body0x41()
                    memmove(addressof(tmp), data[idx:], sizeof(Msg0x83Body0x41))
                    package.update({"锁车状态": tmp.as_dict()})
                    idx += sizeof(Msg0x83Body0x41)
                else:
                    print("error")
        elif header.消息ID == 0x00:
            tmp = MsgCommonAck0x00()
            memmove(addressof(tmp), data[idx:], sizeof(MsgCommonAck0x00))
            package.update({"平台通用应答": tmp.as_dict()})
            idx += sizeof(MsgCommonAck0x00)
            pass
        elif header.消息ID == 0x01:
            package.update({"终端心跳": 'null'})
            pass
        elif header.消息ID == 0xB7:
            cnt, cmd, data_len = struct.unpack("<BHH", data[idx:idx + 5])
            idx += 5
            for _ in range(cnt):
                if cmd == 0x0901:
                    tmp = MsgLockCtrl()
                    memmove(addressof(tmp), data[idx:], sizeof(MsgLockCtrl))
                    package.update({"锁车控制": tmp.as_dict()})
                    idx += sizeof(MsgLockCtrl)
                else:
                    package.update({"控制命令": '控制命令编号未识别'})
        elif header.消息ID == 0xC7:
            serial_no, cnt = struct.unpack("<HB", data[idx:idx + 3])
            package.update({"控制命令应答-原消息序号": serial_no})
            idx += 3
            for _ in range(cnt):
                cmd, data_len, ack = struct.unpack("<HHH", data[idx:idx + 6])
                idx += 6
                package.update({"控制命令应答-命令执行状态": ack})
                if cmd == 0x0901:
                    tmp = MsgLockCtrlAck()
                    memmove(addressof(tmp), data[idx:], sizeof(MsgLockCtrlAck))
                    package.update({"锁车控制应答": tmp.as_dict()})
                    idx += sizeof(MsgLockCtrlAck)
                else:
                    package.update({"控制命令应答": '控制命令编号未识别'})
        print(package)
    else:
        print('check crc error, raw_crc=%x, calc_crc=%x' % (data[-1], crc ^ data[-1]))

def main():
    print("使用格式： python xx.py 目录名(待解析文件放入该目录即可，文件编码确保是UTF8格式)")
    if len(sys.argv)-1 == 0:
        print('命令执行需要参数，见使用格式说明')
        return
    print("解析目录:", sys.argv[1])
    DirName = sys.argv[1]
    for root, dirs, files in os.walk(DirName):
        for name in files:
            file_name = os.path.join(root, name)
            print('-------------->Parse file:', file_name)
            with open(file_name, encoding='UTF-8') as fd:
                for line in fd:
                    try:
                        result = re.search(r'\D(23\w\w00.*23)\D', line)
                        if result:
                            data = result.group(1).strip()
                            #print(data)
                            ParseMsg(bytes.fromhex(data))
                            #break
                    except UnicodeDecodeError:
                        print("UnicodeDecodeError")
                        pass
            #break #一个文件

if __name__ == '__main__':
    main()

