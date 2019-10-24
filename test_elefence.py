#!/usr/bin/python
# -*- coding: UTF-8 -*-
#import pandas as pd
import csv
import re

FileName=r'D:\test\test_py\gps.csv'
GpsLog=r'D:\test\test_py\gps.txt'

latitude = []
longitude = [] 
'''
with open(FileName) as csv_fd:
    data = csv.reader(csv_fd)
    header = next(data)  # 读取第一行每一列的标题
    for row in data:
        longitude.append(int(float(row[5])*1e6))
        latitude.append(int(float(row[6])*1e6))
'''

# 经纬度单位转换：度分转为度 '3029.73514', '11409.67002'
def dm2dd(dm_lat, dm_longi):
    du_lat = dm_lat//100;
    du_longi = dm_longi//100
    fen_lat = (dm_lat - du_lat * 100)/60
    fen_longi = (dm_longi - du_longi * 100)/60
    fen_longi += du_longi
    fen_lat += du_lat;
    #print(fen_lat, fen_longi)
    return (fen_lat, fen_longi)

cnt=0
for row in open(GpsLog):
    if len(row) < 75:
        jw=re.findall(r"000,A,(.{9,11}?),N,(.{9,11}?),E,", row)
        if len(jw) > 0:
            #print("JW:", jw)
            cnt += 1
            (lat, longi)=dm2dd(float(jw[0][0]), float(jw[0][1]))
            latitude.append(int(lat*1e6))
            longitude.append(int(longi*1e6))
print("total:",cnt)

model_lat  =[30499364, 30496913, 30496373, 30496054, 30494209, 30492602, 30490949, 30489445, 30491058, 30492661]
model_longi=[114154602, 114158842, 114159423, 114159144, 114158068, 114156648, 114155268, 114153823, 114151149, 114148728]

'''
def is_in_area(ALongitude, ALatitude, model_lat, model_longi):
    #print("GPS:", ALatitude/1e6, ALongitude/1e6, sep=",")
    mJ = len(model_lat) - 1;
    mResult = 0
    for mI in range(len(model_lat)):
        #print("Model:", model_lat[mI], model_longi[mJ])
        if (model_lat[mI] < ALatitude and model_lat[mJ] >= ALatitude or model_lat[mJ] < ALatitude and model_lat[mI] >= ALatitude) and (model_longi[mI] <= ALongitude or model_longi[mJ] <= ALongitude):
            # 计算出当前位置在地图相邻两个点的直线上的映射，再计算出此射线与多边形相交的次数
            # 此处故意用整除，是为了模拟C语言整形运算
            if (((ALatitude - model_lat[mI]) ) / (model_lat[mJ] - model_lat[mI]) * (model_longi[mJ] - model_longi[mI])) < ALongitude - model_longi[mI] :
                mResult ^= 1
            else:
                mResult ^= 0
        mJ = mI;
    return mResult == 1;
    

'''
def is_in_area(ALongitude, ALatitude, model_lat, model_longi):
    c = 0
    j = len(model_lat) - 1
    for i in range(len(model_lat)):
        if ((model_lat[i] > ALatitude) != (model_lat[j] > ALatitude)) and (ALongitude < (model_longi[j] - model_longi[i]) * (ALatitude - model_lat[i]) / (model_lat[j] - model_lat[i]) + model_longi[i]):
            c = not c
        j = i
    return c;

in_area = 0
for i in range(len(longitude)):
    tmp = is_in_area(longitude[i], latitude[i], model_lat, model_longi)
    if tmp != in_area:
        in_area = tmp
        print("Area:", tmp)
        print(latitude[i]/1e6, longitude[i]/1e6, sep=",")
    

