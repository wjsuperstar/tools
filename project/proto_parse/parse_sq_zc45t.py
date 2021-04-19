# -*- coding: UTF-8 -*-
# auth: WuJian  20201029
# desc: 陕汽展车项目解析
import time
import datetime
import struct
import parse_gb32960
from gmssl import sm2, sm3, func
from gmssl.sm4 import CryptSM4, SM4_ENCRYPT, SM4_DECRYPT

bind_ip = "0.0.0.0"  #监听所有可用的接口
bind_port = 40228   #非特权端口号都可以使用
pack_prop_plaintext_ = 0
pack_prop_sm4_ = 1
sign_k_val_ = '123456'
sta_private_key_ = 'F55B3E38750F4993DC35FE295925AB82E168F42AC50C1DA5C571A87697160B4B'
sta_public_key_ = '8B5802223A98E1891923A103EE4FE08DE39F62D18C8DF9EB4B7F5153E9CD23B081E57D7BD954FDFFDD88AEBC04041F0228CE9E350F735F82ECB0E7013BD597AB'
pla_private_key_ = '98E39D034EACD72AE56433D42488CF849E0F1FFFAE72EA8789BA8644A375B3B7'
pla_public_key_ = '73F1CAA35C035E93F76539756854EE0D183970C6ADA8058A5DE7DF43674816ACD0F0C1E11AEA2888BF32404272B3BBFB3A9A853252FCF70A0B1F3F6803E55117'
sm4_key_ = b'3l5butlj26hvv313'
msg_serial_num_ = 0
vehicle_vin_ = b'TEST1234567890123'
ENTL="0080"
ID="31323334353637383132333435363738"
# a, b, x_G, y_G 都是SM2算法标准中给定的值。a和b是椭圆曲线y=x+ax+b的系数，x_G, y_G是SM2算法选定的基点的坐标
a="FFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFC"
b="28E9FA9E9D9F5E344D5A9E4BCF6509A7F39789F515AB8F92DDBCBD414D940E93"
x_G="32C4AE2C1F1981195F9904466A39C9948FE30BBFF2660BE1715A4589334C74C7"
y_G="BC3736A2F4F6779C59BDCEE36B692153D0A9877CC62A474002DF32E52139F0A0"
# Z = h(ENTL || ID || a || b || xG || yG || xA || yA)
# Z = sm3.sm3_hash(func.bytes_to_list(bytes.fromhex((ENTL+ID+a+b+x_G+y_G+sta_public_key_))))

def encode_std_npv(cmd, ack_flg, vin, encrypt, data):
    head_id = 0x2323
    data_len = len(data)
    if cmd == 0xFA:
        package = struct.pack(">HBB17sBHH%ds" % data_len, head_id, cmd, ack_flg, vin, encrypt, data_len+2, data_len, data)
    else:
        package = struct.pack(">HBB17sBH%ds" % data_len, head_id, cmd, ack_flg, vin, encrypt, data_len, data)
    crc = '%02x' % parse_gb32960.CalcCrc(package[2:])
    package += bytes.fromhex(crc)
    return package

def encode_sq_lay1(encrpt, data, pack_time):
    head_id = 0x5351
    pack_prop = (encrpt & 0x0f)
    data_len = len(data)
    package = struct.pack(">HHH%dsII" % data_len, head_id, pack_prop, data_len, data, 0, pack_time)
    sm2_crypt = sm2.CryptSM2(public_key=None, private_key=pla_private_key_)
    #Z = sm3.sm3_hash(func.bytes_to_list(bytes.fromhex((ENTL + ID + a + b + x_G + y_G + pla_public_key_))))
    #e = sm3.sm3_hash(func.bytes_to_list(bytes.fromhex(Z)+package))
    #sign = sm2_crypt.sign(bytes.fromhex(Z)+package, sign_k_val_) # 对e值进行签名
    sign = sm2_crypt.sign(package, sign_k_val_)
    #print('sign:', sign)
    package += bytes.fromhex(sign)
    return package

def encode_sq_lay2(msg_id, encrpt, data):
    global msg_serial_num_
    msg_prop = 0x20
    data_len = len(data)
    #print(f'---L2--->data_len={data_len}')
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
    #print('sm4_key:', sm4_key.hex())
    data_len = len(sm4_key)
    key_type = 1
    unix_tm = int(time.time())
    package = struct.pack(">BH%dsII" % data_len, key_type, data_len, sm4_key, 0, unix_tm)
    l2 = encode_sq_lay2(0xff00, pack_prop_plaintext_, package)
    l1 = encode_sq_lay1(pack_prop_plaintext_, l2, unix_tm)
    return encode_std_npv(0xFA, 0xFE, vin, 1, l1)

def remote_ctrl_msg(client_socket, data):
    unix_tm = int(time.time())
    l2 = encode_sq_lay2(0xfb00, pack_prop_sm4_, data)
    l1 = encode_sq_lay1(pack_prop_sm4_, l2, unix_tm)
    msg = encode_std_npv(0xFA, 0xFE, vehicle_vin_, 1, l1)
    client_socket.send(msg)

class Parse45tCustomMsg:
    def __init__(self):
        self.__crypt_sm4 = CryptSM4()
        self.__crypt_sm4.set_key(sm4_key_, SM4_DECRYPT)
        self.__crypt_sm2 = sm2.CryptSM2(public_key=sta_public_key_, private_key=None)
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
        encrypt_data, tmp, unix_tm, sign_data = struct.unpack(">%dsII64s" % data_len, data[idx:idx+data_len+64+8])
        self.package.update({"封包时间": time.strftime("%Y-%m-%d %H:%M:%S",  time.localtime(unix_tm))})
        z = sm3.sm3_hash(func.bytes_to_list(bytes.fromhex((ENTL + ID + a + b + x_G + y_G + sta_public_key_))))
        e = sm3.sm3_hash(func.bytes_to_list(bytes.fromhex(z)+data[0:idx+data_len+8]))
        self.__verify = self.__crypt_sm2.verify(sign_data.hex(), bytes.fromhex(e))
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
        data = data[2:]   #跳过透传数据长度
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


if __name__ == '__main__':
    pass
