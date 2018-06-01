#!/usr/bin/env python
# -*- coding:utf-8 -*-


'''
Author: Binake
E-Mail: fhybj@outlook.com
File: mycgi.py
Time: 2018-05-08 22:43
Desc: 
'''
from cgi import FieldStorage


class MyFieldStorage(FieldStorage):

    def get(self, key, default):
        if self.has_key(key):
            value = self[key]
        else:
            value = default

        return value
