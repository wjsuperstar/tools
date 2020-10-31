#!/usr/bin/python
# -*- coding: UTF-8 -*-

#raw_str='2323014C47444348393147384B413134313236390101001C1401080E0806000338393836313131393232323033353530373837373A'
raw_str=''

#去掉头2323和校验码
hex_pack=bytes.fromhex(raw_str[4:-2])

def CalcCrc(in_list, list_len):
    t = 0;
    for i in range(0, list_len):
        t ^= in_list[i]
    return t

a = CalcCrc(hex_pack, len(hex_pack));

print('XOR=%#X' % a);