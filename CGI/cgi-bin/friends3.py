#!/usr/bin/env python
# -*- coding:utf-8 -*-


'''
Author: Binake
E-Mail: fhybj@outlook.com
File: friends3.py
Time: 2018-04-30 13:42
Desc: Simple CGI script, reference Core Python Programming 20.6
'''

import cgi
from urllib import quote_plus

header = "Content-Type: text/html\r\n\r\n"
url = "/cgi-bin/friends3.py"

errhtml = """
<html>
    <head>
        <title>Friend CGI Demo</title>
    </head>
    <body>
        <h3>Error</h3>
        <b>%s</b><p>
        <form>
            <input type="button" value="Back" onclick="window.history.back()">
        </form>
    </body>
</html>
"""

def show_error(error_str):
    print header + errhtml % (error_str,)

formhtml = """
<html>
    <head>
        <title>Friends CGI Demo (static screen)</title>
    </head>
    <body>
        <h3>Friends list for: <i>%s</i></h3>
        <form action="%s">
            <b>Entry your Name:</b>
            <input type="hidden" name="action" value="edit">
            <input type="text" name="person" value="%s" size="15">
            <p>
                %s
            </p>
            <input type="submit">
        </form>
    </body>
</html>
"""

fradio = '<input type="radio" name="howmany" value="%s" %s> %s\n'

def show_form(who, howmany):
    friends = ""
    for i in [0, 10, 25, 50, 100]:
        checked = ""
        if str(i) == howmany:
            checked = "checked"
        friends = friends + fradio % (str(i), checked, str(i))
    print header + formhtml % (who, url, who, friends)


reshtml = '''
<html>
    <head>
        <title>Friends CGI Demo (dynamic screen)</title>
    </head>
    <body>
        <h3>Friends list for: <i>%s</i></h3>
        Your name is: <b>%s</b><p>
        You have <b>%s</b> friends.
        <p>
        Click <a href="%s">here</a> to edit your data again.
    </body>
</html>
'''

def do_result(who, howmany):
    new_url = url + "?action=reedit&person=%s&howmany=%s" % \
        (quote_plus(who), howmany)

    print header + reshtml % (who, who, howmany, new_url)


def main():
    error = ""
    form = cgi.FieldStorage()

    if form.has_key('person'):
        who = form['person'].value.title()
    else:
        who = "New User"

    if form.has_key('howmany'):
        howmany = form['howmany'].value
    else:
        if form.has_key('action') and form['action'].value == 'edit':
            error = "Please select number of friends"
        else:
            howmany = 0

    if not error:
        if form.has_key('action') and form['action'].value != 'reedit':
            do_result(who, howmany)
        else:
            show_form(who, howmany)
    else:
        show_error(error)

if __name__ == '__main__':
    main()
