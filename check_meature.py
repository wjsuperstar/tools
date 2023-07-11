#!/usr/bin/python
# -*- coding: UTF-8 -*-
# author: WuJian

import os
import sys
import tarfile


def untar(fname, dirs):
    """
    解压tar.gz文件
    :param fname: 压缩文件名
    :param dirs: 解压后的存放路径
    :return: bool
    """
    try:
        t = tarfile.open(fname)
        #print(t.getnames())
        t.extractall(path=dirs)
        t.close()
        return True
    except Exception as e:
        print(e)
        return False


def main():
    print("使用格式： python xx.py 目录名(递归解析目录内的数据文件)")
    DirName = "obu"
    try:
        DirName = sys.argv[1]
    except IndexError:
        pass
    print("解析目录:", DirName)
    for root, dirs, files in os.walk(DirName):
        for name in files:
            file_name = os.path.join(root, name)
            if file_name.endswith('.tgz'):
                print("unpack .tgz: ", file_name)
                unpack_dir = file_name.split('.')[0]
                print(unpack_dir)
                untar(file_name, unpack_dir)

    for root, dirs, files in os.walk(DirName):
        for name in files:
            file_name = os.path.join(root, name)
            if file_name.endswith('.tar.gz'):
                print("unpack .tar.gz: ", file_name)
                unpack_dir = os.path.dirname(file_name)
                untar(file_name, unpack_dir)

    for root, dirs, files in os.walk(DirName):
        for name in files:
            file_name = os.path.join(root, name)
            if file_name.endswith('.log'):
                print('-------------->check ', file_name)
                row_num = 0
                with open(file_name) as fd:
                    for line in fd:
                        try:
                            # print(line)
                            row_num += 1
                            data = line.split(',')[25]
                            if data == 'measureStatus':
                                continue
                            measureStatus = int(data)
                            if measureStatus != 1:
                                print('Check not position------->file_name=%s, row_number=%d, measureStatus=%d' % (
                                file_name, row_num, measureStatus))
                        except AttributeError:
                            continue
                        # break #一行
                # break #一个文件


if __name__ == '__main__':
    main()
    input("close window to quit.")
