import os
import re
import sys
import struct
import parse_gb32960





def main():
    print("使用格式： python xx.py 目录名(待解析文件放入该目录即可，文件编码确保是UTF8格式)")
    if len(sys.argv)-1 == 0:
        print('命令执行需要参数，见使用格式说明')
        return
    DirName = sys.argv[1]
    print("解析目录:", DirName)
    for root, dirs, files in os.walk(DirName):
        for name in files:
            file_name = os.path.join(root, name)
            print('-------------->Parse file:', file_name)
            with open(file_name, encoding='UTF-8') as fd:
                for line in fd:
                    try:
                        result = re.search(r'\D(2323.*)\D', line)
                        if result:
                            data = result.group(1).strip()
                            print(data)
                            obj = parse_gb32960.MainParseMsg()
                            package = obj.parse_main_msg(bytes.fromhex(data))
                            print(package)
                            #break
                    except UnicodeDecodeError:
                        print("UnicodeDecodeError")
                        pass
            #break #一个文件

if __name__ == '__main__':
    main()
