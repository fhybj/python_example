#!/usr/bin/env python
# -*- coding:utf-8 -*-


'''
Author: Binake
E-Mail: fhybj@outlook.com
File: advcgi.py
Time: 2018-04-30 15:25
Desc: Advance CGI Script, reference Core Python Programming 20.8
'''


from cgi import FieldStorage
from os import environ
from urllib import unquote, quote
from cStringIO import StringIO


class AdvCGI(object):

    header = "Context-Type: text/html\r\n\r\n"
    url = "/cgi-bin/advcgi.py"

    formhtml = """
    <html>
        <head>
            <title>Advanced CGI Demo</title>
        </head>
        <body>
            <h2>Advanced CGI Demo Form</h2>
            <form method="post" action="%s" enctype="multipart/form-data">
            <h3>My Cookie Setting</h3>
            <li> <code><b>CPPuser = %s </b></code>
            <h3>Enter cookie value<br>
            <input name="cookie" value="%s"> (<i>optional</i>)</h3>
            <h3>Enter your name<br>
            <input name="person" value="%s"> (<i>required</i>)</h3>
            <h3>What languages can you program in? (<i>at least on required</i>)</h3>
            %s
            <h3>Enter file to upload</h3>
            <input type="file" name="upfile" value="%s" class="filetext" size=45>
            <p>
            <input type="submit">
            </form>
        </body>
    </html>
    """

    lang_set = ('Python', 'Perl', 'Java', 'C++', 'PHP', 'C', 'JavaScript')
    lang_item = '<input type="checkbox" name="lang" value="%s" %s> %s\n'

    def getCPPCookies(self):
        """
        Read cookie from client
        """
        if environ.has_key('HTTP_COOKIE'):
            print environ['HTTP_COOKIE']
            for eachCookie in map(str.strip, environ['HTTP_COOKIE'].split(';')):
                if len(eachCookie) > 6 and eachCookie[:3] == 'CPP':
                    tag = eachCookie[3:7]
                    try:
                        self.cookies[tag] = eval(unquote(eachCookie[8:]))
                    except (NameError, SyntaxError):
                        self.cookies[tag] = unquote(eachCookie[8:])
        else:
            print "set default cookies value"
            self.cookies['info'] = self.cookies['user'] = ''

        if self.cookies.has_key('info') and self.cookies['info'] != '':
            self.who, self.lang_str, self.fn = self.cookies['info'].split(':')
            self.langs = self.lang_str.split(',')
        else:
            self.who = self.fn = ""
            self.langs = ['Python']

    def show_form(self):
        self.getCPPCookies()
        lang_str = ""
        for eachLang in AdvCGI.lang_set:
            if eachLang in self.langs:
                lang_str += AdvCGI.lang_item % (eachLang, "checked", eachLang)
            else:
                lang_str += AdvCGI.lang_item % (eachLang, "", eachLang)

        if not self.cookies.has_key('user') or self.cookies['user'] == "":
            cookie_status = '<i>(Cookie has not been set yet)</i>'
            user_cookie = ""
        else:
            user_cookie = cookie_status = self.cookies['user']

        print AdvCGI.header + AdvCGI.formhtml % \
        (AdvCGI.url, cookie_status, user_cookie, self.who, lang_str, self.fn)


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

    def show_error(self):
        print AdvCGI.header + AdvCGI.errhtml % (self.error,)


    reshtml = '''
    <html>
        <head>
            <title>Advanced CGI Demo (dynamic screen)</title>
        </head>
        <body>
            <h2>Your Uploaded Data</h2>
            <h3>Your cookie value is: <b>%s</b></h3>
            <h3>Your name is : <b>%s</b></h3>
            <h3>You can program in the following languages:</h3>
            <ul>%s</ul>
            <h3>Your uploaded file...<br>
            Name: <i>%s</i><br>
            Contents:</h3>
            <pre>%s</pre>
            Click <a href="%s">here</a> to return to form.
        </body>
    </html>
    '''

    def setCPPCookies(self):
        for eachCookie in self.cookies.keys():
            print 'Set-Cookie: CPP%s=%s; path=/' % (eachCookie, quote(self.cookies[eachCookie]))

    def do_results(self):
        MAXBYTES = 1024
        lang_list = ""

        for eachLang in self.langs:
            lang_list += '<li>%s<br>' % eachLang

        file_data = ""
        while len(file_data) < MAXBYTES:
            data = self.fp.readline()
            if data == "":
                break
            file_data += data
        else:
            file_data += "... <b><i>(file truncated due to size)<i><b>"
        self.fp.close()

        if file_data == "":
            file_data = "<b><i>(file upload error or file not given)</i></b>"
        file_name = self.fn

        if not self.cookies.has_key('user') or self.cookies['user'] == "":
            cookie_status = "<i>(cookie has not been set yet)</i>"
            user_cookie = ""
        else:
            user_cookie = cookie_status = self.cookies['user']

        self.cookies['info'] = ":".join([self.who, ",".join(self.langs), file_name])
        self.setCPPCookies()
        print AdvCGI.header + AdvCGI.reshtml % \
        (cookie_status, self.who, lang_list, file_name, file_data, AdvCGI.url)

    def go(self):
        """
        Dynamic generate the HTML page
        """
        self.cookies = {}
        self.error = ""
        form = FieldStorage()

        if not form.keys():
            self.show_form()
            return

        if form.has_key('person'):
            self.who = form['person'].value.strip().title()
            if self.who == "":
                self.error = "Your name is required. (blank)"
        else:
            self.error = "Your name is required. (missing)"

        if form.has_key('cookie'):
            self.cookies['user'] = unquote(form['cookie'].value.strip())
        else:
            self.cookies['user'] = ""

        self.langs = []
        if form.has_key('lang'):
            lang_data = form['lang']

            if isinstance(lang_data, list):
                for eachLang in lang_data:
                    self.langs.append(eachLang.value)
            else:
                self.langs.append(lang_data)
        else:
            self.error = 'At least one language required.'

        if form.has_key('upfile'):
            upfile = form['upfile']
            self.fn = upfile.filename or ""
            if upfile.file:
                self.fp = upfile.file
            else:
                self.fp = StringIO('(no data)')
        else:
            self.fp = StringIO('(no file)')
            self.fn = ""

        if not self.error:
            self.do_results()
        else:
            self.show_error()

        

if __name__ == '__main__':
    page = AdvCGI()
    page.go()
