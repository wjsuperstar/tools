#!/usr/bin/python
# -*- coding: UTF-8 -*-
# desc:Analyze GSENSOR data collection frequency 
# auth:wujian 20220221
import sys
import re
import codecs

class AnalyzeFile:
    def __init__(self, file_name, min_ms, max_ms):
        self._file_name = file_name
        self._line_no = 0
        self._last_time = 0
        self._min_ms = min_ms
        self._max_ms = max_ms
        print(f"检查范围:[{self._min_ms}ms, {self._max_ms}ms]")
        
    def analyze(self):
        #with open(self._file_name, encoding='utf8') as fd:
        with codecs.open(self._file_name, 'r', encoding='utf8') as fd:
            for row in fd:
                self._line_no = self._line_no+1
                result = re.search(r'gsensor_dcallback', row)
                if result:
                    data = row.strip().split(r' ')
                    ti_str = data[7].split(r':')
                    #print('ti_str=', ti_str)
                    ti_int = int(ti_str[1], 16)
                    if self._last_time != 0:
                        diff_ti = ti_int - self._last_time
                        diff_ti = diff_ti/1000000
                        #print("diff_ti=", diff_ti)
                        if diff_ti > self._max_ms or diff_ti < self._min_ms:
                            print(f'错误输出频率:{diff_ti}, 行号:{self._line_no}, 内容:{row}')
                    self._last_time = ti_int
                    

def main():
    print("usage: python dvr-gsensor.py file_name min_ms max_ms")
    print("脚本功能是把不在[min_ms, max_ms]范围内的Gsensor数据打印出来")
    obj = AnalyzeFile(sys.argv[1], float(sys.argv[2]), float(sys.argv[3]))
    obj.analyze()

if __name__ == '__main__':
    main()