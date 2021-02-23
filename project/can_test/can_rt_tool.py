# -*- coding: UTF-8 -*-
# auth: WuJian  2020-12-11
# desc: 简易can收发器

from drv_can import *
import threading
import sys, getopt
import time
import datetime
import hashlib
import json

class TCanRxTxTool():
    def __init__(self, cfg_path = 'can_rt_tool.json'):
        self._cfg_path = cfg_path
        self._tx_enable = False
        self._hide_rx  = False
        self._hide_tx = False
        self._cfg_period = None
        self._tick = dict()
        self._tx_tick = dict()
        self._baud = BAUD_250K
        self._check_period = 0
        self.rx_filter_en = False

    def store(self, data):
        with open(self._cfg_path, 'w') as fw:
            json.dump(data, fw)
    def load(self):
        try:
            with open(self._cfg_path, 'r', encoding='utf-8') as fw:
                return json.load(fw)
        except FileNotFoundError:
            return None
            pass
    def display(self, hide, tag, can_id, data):
        if not hide:
            dt_ms = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
            print(dt_ms, tag, hex(can_id), [hex(i) for i in data])
    # CAN报文接收处理线程
    def handle_recv(self, f_can):
        while True:
            len, can_id, data = f_can.read()
            if len > 0:
                idx = 0
                if self.rx_filter_en :
                    for rx_item in self._rx_cfg:
                        rx_id   = int(rx_item['id'], 16)
                        if can_id == rx_id:
                            if self._check_period > 0:
                                t = time.time()
                                ms_t = int(round(t * 1000))  # 毫秒级时间
                                rx_period = rx_item['period']
                                last_tick = self._tick.get(can_id, ms_t)
                                offset_t = ms_t - last_tick
                                if offset_t >= rx_period * (1-self._check_period) and offset_t < rx_period*(1+self._check_period):
                                    self.display(self._hide_rx, "RX", can_id, data)
                                else:
                                    print("[%s] Period Error, offset=%d" % (hex(can_id), offset_t))
                                self._tick[can_id] = ms_t
                        idx += 1
                else:
                    self.display(self._hide_rx,"RX", can_id, data)

    def start(self):
        cfg = self.load()
        if cfg:
            print('Use Config:', json.dumps(cfg, ensure_ascii=False, indent=1))
            if cfg['tx_enable'] > 0:
                self._tx_enable = True
            if cfg['hide_tx'] > 0:
                self._hide_tx = True
            if cfg['hide_rx'] > 0:
                self._hide_rx = True
            if cfg['rx_filter_en'] > 0:
                self.rx_filter_en = True
            self._check_period = cfg['check_rx_period']
            self._baud       = cfg['baud']
            self._tx_cfg     = cfg['tx_cfg']
            self._rx_cfg     = cfg['rx_cfg']
            if self._baud == 250:
                self._baud = BAUD_250K
            elif self._baud == 500:
                self._baud = BAUD_500K

            if self._check_period > 100:
                self._check_period = 0
            else:
                self._check_period /= 100

        self._f_can = ZlgCanDev(baud=self._baud)
        self._f_can.open()
        self._receive_handler = threading.Thread(target=self.handle_recv, args=(self._f_can,))
        self._receive_handler.start()
        while True:
            if self._tx_enable:
                idx = 0
                for tx_item in self._tx_cfg:
                    t = time.time()
                    ms_t = int(round(t * 1000))  # 毫秒级时间戳
                    tx_id     = int(tx_item['id'], 16)
                    tx_period = tx_item['period']
                    last_tick = self._tx_tick.get(idx, 0)
                    if ms_t - last_tick >= tx_period:
                        tx_data = [int(i, 16) for i in tx_item['data']]
                        self.display(self._hide_tx, "TX", tx_id, tx_data)
                        self._f_can.write(tx_id, tx_data)
                        self._tx_tick[idx] = ms_t
                    idx += 1

            time.sleep(0.005)

if __name__ == '__main__':
    obj = TCanRxTxTool()
    obj.start()
