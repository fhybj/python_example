#!/usr/bin/env python
# -*- coding:utf-8 -*-


'''
Author: Binake
E-Mail: fhybj@outlook.com
File: name_service.py
Time: 2018-04-17 20:46
Desc: 名称服务器，维护已经注册的功能服务器的信息，并根据服务名称返回服务器信息给客户端
'''

import socket
import select

HOST = "localhost"
PORT = 9898
ADDR = (HOST, PORT)
BUFSIZE = 1024


service_socket = socket.socket()
service_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
service_socket.bind(ADDR)
service_socket.listen(5)

current_list = [service_socket]
name_map = dict()

def main():
    while True:
        rlist, wlist, xlist = select.select(current_list, [], [])
        for sock in rlist:
            if sock is service_socket:
                client, addr = service_socket.accept()
                current_list.append(client)
                print "Client (%s:%s) connected." % addr
            else:
                try:
                    cmd = sock.recv(BUFSIZE)
                    if cmd:
                        cmd, data = cmd.split(':', 1)
                        if cmd == 'regist':
                            name, ip, port = data.split(':')
                            name_map[name] = (ip, port)
                        elif cmd == 'get':
                            if data in name_map:
                                response = ":".join(name_map[data])
                            else:
                                response = "error"
                            sock.send(response)
                except socket.error:
                    sock.close()
                    current_list.remove(sock)

if __name__ == '__main__':
    main()