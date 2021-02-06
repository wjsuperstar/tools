import time
import csv
import struct


#SrcFile=r'D:\test\test_py\1111.csv'
SrcFile=r'D:\test\test_py\ldd.txt'
DstFile=r'D:\test\test_py\example_can.dat'


can_id   = []
can_data = []

# 根据csv原始文件生成
def parse_csv():
    with open(SrcFile) as csvfile:
        csv_reader = csv.reader(csvfile)  # 使用csv.reader读取csvfile中的文件
        header = next(csv_reader)  # 读取第一行每一列的标题
        for row in csv_reader:  # 将csv 文件中的数据保存到can_data中
            can_id.append(row[3])
            can_data.append(row[7])

# 根据txt原始文件生成
def parse_txt():
    with open(SrcFile) as fd:
        next(fd)
        for row in fd: 
            line = row.split('  ')
            #print(line[12].strip())
            can_id.append(line[6])
            can_data.append(line[12])

def BuildFile():
    with open(DstFile, 'wb+') as fd:
        for i in range(len(can_id)):
            ticks = time.time()
            s = can_data[i].strip()
            #print(can_id[i])
            id=int(can_id[i], 16)
            if id > 0x7ff:
                part1 = struct.pack("II", id, int(ticks))
                #print(part1)
                part2 = b''
                for j in s.split(" "):
                    part2 = part2 + struct.pack("B", int(j, 16))
                print("write len =", fd.write(part1 + part2))
                

'''
def parse_id():
    with open(SrcFile) as f:
        for line in f:
            can_id.append(int(line, 16))



def BuildFile():
    with open(DstFile, 'wb+') as fd:
        idx = 0
        for i in range(100000):
            ticks = time.time()
            if (idx >= len(can_id)):
                idx = 0
            print(hex(can_id[idx]))
            #print("idx=", idx)
            #print(hex(int(ticks)))
            part1 = struct.pack("II", can_id[idx], int(ticks))
            #print(part1)
            part2 = b'\x00\x01\x02\x03\x04\x05\x06\x07'
            print("write len =", fd.write(part1 + part2))
            idx += 1
'''

if __name__ == '__main__':
    parse_txt()
    BuildFile()


