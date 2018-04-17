#!/usr/bin/env python
# -*- coding:utf-8 -*-


'''
Author: Bianke
E-Mail: fhybj@outlook.com
File: tcp_client_get_http.py
Time: 2018-04-17(星期二) 10:14
Desc: 基于TCP的网页客户端，连接到网站的80端口，获取数据之后将数据保存到文件.
'''

import socket
import sys

HOST = "www.mooc.cn"
PORT = 80
ADDR = (HOST, PORT)
BUFSIZE = 4096

http_socket = socket.socket()
try:
    http_socket.connect(ADDR)
    http_socket.settimeout(1) # 将socket设置为non-blocking
except:
    print "Unable to connect."
    sys.exit()

try:
    http_socket.send("GET / HTTP/1.1\r\n")
    http_socket.send("Host: www.mooc.cn\r\n")
    http_socket.send("Connection: keep-alive\r\n")  # Connection属性设置为keep-alive，意为保持连接，和socket.settimeout配合
    http_socket.send("Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8\r\n")
    http_socket.send("Upgrade-Insecure-Requests: 1\r\n")
    http_socket.send("User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36\r\n")
    http_socket.send("Accept-Encoding: deflate, br\r\n")
    http_socket.send("Accept-Language: zh-CN,zh;q=0.9\r\n\r\n")
except socket.error, e:
    http_socket.close()

content = []
try:
    while True:
        data = http_socket.recv(BUFSIZE) # 因为socket是non-blocking的，而和服务器的连接是keep-alive的，所以当timeout且没有数据被接受到的时候，会raise Error
        content.append(data)
except:
    print "receiver all data"
finally:
    http_socket.close()

print '--------------------'
data = ''.join(content)

header, html = data.split('\r\n\r\n', 1) 
with open('F:/mooc.html', 'w+') as fd:
    fd.write(html)