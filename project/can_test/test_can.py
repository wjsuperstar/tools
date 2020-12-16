import can
import random
import cantools
import time
import json
import sys, getopt

def display_help():
    print('用法：xx.py -i DBC文件 -r 随机种子')
    print('-b CAN波特率，500k: 500000, 250k: 250000, 默认500k，发送到第0通道，通道不可配')
    print('-i DBC文件，确保最大值，最小值已配置，脚本根据该文件配置规则发送数据can总线上')
    print('-r 随机种子，若种子相同，则发送值相同，便于分析数据。并输出can_data.json, 记录dbc信号发送的实际值')
    print('-c 循环发送次数，发送相同序列的值的轮数, 默认1轮')
def parse_cmd_param():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hi:r:c:", ["indbc=", "random=", "count="])
    except getopt.GetoptError:
        display_help()
        sys.exit(-1)

    a = None
    b = 12345
    c = 1
    d = 500000
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            display_help()
            sys.exit(0)
        elif opt in ("-i", "--infile"):
            a = arg
        elif opt in ("-r", "--random"):
            b = int(arg)
        elif opt in ("-c", "--count"):
            c = int(arg)
        elif opt in ("-b", "--baud"):
            c = int(arg)

    if a is None:
        display_help()
        sys.exit(-1)

    return a, b, c, d

def store(data):
    with open('can_data.json', 'w') as fw:
        # 将字典转化为字符串
        # json_str = json.dumps(data)
        # fw.write(json_str)
        # 上面两句等同于下面这句
        json.dump(data, fw)

def main():
    file, seed, send_cnt, b = parse_cmd_param()
    bus = can.interface.Bus(bustype = 'canalystii', channel = 0, baud = b)
    db = cantools.db.load_file(file)
    as_cfg = dict()
    for i in range(send_cnt):
        print('--------------------->发送次数:', i)
        random.seed(seed)
        for message in db.messages:
            #print(message.length)
            if message.length <= 8:
                # min(int(sig.minimum), 2^sig.length), min(int(sig.maximum), 2^sig.length)
                send_data = {sig.name: random.randint(int(sig.minimum), int(sig.maximum)) for sig in message.signals}
                print(send_data)
                if i == 0:
                    as_cfg.update(send_data)
                    # print(as_cfg)
                    store(as_cfg)
                data=message.encode(send_data)
                msg = can.Message(arbitration_id=message.frame_id, data=data)
                bus.send(msg)
                time.sleep(0.01)
        time.sleep(1)

if __name__ == '__main__':
    main()
