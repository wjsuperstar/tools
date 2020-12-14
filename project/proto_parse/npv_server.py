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
vehicle_vin_ = b'TEST1234567890123'
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

class Parse45tCustomMsg:
    def __init__(self):
        self.__crypt_sm4 = CryptSM4()
        self.__crypt_sm4.set_key(sm4_key_, SM4_DECRYPT)
        self.__crypt_sm2 = sm2.CryptSM2(public_key=pla_public_key_, private_key=None)
        self.__verify = False
        self.__msg_id = 0
        self.package = dict()

    def decode_sq_lay1(self, data):
        idx = 0
        head_id, pack_prop, data_len = struct.unpack(">HHH", data[idx:idx+6])
        self.package.update({"封包标识": hex(head_id)})
        self.package.update({"封包属性": pack_prop})
        self.package.update({"封包长度": data_len})
        idx += 6
        encrypt_data, unix_tm, sign_data = struct.unpack(">%dsI64s" % data_len, data[idx:idx+data_len+68])
        self.package.update({"封包时间": time.strftime("%Y-%m-%d %H:%M:%S",  time.localtime(unix_tm))})
        self.__verify = self.__crypt_sm2.verify(sign_data.hex(), data[0:idx+data_len+4])

        self.package.update({"验签结果": self.__verify})
        if (pack_prop & 0x0f) == pack_prop_sm4_:
            encrypt_data = self.__crypt_sm4.crypt_ecb(encrypt_data)
        return encrypt_data

    def decode_sq_lay2(self, data):
        idx = 0
        msg_prop, msg_id, msg_no, msg_len = struct.unpack(">HHHH", data[idx:idx+8])
        self.__msg_id = msg_id
        self.package.update({"消息属性": msg_prop})
        self.package.update({"消息ID": hex(msg_id)})
        self.package.update({"消息序号": msg_no})
        self.package.update({"消息长度": msg_len})
        idx += 8
        msg_data, crc = struct.unpack(">%dsB" % msg_len, data[idx:idx+msg_len+1])
        calc_crc = parse_gb32960.CalcCrc(data[0:idx+msg_len])
        if calc_crc == crc:
            return msg_data
        else:
            return None

    def decode_key_exchange_ack(self, data):
        req_no, result = struct.unpack(">HB", data)
        self.package.update({"请求序号": req_no})
        self.package.update({"密钥交换结果": result})
    def decode_ctrl_exec_status(self, data):
        desc = ('指令序号', '指令状态', '执行进度')
        values = struct.unpack(">HBB", data)
        self.package.update({"控制指令执行状态": dict(zip(desc, values))})
    def decode_ctrl_exec_result(self, data):
        desc = ('指令序号', '执行结果', '失败原因', '附加结果类型', '附加结果长度')
        values = struct.unpack(">H3BH", data)
        res = dict(zip(desc, values))
        if values[4] > 0:
            res.update({"附件结果" : data[7:]})
        self.package.update({"控制指令执行结果": res})

    def parse(self, data):
        data = self.decode_sq_lay2(self.decode_sq_lay1(data))
        if data is None:
            return None
        msg_id = self.__msg_id
        if msg_id == 0xff01:
            self.decode_key_exchange_ack(data)
        elif msg_id == 0xfb01:
            self.decode_ctrl_exec_status(data)
        elif msg_id == 0xfb02:
            self.decode_ctrl_exec_result(data)
        else:
            print('暂不支持解析的消息ID：', msg_id, data)
        return self.package

class Sq45tParseMsg(parse_gb32960.MainParseMsg):
    def __init__(self):
        super().__init__()
        #self.__data = data
    def parse_custom_msg(self, cmd, data):
        if cmd == 0xFB:
            obj = Parse45tCustomMsg()
            result = obj.parse(data)
            print(result)

def deal_recv_data(client_socket, data):
    obj = Sq45tParseMsg()
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
            global logon_flg_
            logon_flg_ = True
        elif cmd == 0x04:
            pass
        elif cmd == 0x07:
            d_arry = bytearray(data)
            d_arry[3] = 1
            d_arry[-1] = parse_gb32960.CalcCrc(d_arry[2:-1])
            client_socket.send(bytes(d_arry))

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
        if len(request) > 24:
            print("[*] Received: %s" % request.hex())
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
