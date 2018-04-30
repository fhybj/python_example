#!/usr/bin/env python
# -*- coding:utf-8 -*-


'''
Author: Binake
E-Mail: fhybj@outlook.com
File: friends1.py
Time: 2018-04-29 16:55
Desc: Simple CGI script, reference Core Python Programming 20.4
'''

import cgi

reshtml = '''Content-Type: text/html\r\n\r\n
<html>
    <head>
        <title>Friends CGI Demo (dynamic screen)</title>
    </head>
    <body>
        <h3>Friends list for: <i>%s</i></h3>
        Your name is: <b>%s</b><p>
        You have <b>%s</b> friends.
    </body>
</html>
'''

form = cgi.FieldStorage()
who = form['person'].value
howmany = form['howmany'].value
print reshtml % (who, who, howmany)
