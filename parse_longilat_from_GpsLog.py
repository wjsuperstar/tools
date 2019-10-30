#!/usr/bin/python
# -*- coding: UTF-8 -*-
import re

class ParseGps:
    def __init__(self, file_name):
        self.__GpsPoints = []
        with open(file_name) as fd:
            for row in fd:
                if len(row) < 80:
                    jw=re.findall(r"000,A,(.{9,11}?),N,(.{9,11}?),E,", row)
                    if len(jw) > 0:
                        gps=self.dm2dd(float(jw[0][0]),float(jw[0][1]))
                        self.__GpsPoints.append(gps)
                        
    def dm2dd(self, dm_lat, dm_longi):
        du_lat = dm_lat//100;
        du_longi = dm_longi//100
        fen_lat = (dm_lat - du_lat * 100)/60
        fen_longi = (dm_longi - du_longi * 100)/60
        fen_longi += du_longi
        fen_lat += du_lat;
        #print(fen_lat, fen_longi)
        return (fen_lat, fen_longi)

    def display(self):
            print("总共:", len(self.__GpsPoints))
            for i in self.__GpsPoints:
                print("%f,%f" % i)
    
    def get_gps_point(self):
        return self.__GpsPoints
        

def main():
    GpsLogPath = r'GPS_0.log'
    ParseGps(GpsLogPath).display()

if __name__ == '__main__':
    main()