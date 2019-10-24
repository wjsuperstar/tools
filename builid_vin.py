#!/usr/bin/python
# -*- coding: UTF-8 -*-
# auth:wujian 20191017

# 以下是配置根据vin和canid修改：
VIN=r"TEST0000000000001"
#VIN=r"LDP52A966JN427680"
CanId = 0x566

# 以下为代码，不允许修改。
def GetCheckSum(id, data):
    check_sum = ((id >> 24)&0xFF) + ((id>> 16)&0xFF) + ((id >> 8)&0xFF) + (id & 0xFF);
    for i in range(7):
        check_sum += data[i];

    while check_sum > 0xFF:
        check_sum = ((check_sum & 0xFF00)>>8) + (check_sum & 0xFF);
    
    check_sum = (~check_sum)&0xFF;
    return check_sum

def main():
    for idx in range(4):
        data=[]
        data.append(idx)
        for i in range(6):
            if idx == 0:
                data.append(0xff)
            else:
                vin_idx = i+6*(idx-1)
                if vin_idx < len(VIN):
                    data.append(ord(VIN[vin_idx]))
                else:
                    data.append(0xff)
        crc = GetCheckSum(CanId, data)
        data.append(crc)
        display=[hex(k) for k in data]
        print(" ".join(display))

if __name__ == '__main__':
    main()
