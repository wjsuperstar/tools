# -*- coding: UTF-8 -*-
# auth: WuJian  20201029
# desc: 陕汽4.5t模拟服务器
import time
import datetime
import os
import re
import struct
import socket
import threading
import parse_gb32960
from gmssl import sm2, sm3, func
from gmssl.sm4 import CryptSM4, SM4_ENCRYPT, SM4_DECRYPT

bind_ip = "0.0.0.0"  #监听所有可用的接口
bind_port = 40228   #非特权端口号都可以使用
pack_prop_plaintext_ = 0
pack_prop_sm4_ = 1
sign_k_val_ = '3132333435363738'
sta_private_key_ = 'F55B3E38750F4993DC35FE295925AB82E168F42AC50C1DA5C571A87697160B4B'
sta_public_key_ = '8B5802223A98E1891923A103EE4FE08DE39F62D18C8DF9EB4B7F5153E9CD23B081E57D7BD954FDFFDD88AEBC04041F0228CE9E350F735F82ECB0E7013BD597AB'
pla_private_key_ = '98E39D034EACD72AE56433D42488CF849E0F1FFFAE72EA8789BA8644A375B3B7'
pla_public_key_ = '73F1CAA35C035E93F76539756854EE0D183970C6ADA8058A5DE7DF43674816ACD0F0C1E11AEA2888BF32404272B3BBFB3A9A853252FCF70A0B1F3F6803E55117'
sm4_key_ = b'3l5butlj26hvv313'
msg_serial_num_ = 0
vehicle_vin_ = b'1234567890wujian0'
logon_flg_ = False

def encode_std_npv(cmd, ack_flg, vin, encrypt, data):
    head_id = 0x2323
    data_len = len(data)
    package = struct.pack(">HBB17sBH%ds" % data_len, head_id, cmd, ack_flg, vin, encrypt, data_len, data)
    crc = '%02x' % parse_gb32960.CalcCrc(package)
    package += bytes.fromhex(crc)
    return package

def encode_sq_lay1(encrpt, data, pack_time):
    head_id = 0x5351
    pack_prop = (encrpt & 0x0f)
    data_len = len(data)
    package = struct.pack(">HHH%dsI" % data_len, head_id, pack_prop, data_len, data, pack_time)

    sm2_crypt = sm2.CryptSM2(public_key=None, private_key=pla_private_key_)
    sign = sm2_crypt.sign(package, sign_k_val_)
    print('sign:', sign)
    package += bytes.fromhex(sign)
    return package

def encode_sq_lay2(msg_id, encrpt, data):
    global msg_serial_num_
    msg_prop = 0x20
    data_len = len(data)
    package = struct.pack(">HHHH%ds" % data_len, msg_prop, msg_id, msg_serial_num_, data_len, data)
    crc = '%02x' % parse_gb32960.CalcCrc(package)
    package += bytes.fromhex(crc)
    msg_serial_num_ += 1
    #print(package)
    if encrpt == pack_prop_sm4_:
        crypt_sm4 = CryptSM4()
        crypt_sm4.set_key(sm4_key_, SM4_ENCRYPT)
        package = crypt_sm4.crypt_ecb(package)
    return package

def key_exchange_msg(buf, vin):
    global vehicle_vin_
    vehicle_vin_ = vin
    sm2_crypt = sm2.CryptSM2(public_key=sta_public_key_, private_key=None)
    sm4_key = sm2_crypt.encrypt(buf)
    print('sm4_key:', sm4_key.hex())
    data_len = len(sm4_key)
    key_type = 1
    unix_tm = int(time.time())
    package = struct.pack(">BH%dsI" % data_len, key_type, data_len, sm4_key, unix_tm)
    l2 = encode_sq_lay2(0xff00, pack_prop_plaintext_, package)
    l1 = encode_sq_lay1(pack_prop_plaintext_, l2, unix_tm)
    return encode_std_npv(0xFA, 0xFE, vin, 1, l1)

def remote_ctrl_msg(client_socket, data):
    unix_tm = int(time.time())
    l2 = encode_sq_lay2(0xfb00, pack_prop_sm4_, data)
    l1 = encode_sq_lay1(pack_prop_sm4_, l2, unix_tm)
    msg = encode_std_npv(0xFA, 0xFE, vehicle_vin_, 1, l1)
    client_socket.send(msg)

def deal_send_data(client_socket, package):
    pass
    #if logon_flg_:
    #    client_socket.send(key_exchange_msg(sm4_key_, package['消息头']['VIN']))

class Sq45tParseMsg(parse_gb32960.MainParseMsg):
    def __init__(self):
        super().__init__()
        #self.__data = data
    def parse_custom_msg(self, cmd, data):
        package = dict()
        if cmd == 0xFB:
            idx = 0
            tot_len = len(data)
            used_len = [0]
            print('陕汽0xFB上行消息，待解析')

def deal_recv_data(client_socket, data):
    obj = Sq45tParseMsg()
    package = obj.parse_main_msg(data)
    #print(package)
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
            global logon_flg_
            logon_flg_ = True
        elif cmd == 0x04:
            pass
        elif cmd == 0x07:
            send_info = key_exchange_msg(sm4_key_, package['消息头']['VIN'])
            print("密钥下发", send_info.hex())
            client_socket.send(send_info)
            pass
        elif cmd == 0xef:
            pass

        deal_send_data(client_socket, package)
    except KeyError:
        print('msg error.')


#客户处理线程
def handle_client(client_socket):
    while True:
        request = client_socket.recv(2048)
        print("[*] Received: %s" % request)
        deal_recv_data(client_socket, request)
        #client_socket.close()

#输入事件处理
def handle_event(client_socket):
    while True:
        data = input("输入指令(cmd param): ")
        if len(data) > 2:
            res = data.strip().split(' ')
            cmd = int(res[0])
            param = int(res[1])
            print("cmd=%d, param=%d" % (cmd, param))
            if cmd == 1:  # 车门
                package = struct.pack(">B", cmd)
                remote_ctrl_msg(client_socket, package)
                pass
            elif cmd == 2:  # 空调
                package = struct.pack(">BH", cmd, param)
                remote_ctrl_msg(client_socket, package)
            elif cmd == 3:  # 车灯
                package = struct.pack(">B", cmd)
                remote_ctrl_msg(client_socket, package)
            elif cmd == 4:  # 车窗
                package = struct.pack(">BB", cmd, param)
                remote_ctrl_msg(client_socket, package)
            elif cmd == 5:  # 锁车
                package = struct.pack(">BH", cmd, param)
                remote_ctrl_msg(client_socket, package)
            elif cmd == 6:  # 车钥
                package = struct.pack(">B", cmd)
                remote_ctrl_msg(client_socket, package)
def main():
    # AF_INET：使用标准的IPv4地址或主机名，SOCK_STREAM：说明这是一个TCP服务器
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((bind_ip, bind_port))
    print("[*] Listening on %s:%d" % (bind_ip, bind_port))
    # 最大连接数
    server.listen(5)
    while True:
        #等待客户连接，连接成功后，将socket对象保存到client，将细节数据等保存到addr
        client, addr = server.accept()
        print("[*] Acception connection from %s:%d" % (addr[0],addr[1]))
        client_handler = threading.Thread(target=handle_client,args=(client,))
        client_handler.start()
        input_event = threading.Thread(target=handle_event, args=(client,))
        input_event.start()

if __name__ == '__main__':
    main()
