import time
import csv
import struct


SrcFile=r'D:\test\test_py\1111.csv'
DstFile=r'D:\test\test_py\example_can.dat'


can_id   = []
can_data = []

def parse_csv():
    with open(SrcFile) as csvfile:
        csv_reader = csv.reader(csvfile)  # 使用csv.reader读取csvfile中的文件
        header = next(csv_reader)  # 读取第一行每一列的标题
        for row in csv_reader:  # 将csv 文件中的数据保存到can_data中
            can_id.append(row[3])
            can_data.append(row[7])

def BuildFile():
    with open(DstFile, 'wb+') as fd:
        for i in range(len(can_id)):
            ticks = time.time()
            s = can_data[i].strip(' ')
            print(can_id[i])
            print(hex(int(ticks)))
            print(s)
            part1 = struct.pack("II", int(can_id[i], 16), int(ticks))
            #print(part1)
            part2 = b''
            for j in s.split(" "):
                part2 = part2 + struct.pack("B", int(j, 16))
            print("write len =", fd.write(part1 + part2))
    fd.close()

if __name__ == '__main__':
    parse_csv()
    BuildFile()


