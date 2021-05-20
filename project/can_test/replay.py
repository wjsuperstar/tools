import re,time,datetime,binascii
import can
import datetime
from can import Message
bus = can.interface.Bus(bustype='canalystii', device=0,channel=0, bitrate=250000)
REGEX = re.compile(r'\d+\t\t接收\s+([0-9:\.]+)\s+0x([0-9a-f]+)\s+数据帧\s+扩展帧\s+0x08 +([ 0-9a-f]+)')
with open('zq123.txt','r') as fin:
    beg_ts = None
    for idx,line in enumerate(fin):
        if idx ==0:
            continue
        line = line.strip()
        m = REGEX.match(line)
        if m:
            ts,frame_id,data = m.groups()
            frame_id = int(frame_id, 16)
            ts = ts[:-2]#.replace('.0','')
            ts = datetime.datetime.strptime(ts,'%H:%M:%S.%f')
            real_data = binascii.a2b_hex(data.replace(' ',''))
            buffer = can.Message(arbitration_id=frame_id, data=real_data, is_extended_id=True)
            if beg_ts is None:
                beg_ts = ts
                real_begin_ts = time.time()
            else:
                if time.time() - real_begin_ts <= (ts - beg_ts).total_seconds():
                    time.sleep(0.001)
            bus.send(buffer)
            print(f"{time.time()} {frame_id:x} {data}")
        