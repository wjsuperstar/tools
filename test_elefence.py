#!/usr/bin/python
# -*- coding: UTF-8 -*-
#import pandas as pd
import csv

FileName=r'D:\test\test_py\gps.csv'

latitude = []
longitude = []
with open(FileName) as csv_fd:
    data = csv.reader(csv_fd)
    header = next(data)  # 读取第一行每一列的标题
    for row in data:
        longitude.append(int(float(row[5])*1e6))
        latitude.append(int(float(row[6])*1e6))


model_lat  =[30499364, 30496913, 30496373, 30496054, 30494209, 30492602, 30490949, 30489445, 30491058, 30492661]
model_longi=[114154602, 114158842, 114159423, 114159144, 114158068, 114156648, 114155268, 114153823, 114151149, 114148728]

def is_in_area(ALongitude, ALatitude, model_lat, model_longi):
    print("GPS:", ALatitude/1e6, ALongitude/1e6, sep=",")
    mJ = len(model_lat) - 1;
    mResult = 0
    for mI in range(len(model_lat)):
        #print("Model:", model_lat[mI], model_longi[mJ])
        if (model_lat[mI] < ALatitude and model_lat[mJ] >= ALatitude or model_lat[mJ] < ALatitude and model_lat[mI] >= ALatitude) and (model_longi[mI] <= ALongitude or model_longi[mJ] <= ALongitude):
            # 计算出当前位置在地图相邻两个点的直线上的映射，再计算出此射线与多边形相交的次数
            if (model_longi[mI] + (ALatitude - model_lat[mI]) / (model_lat[mJ] - model_lat[mI]) * (model_longi[mJ] - model_longi[mI])) < ALongitude:
                mResult ^= 1
            else:
                mResult ^= 0
        mJ = mI;
    return mResult == 1;
    
    
for i in range(len(longitude)):
    print(is_in_area(longitude[i], latitude[i], model_lat, model_longi))
    