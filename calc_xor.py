#!/usr/bin/python
# -*- coding: UTF-8 -*-

#raw_str='232301FE485154455354443032303031303532323701001E140B0514373B009C3839383630303036313131373531303235343931010035'


raw_str='232301FE485154455354443032303031303532323701001E140B0A0F3B1E002738393836303030363131313735313032353439310100B3'

data = list(raw_str)
data[6] = '0'
data[7] = '1'

raw_str = ''.join(data)

#去掉头2323和校验码
hex_pack=bytes.fromhex(raw_str[4:-2])

def CalcCrc(in_list, list_len):
    t = 0;
    for i in range(0, list_len):
        t ^= in_list[i]
    return t

a = CalcCrc(hex_pack, len(hex_pack));

print(format('XOR=%02X' % a));

s = raw_str[0:-2] + format('%02X' % a)

print(s)

