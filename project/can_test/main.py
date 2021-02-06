
import can

def send_one():
    bus = can.interface.Bus(bustype='canalystii', channel=0, baud=500000)

    msg = can.Message(arbitration_id=0xc0ffee,
                      data=[0, 25, 0, 1, 3, 1, 4, 1],
                      is_extended_id=True)

    try:
        bus.send(msg)
        print("Message sent on {}".format(bus.channel_info))
    except can.CanError:
        print("Message NOT sent")

if __name__ == '__main__':
    for _ in range(100):
        send_one()