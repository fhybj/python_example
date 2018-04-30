#!/usr/bin/env python
# -*- coding:utf-8 -*-


'''
Author: Binake
E-Mail: fhybj@outlook.com
File: friends2.py
Time: 2018-04-30 13:24
Desc: Simple CGI script, reference Core Python Programming 20.5
'''
import cgi

header = "Content-Type: text/html\r\n\r\n"

formhtml = """
<html>
    <head>
        <title>Friends CGI Demo (static screen)</title>
    </head>
    <body>
        <h3>Friends list for: <i>NEW USER</i></h3>
        <form action="/cgi-bin/friends2.py">
            <b>Entry your Name:</b>
            <input type="hidden" name="action" value="edit">
            <input type="text" name="person" value="NEW USER" size="15">
            <p>
                %s
            </p>
            <input type="submit">
        </form>
    </body>
</html>
"""

fradio = '<input type="radio" name="howmany" value="%s" %s> %s\n'


def show_form():
    friends = ''
    for i in [0, 10, 25, 50, 100]:
        checked = ""
        if i == 0:
            checked = 'checked'
        friends = friends + fradio % (str(i), checked, str(i))

    print header + formhtml % (friends,)


reshtml = '''
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

def do_result(who, howmany):
    print header + reshtml % (who, who, howmany)

def main():
    form = cgi.FieldStorage()
    if form.has_key('person'):
        who = form['person'].value
    else:
        who = 'NEW USER'

    if form.has_key('howmany'):
        howmany = form['howmany'].value
    else:
        howmany = 0

    if form.has_key('action'):
        do_result(who, howmany)
    else:
        show_form()


if __name__ == '__main__':
    main()
