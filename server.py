#!/usr/bin/python
# -*- coding: UTF-8 -*-

# 导入socket库:
import socket
import time
import threading
import os

streamNum = 1

def LOG_HEX(l):
	for i in l:
		print "%02x" % ord(i),

def byte2bcd(inByte):
	return (((inByte /10) << 4) & 0xF0) | ((inByte % 10) & 0x0F);

def str2bcd(inStr, inStrLen):
	outBcd = []
	tmpStr = inStr
	if inStrLen % 2:
		tmpStr = '0' + tmpStr
	for i in range(0, inStrLen, 2):
		t = tmpStr[i : i+2]
		outBcd.append(byte2bcd(int(t)))
	return outBcd

def jt_send(sock, id, buf, bufLen):
	strPhone = '15618909680'
	lPhone = str2bcd(strPhone, len(strPhone))
	limitSize = 1000
	packCount = (bufLen + limitSize + 1)/limitSize
	packIdx = 1
	packet2 = []
	
	tmpBufLen = 0
	packet2.append(id >> 8)
	packet2.append(id & 0xff)
	
	packet2.append(0)
	packet2.append(0)
	
	for i in range(0, len(lPhone)):
		packet2.append(lPhone[i])
	
	global streamNum
	streamNum %= 0xffff
	packet2.append(streamNum >> 8)
	packet2.append(streamNum & 0xff)
	streamNum += 1

	while packIdx <= packCount:
		if packIdx != packCount:
			sendSize = limitSize
		else:
			sendSize = bufLen - limitSize * (packCount-1)
		
		if packCount > 1:
			tmpBufLen = (1 << 13) | (sendSize & 0x3ff)
		else:
			tmpBufLen = sendSize & 0x3ff
		#modify data len
		packet2[2] = tmpBufLen >> 8
		packet2[3] = tmpBufLen & 0xff
		
		crc = 0
		packet = []
		packet.append(chr(0x7E))
		for i in range(0, len(packet2)):
			if packet2[i] == 0x7E:
				packet.append(chr(0x7D))
				packet.append(chr(0x02))
			elif packet2[i] == 0x7D:
				packet.append(chr(0x7D))
				packet.append(chr(0x01))
			else:
				packet.append(chr(packet2[i]))
			crc = crc ^  packet2[i]
		
		if packCount > 1:
			packet.append(chr(packCount >> 8))
			packet.append(chr(packCount & 0xff))
			packet.append(chr(packIdx >> 8))
			packet.append(chr(packIdx & 0xff))
			crc = crc ^ (packCount >> 8)
			crc = crc ^ (packCount & 0xff)
			crc = crc ^ (packIdx >> 8)
			crc = crc ^ (packIdx & 0xff)
		
		for i in range(0, sendSize):
			tmp = buf[i + (packIdx-1)*sendSize]
			if tmp == chr(0x7E):
				packet.append(chr(0x7D))
				packet.append(chr(0x02))
			elif tmp == chr(0x7D):
				packet.append(chr(0x7D))
				packet.append(chr(0x01))
			else:
				packet.append(tmp)
			crc = crc ^  ord(tmp)
		
		if crc == 0x7E:
			packet.append(chr(0x7D))
			packet.append(chr(0x02))
		elif crc == 0x7D:
			packet.append(chr(0x7D))
			packet.append(chr(0x01))
		else:
			packet.append(chr(crc))
		
		packet.append(chr(0x7E))
		LOG_HEX(packet)
		print('\npackCount=%d,  packIdx=%d, bufLen=%d, sendSize=%d \n\n' % (packCount, packIdx, bufLen, sendSize))
		tmpPacket=''.join(packet)
		sock.send(tmpPacket)
		packIdx += 1
		time.sleep(1)

def tcplink(sock, addr):
	print('Accept new connection from %s:%s...' % addr)
	while True:
		print 'start recv'
		data = sock.recv(1024)
		if not data:
			time.sleep(2)
			continue
		if data == 'update':
			#filePath=r'D:\tools\python_test\DVR.bin'
			filePath=r'D:\tools\python_test\MCU.bin'
			fsize = os.path.getsize(filePath)
			print 'filePath=%s, fsize=%d' % (filePath, fsize)
			fp = open(filePath, "rb")
			buf = fp.read();
			
			updateData = '0' + '12345' + '5' + 'V1002' + '1000'
			updateData += buf
			bufLen = len(updateData)
			jt_send(sock, 0x8108, updateData, bufLen)
			print 'send over.'
			print 'bufLen=%d' % bufLen
			fp.close()
			break
	#time.sleep(1)
	sock.close()
	print('Connection from %s:%s closed.' % addr)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 监听端口:
s.bind(('192.168.20.151', 9999))
s.listen(5)
print('Waiting for connection...')
while True:
    # 接受一个新连接:
    sock, addr = s.accept()
    # 创建新线程来处理TCP连接:
    t = threading.Thread(target=tcplink, args=(sock, addr))
    t.start()







