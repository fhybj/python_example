#!/usr/bin/env python
# -*- coding:utf-8 -*-


'''
Author: Binake
E-Mail: fhybj@outlook.com
File: name_client.py
Time: 2018-04-17 22:05
Desc: 名称服务器的客户端，通过名称从名称服务器获取功能服务器的信息
'''

import socket

HOST = "localhost"
PORT = 9898
ADDR = (HOST, PORT)
BUFSIZE = 1024


def main():
    client = socket.socket()
    client.connect(ADDR)

    while True:
        service = raw_input('<service> ')
        client.send("get:%s" % service)
        service = client.recv(BUFSIZE)
        if service != 'error':
            sub_service = socket.socket()
            ip, port = service.split(':')
            sub_service.connect((ip, int(port)))
            while True:
                data = raw_input('> ')
                if data == 'exit':
                    break
                sub_service.send(data)
                data = sub_service.recv(BUFSIZE)
                print data
            sub_service.close()
        else:
            print "Invalid service name"

if __name__ == '__main__':
    main()