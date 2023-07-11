from time import sleep
import serial_bus
import threading
import json
import logging





class TDvrTest:
    def __init__(self):
        self.uart_handle = serial_bus.SerialBus(None, None)
        self.tx_thread = None
        self.rx_thread = None
        self.AtCmdList = None
        self.stop_event = threading.Event()

    def load_cfg(self):
        with open("dvr_test_cfg.json", encoding='utf-8') as fd:
            js = json.load(fd)
            self.AtCmdList = js["atCmdList"]

    def start(self):
        port = serial_bus.find_at_com()
        self.uart_handle.start(port, 115200, 8, 1, 'N')
        self.tx_thread = threading.Thread(target=self._send)
        self.rx_thread = threading.Thread(target=self._recv)
        self.stop_event.clear()
        self.tx_thread.start()
        #self.rx_thread.start()
    def end(self):
        self.uart_handle.join()

    def _send(self):
        logging.info('tx thread is started')
        while not self.stop_event.is_set():
            for pair in self.AtCmdList :
                if pair["enable"] == 0:
                    continue
                if pair["mode"] == 0:
                    cmd =

    def _recv(self):
        logging.info('at rx thread is started')
        while not self.stop_event.is_set():
            try:
                data = self.uart_handle.read(0.2)
                if data and len(data) > 0:
                    deal_at_cmd(data)
            except IOError as e:
                logging.warning(e)
                uart_handle.join()
                self.stop_event.set()
        logging.info('at rx thread exits')

    def exec_at_test(self):
        pass

    def deal_at_cmd(self,data):
        if data.startswith("")

def main():
    test = TDvrTest()

if __name__ == '__main__':
    main()
