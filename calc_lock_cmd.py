#!/usr/bin/python
# -*- coding: UTF-8 -*-

opt_cmd_list = [0x4F, 0xCF, 0xE7, 0xD7, 0xF7, 0xC3, 0xCF]

seed = 0x9b
cmd_idx = 0

a = ~(seed ^ opt_cmd_list[cmd_idx])

print(hex(a&0xff));
