#!/usr/bin/env python
# -*- coding:utf-8 -*-


'''
Author: Binake
E-Mail: fhybj@outlook.com
File: comment.py
Time: 2018-05-08 20:22
Desc: Core Python Programming Chapter 20,  20-11
'''
import cgi
import cgitb;cgitb.enable()


header = "Content-Type: text/html\r\n\r\n"

formhtml = """
<!DOCTYPE html>
<html>
    <head>
        <title>评论</title>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    </head>
    <body>
        <form action="/cgi-bin/comment.py">
        <b>写下您的评论：</b>
        <p>
        <textarea name="comment" cols="50" rows="10"></textarea>
        <p>
        <input type="submit">
        </form>
    </body>
</html>
"""

def show_form():
    print header + formhtml


thankshtml = """
<!DOCTYPE html>
<html>
    <head>
        <title>感谢您的评论</title>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    </head>
    <body>
        感谢您的评论！
    </body>
</html>
"""

def show_thankes():
    print header + thankshtml;

def main():
    form = cgi.FieldStorage()

    if form.has_key('comment'):
        show_thankes()
    else:
        show_form()

if __name__ == '__main__':
    main()