#!/usr/bin/env python
# -*- coding:utf-8 -*-


'''
Author: Binake
E-Mail: fhybj@outlook.com
File: name_sub_service.py
Time: 2018-04-17 21:06
Desc: 名称服务器的子服务器，提供具体的功能
'''

import socket
import sys
import select

def main(argv):
    print argv
    if len(argv) != 4:
        print "argument error"
        sys.exit()

    name = argv[1]
    ip, port = argv[2:]
    service_socket = socket.socket()
    service_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    service_socket.bind((ip, int(port)))
    service_socket.listen(5)

    client_socket = socket.socket()
    client_socket.connect(('localhost', 9898))
    cmd = "regist:%s:%s:%s" % (name, ip, port)
    client_socket.send(cmd)

    current_list = [service_socket]

    while True:
        rlist, wlist, xlist = select.select(current_list, [], [])
        for sock in rlist:
            if sock is service_socket:
                client, addr = service_socket.accept()
                current_list.append(client)
                print "Client (%s:%s) connected." % client.getpeername()
            else:
                data = sock.recv(1024)
                if not data:
                    sock.close()
                    current_list.remove(sock)
                    break
                response = "<%s> %s" % (name, data)
                sock.send(response)



if __name__ == '__main__':
    main(sys.argv)
