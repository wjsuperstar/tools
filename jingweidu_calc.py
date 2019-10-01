#!/usr/bin/python
# -*- coding: UTF-8 -*-

FileName=r'D:\test\test_py\gps_point.txt'

file = open(FileName)
for line in file:
    t=line.split(" ")
    #print(t[0] + " " + t[1])
    print("%f,%f"%(int(t[1], 16)/1e6,int(t[0], 16)/1e6))
   