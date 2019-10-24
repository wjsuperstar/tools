#!/usr/bin/python
# -*- coding: UTF-8 -*-

import configparser

config_file_path = r'D:\test\test_py\FenceMap.txt'

def GetGpsPoint(file_name):
    cf = configparser.ConfigParser()
    cf.read(file_name)
    return cf.get("Road", "Point0")

def main():
    num = 0
    point=GetGpsPoint(config_file_path);
    #print(point)
    t = point.split(",")
    cnt = len(t) - len(t)%2
    for i in range(0, cnt, 2):
        num += 1
        print("%f,%f"%(int(t[i+1], 10)/1e6,int(t[i], 10)/1e6))
    print("num=", num)

if __name__ == '__main__':
    main()