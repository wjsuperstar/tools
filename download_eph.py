import time
from ftplib import FTP
import logging
from tcping import Ping

remote_file = 'eph.dat'
local_file = 'eph.dat'

def test_net():
    try:
        logging.error('test net: www.baidu.com:80')
        ping = Ping('www.baidu.com', 80, 500)  # 地址、端口、超时时间
        ping.ping(3)                           # ping命令执行次数
        ret = ping.result.table                # 以表格形式展现（ping.result.raw  # 原始形态，ping.result.rows  # 行显示）
        logging.error(ret)

        logging.error('test net: 18.177.237.209:21')
        ping = Ping('18.177.237.209', 21, 500)
        ping.ping(3)
        ret = ping.result.table  
        logging.error(ret)
    except Exception as e:
        logging.error(e)

def ftp_connect():
    """用于FTP连接"""
    #ftp_server = 'agnss.queclocator.com'
    ftp_server = '18.177.237.209'
    username = 'L76K_LF'  # 用户名
    password = '8d1H5k4t'  # 密码
    ftp = FTP()
    try:
        #ftp.set_debuglevel(0)  # 较高的级别方便排查问题
        ftp.connect(ftp_server, 21, 2)
        ftp.login(username, password)
    except Exception as e:
        logging.error('ftp connect error:')
        logging.error(e)
        test_net()
        ftp = None
    return ftp

def download_file():
    """用于目标文件下载"""
    ftp = ftp_connect()
    if ftp:
        bufsize = 1024*8
        fp = open(local_file, 'wb')
        ftp.set_debuglevel(1)  # 较高的级别方便排查问题
        ftp.retrbinary('RETR ' + remote_file, fp.write, bufsize)
        fp.close()
        ftp.quit()
        logging.info('download eph.dat success!')
    else:
        logging.error('download eph.dat fail!')

if __name__ == "__main__":
    logging.basicConfig(filename='test_ftp_dn.log', format='%(asctime)s %(message)s', level=logging.DEBUG)
    last_time = 0
    while True:
        now = time.time()
        if now - last_time >= 60:
            download_file()
            last_time = now
            #print('last_time=', last_time)
