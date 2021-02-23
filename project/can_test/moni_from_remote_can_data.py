
from drv_can import *
import time
import os
import sys

import os
import sys

print("使用格式： python xx.py 目录名 解析标志")
print("解析目录:", sys.argv[1])
DirName =sys.argv[1]
dc = ZlgCanDev(baud = BAUD_250K)
line_no = 0

def parse_txt(line):
    td = line.split(r" ")
    id = int(td[1], 16)
    data = []
    for i in range(8):
        data.append(int(td[6+i], 16))
    print(hex(id))
    dc.write(id, data)
    time.sleep(0.01)

def parse_asc(line):
    global line_no
    line_no += 1
    if line_no > 3:
        td = line.strip().split(r" ")
        #print(td)
        id = td[2][0:-1]
        id = int(id, 16)
        data = []
        for i in range(8):
            data.append(int(td[-i-1], 16))
        data.reverse()
        print('id =', hex(id), [hex(i) for i in data])
        dc.write(id, data)
        time.sleep(0.01)

def main():
    last_time = 0
    for root, dirs, files in os.walk(DirName):
        for name in files:
            file_name = os.path.join(root, name)
            if file_name.endswith('.txt') or file_name.endswith('.asc'):
                print('-------------->open ', file_name)
                with open(file_name) as fd:
                    for line in fd:
                        try:
                            if file_name.endswith('.txt'):
                                parse_txt(line)
                            elif file_name.endswith('.asc'):
                                parse_asc(line)
                        except AttributeError:
                            # 忽略不合法的数据
                            continue
                #break #一个文件
if __name__ == '__main__':
    main()