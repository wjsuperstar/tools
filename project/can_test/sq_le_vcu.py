# -*- coding: UTF-8 -*-
# auth: WuJian  2020-12-11
# desc: 陕汽LE模拟VCU工具

from drv_can import *
import threading
import sys, getopt
import time
import random
import hashlib
import json

kSqSsSendSeed   = 0   # 发送种子
kSqSsWaitMd5Key = 1   # 等待密钥
kSqSsCheckSucc  = 2   # VCU校验成功
kSqSsCheckFail  = 3   # VCU校验失败
kSqSsIdle       = 4   # 空闲

class TSqleVcu():
    def __init__(self, baud = BAUD_500K, cfg_path = 'vcu_cfg.json'):
        self._f_can = ZlgCanDev(baud = baud)
        self._cfg_path = cfg_path
        self._fixed_key_status   = 0
        self._lock_active_status = 0
        self._speed_limit_status = 0
        self._shake_status = kSqSsIdle
        self._lock_cmd = 0
        self._lock_cmd_param = 0
        self._seed = []
        self._cfg = dict()

    def store(self, data):
        with open(self._cfg_path, 'w') as fw:
            json.dump(data, fw)
    def load(self):
        try:
            with open(self._cfg_path, 'r') as fw:
                return json.load(fw)
        except FileNotFoundError:
            return None
            pass
    def shake_check(self):
        if self._shake_status == kSqSsSendSeed:
            data = [random.randint(i, 254) for i in range(8)]
            self._seed = data[2:]
            print(time.strftime('%Y-%m-%d %H:%M:%S'), 'build seed =', bytes(self._seed).hex())
            data[0] = 0x05
            data[1] = 0x01
            self._f_can.write(0x18FD0127, data)
            self._shake_status = kSqSsWaitMd5Key
        elif self._shake_status == kSqSsCheckSucc:
            data = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]
            data[0] = 0x11
            data[1] = 0x01
            self._f_can.write(0x18FD0127, data)
            self._shake_status = kSqSsIdle
            pass
        elif self._shake_status == kSqSsCheckFail:
            data = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]
            data[0] = 0x01
            data[1] = 0x01
            self._f_can.write(0x18FD0127, data)
            self._shake_status = kSqSsSendSeed
            pass

    # CAN报文接收处理线程
    def handle_recv(self, f_can):
        while True:
            len, can_id, data = f_can.read()
            if len > 0:
                #print('recv id=', hex(can_id), [hex(i) for i in data])
                if can_id == 0x18FE00EB:  # 固定密钥
                    print(time.strftime('%Y-%m-%d %H:%M:%S'), '固定密钥报文 ', hex(can_id), [hex(i) for i in data])
                    self._fixed_key_status = 1
                    self._cfg.update({'fixed_key_status': self._fixed_key_status})
                    if self._lock_active_status == 1:
                        self._shake_status = kSqSsSendSeed
                    print('保存配置1.')
                    self.store(self._cfg)
                elif can_id == 0x18FE01EB:  # 锁车和解锁id
                    print(time.strftime('%Y-%m-%d %H:%M:%S'), '锁车握手报文 ', hex(can_id), [hex(i) for i in data])
                    EVT_LockReqType = data[0] & 0x03
                    EVT_LockCmd     = data[1] & 0x0f
                    if EVT_LockReqType == 0x01: # 0x1:反馈密钥
                        if self._shake_status == kSqSsWaitMd5Key:
                            EVT_LockKey = bytes(data[2:]).hex()
                            digest = hashlib.md5(bytes(self._seed)).hexdigest()
                            digest = digest[0:12]
                            print('calc digest=', digest, 'recv digest=', EVT_LockKey)
                            if digest == EVT_LockKey:
                                print('MD5握手校验成功.')
                                self._shake_status = kSqSsCheckSucc
                            else:
                                print('MD5握手校验失败.')
                                self._shake_status = kSqSsCheckFail
                        else:
                            self._shake_status = kSqSsSendSeed
                    elif EVT_LockReqType == 0x00: # 0x0:锁车指令
                        cmd_desc = {0x1:'握手校验',0x3:'激活锁车配置功能', 0x4:'关闭锁车配置功能',0x7:'限制车速', 0x8:'解除限制车速'}
                        print('锁车指令(%d):%s' % (EVT_LockCmd, cmd_desc[EVT_LockCmd]))
                        self._lock_cmd = EVT_LockCmd
                        if self._lock_cmd == 3:
                            self._lock_active_status = 1
                        elif self._lock_cmd == 4:
                            self._lock_active_status = 0
                        elif self._lock_cmd == 7:
                            self._speed_limit_status = 1
                        elif self._lock_cmd == 8:
                            self._speed_limit_status = 0
                        self._cfg.update({'lock_cmd':self._lock_cmd})
                        self._cfg.update({'lock_active_status': self._lock_active_status})
                        self._cfg.update({'speed_limit_status': self._speed_limit_status})
                        print('保存配置2.')
                        self.store(self._cfg)
                elif can_id == 0x18FE02EB:  # 车速/转速限制
                    print(time.strftime('%Y-%m-%d %H:%M:%S'), ' 下发车速报文 ', hex(can_id), [hex(i) for i in data])
                    self._lock_cmd_param = data[0]
                    print('车速:', self._lock_cmd_param)
                elif can_id == 0x18FFF6EB:
                    print(time.strftime('%Y-%m-%d %H:%M:%S'), ' 预警报文 ', hex(can_id), [hex(i) for i in data])
    def start(self):
        cfg = self.load()
        if cfg:
            self._cfg = cfg
            self._fixed_key_status   = self._cfg['fixed_key_status']
            self._lock_active_status = self._cfg['lock_active_status']
            self._speed_limit_status = self._cfg['speed_limit_status']
        if self._lock_active_status == 1:
            self._shake_status = kSqSsSendSeed
        self._f_can.open()
        self._receive_handler = threading.Thread(target=self.handle_recv, args=(self._f_can,))
        self._receive_handler.start()
        while True:
            data = [0, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]
            data[0] = self._fixed_key_status | (self._lock_active_status << 2) | (self._speed_limit_status << 4)
            #print(hex(data[0]))
            self._f_can.write(0x18FD0027, data)
            time.sleep(0.5)
            self.shake_check()

def main():
    vcu = TSqleVcu()
    vcu.start()

if __name__ == '__main__':
    main()