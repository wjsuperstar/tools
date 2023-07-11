#!/usr/bin/python
# -*- coding: UTF-8 -*-
# desc: 
# auth:wujian 2022-11-01
import sys
import os
import cv2
import numpy as np
from tcping import Ping
import logging
import urllib3
import certifi
import requests

def test_net():
    try:
        logging.error('test net: www.baidu.com:80')
        ping = Ping('www.baidu.com', 80, 500)  # 地址、端口、超时时间
        ping.ping(3)                           # ping命令执行次数
        ret = ping.result.table                # 以表格形式展现（ping.result.raw  # 原始形态，ping.result.rows  # 行显示）
        logging.error(ret)

        logging.error('test net: 18.177.237.209:21')
        ping = Ping('18.177.237.209', 21, 500)
        ping.ping(3)
        ret = ping.result.table  
        logging.error(ret)
    except Exception as e:
        logging.error(e)


if __name__ == '__main__':
    test_net()
