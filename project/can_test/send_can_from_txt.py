import drv_can
import time

dc = drv_can.ZlgCanDev()

for i in range(100):
    data = [1, 4, 7, 2, 5, 8, 3, 6]
    dc.write(0x1234, data)
    time.sleep(0.001)

for i in range(1000):
    ret, id, data = dc.read()
    if ret > 0:
        print("ID=", id, "len=", len(data), "data=", data)
    time.sleep(0.01)