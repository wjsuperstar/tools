# -*- coding: UTF-8 -*-
# auth: WuJian  20201029
# desc: 陕汽模拟服务器
import socket
import threading
from parse_sq_le import *

bind_ip = "0.0.0.0"  #监听所有可用的接口
bind_port = 40228   #非特权端口号都可以使用
g_online = False
g_vin = ""

def deal_recv_data(client_socket, data):
    obj = SqParseMsg()
    package = obj.parse_main_msg(data)
    print(package)
    try:
        cmd = package["消息头"]["命令标识"]
        if cmd == 0x02:
            '''
            d_arry = bytearray(data)
            d_arry[3] = 1
            d_arry[-1] = parse_gb32960.CalcCrc(d_arry[2:-1])
            client_socket.send(bytes(d_arry))
            '''
        elif cmd == 0x03:
            pass
        elif cmd == 0x01:
            d_arry = bytearray(data)
            d_arry[3] = 1
            d_arry[-1] = parse_gb32960.CalcCrc(d_arry[2:-1])
            client_socket.send(bytes(d_arry))
            global g_online, g_vin
            g_online = True
            g_vin = package['消息头']['VIN']
            send_info = key_exchange_msg(sm4_key_, g_vin)
            client_socket.send(send_info)
            print("密钥下发", send_info.hex())

        elif cmd == 0x04:
            pass
        elif cmd == 0x07:
            d_arry = bytearray(data)
            d_arry[3] = 1
            d_arry[-1] = parse_gb32960.CalcCrc(d_arry[2:-1])
            client_socket.send(bytes(d_arry))

            pass
        elif cmd == 0xef:
            pass

    except KeyError:
        print('msg error.')


#客户处理线程
def handle_client(client_socket):
    while True:
        request = client_socket.recv(4096)
        if len(request) > 24:
            dt_ms = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
            print("[%s] Received: %s" % (dt_ms, request.hex()))
            deal_recv_data(client_socket, request)
            #client_socket.close()

#输入事件处理
def handle_event(client_socket):
    while True:
        data = input("输入指令(cmd pa1 pa2): ")
        if len(data) > 2:
            res = data.strip().split(' ')
            cmd = int(res[0])
            param = int(res[1])
            param2 = int(res[2])
            print("cmd=%d, param=%d, param2=%d" % (cmd, param, param2))
            if cmd == 1:  # 车门
                package = struct.pack(">BB", cmd, param)
                remote_ctrl_msg(client_socket, package)
                pass
            elif cmd == 2:  # 空调
                package = struct.pack(">BBH", cmd, param, param2)
                remote_ctrl_msg(client_socket, package)
            elif cmd == 3:  # 车灯
                package = struct.pack(">BB", cmd, param)
                remote_ctrl_msg(client_socket, package)
            elif cmd == 4:  # 车窗
                package = struct.pack(">BBB", cmd, param, param2)
                remote_ctrl_msg(client_socket, package)
            elif cmd == 5:  # 锁车
                package = struct.pack(">BBH", cmd, param, param2)
                remote_ctrl_msg(client_socket, package)
            elif cmd == 6:  # 车钥
                package = struct.pack(">BB", cmd, param)
                remote_ctrl_msg(client_socket, package)
            elif cmd == 7:  # 寻车
                package = struct.pack(">BBB", cmd, param, param2)
                remote_ctrl_msg(client_socket, package)
            elif cmd == 99 and g_online:
                send_info = key_exchange_msg(sm4_key_, g_vin)
                client_socket.send(send_info)
                print("密钥下发", send_info.hex())

def main():
    # AF_INET：使用标准的IPv4地址或主机名，SOCK_STREAM：说明这是一个TCP服务器
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((bind_ip, bind_port))
    print(f"[*] Listening on {bind_ip}:{bind_port}")
    # 最大连接数
    server.listen(5)
    while True:
        #等待客户连接，连接成功后，将socket对象保存到client，将细节数据等保存到addr
        client, addr = server.accept()
        dt_ms = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        print("[%s] Acception connection from %s:%d" % (dt_ms, addr[0],addr[1]))
        client_handler = threading.Thread(target=handle_client,args=(client,))
        client_handler.start()
        input_event = threading.Thread(target=handle_event, args=(client,))
        input_event.start()

if __name__ == '__main__':
    main()
