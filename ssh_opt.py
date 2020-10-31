#!/usr/bin/python
# -*- coding: UTF-8 -*-

import paramiko

class ssh_client():

    def __init__(self, host=None,port=22, username=None, password=None, pkey_path=None, timeout=10):
        self.client = paramiko.SSHClient()
        """
        使用xshell登录机器，对于第一次登录的机器会提示允许将陌生主机加入host_allow列表
        需要connect 前调用，否则可能有异常。
        """
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        if password != None:
            self.client.connect(hostname=host, port=port, username=username, password=password, timeout=timeout)
        elif  pkey_path != None:
            """使用秘钥登录"""
            self.pkey = paramiko.RSAKey.from_private_key_file(pkey_path)
            self.client.connect(hostname=host,port=port,pkey=self.pkey, timeout=timeout)

        self.sftp = self.client.open_sftp()


    def run_cmd(self, cmd):
        _in, _out, _error = self.client.exec_command(cmd)
        return _out.read(),_error.read()

    def put_file(self, local, remote):
        return self.sftp.put(localpath=local, remotepath=remote)

    def get_file(self, local, remote):
        return self.sftp.get(localpath=local, remotepath=remote)

    def __del__(self):
        self.client.close()
        self.sftp.close()


if __name__ == "__main__":
    print("------ paramiko ssh client test -------")
    ## 密码登录
    client = ssh_client(host='47.111.129.182', username='root', password='Hopechart!110')
    ## 秘钥登录
    #client = ssh_client(host='192.168.37.134', username='lcd',pkey_path="/home/lcd/.ssh/id_rsa")

    out, err = client.run_cmd('ss -ant')
    type(out)
    print('out=', out.strip('\n'))
    #print('err=', err)
    if len(err) != 0:
        print("cmd exec error")

    out, err = client.run_cmd('pwd; cd /home/')
    print("cO : %s"%out.strip('\n'))
    print("cE : %s"%err.strip('\n'))
    if len(err) != 0:
        print("cmd exec error")

    print(client.get_file(local="./aa", remote="/root/wujian/test/tcpdump"))
    #print client.put_file(local="./aa", remote="/home/lcd/bb")