#!/usr/bin/python
# -*- coding: UTF-8 -*-

raw_str='2323F101544553543030303030303030303030303101000700000002793D0097'

#去掉头2323和校验码
hex_pack=bytes.fromhex(raw_str[4:-2])

def CalcCrc(in_list, list_len):
    t = 0;
    for i in range(0, list_len):
        t ^= in_list[i]
    return t

a = CalcCrc(hex_pack, len(hex_pack));

print('XOR=%#X' % a);