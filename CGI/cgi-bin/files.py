#!/usr/bin/env python
# -*- coding:utf-8 -*-


'''
Author: Binake
E-Mail: fhybj@outlook.com
File: files.py
Time: 2018-05-08 20:55
Desc: Core Python Programming Chapter 20,  20-16
'''
#import cgi
import cgitb;cgitb.enable()
import zipfile
import os

import mycgi

header = "Content-Type: text/html\r\n\r\n"

formhtml = """
<!DOCTYPE html>
<html>
    <head>
        <title>上传文件</title>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    </head>
    <body>
        <form method="post" action="/cgi-bin/files.py" enctype="multipart/form-data">
        <b>选择您要上传的文件：</b>
        <p>
        <input type="file" name="upfile">
        <p>
        <input type="submit">
        </form>
    </body>
</html>
"""

def show_form():
    print header + formhtml

upfilehtml = """
<!DOCTYPE html>
<html>
    <head>
        <title>上传成功</title>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    </head>
    <body>
        上传文件成功！
    </body>
</html>
"""

def do_upfile(upfile):
    if upfile == '404':
        print header + "404 No Found"
    else:
        filename = upfile.filename
        fp = upfile.file
        with open(filename, 'wb+') as wfp:
            for line in fp:
                wfp.write(line)
        fp.close()

        if zipfile.is_zipfile(filename):
            zfile = zipfile.ZipFile(filename)
            extract_dir = os.path.splitext(filename)[0]
            zfile.extractall(extract_dir)
            zfile.close()

        print header + upfilehtml


def main():
    form = mycgi.MyFieldStorage()

    if form.has_key('upfile'):
        upfile = form.get('upfile', '404')
        do_upfile(upfile)
    else:
        show_form()

if __name__ == '__main__':
    main()