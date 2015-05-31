#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

# Author: Kin Lo <kinabcd@gmail.com>
from xml.sax.saxutils import escape
class XMLRPC:
    def __init__(self, methodName):
        self.params = []
        self.methodName = methodName

    def addParam(self, param):
        self.params.append(param)

    def __str__(self):
        s = '<?xml version="1.0"?>' \
            '<methodCall>' \
            '<methodName>' + self.methodName + '</methodName>'
        if len(self.params) > 0 :
            s += '<params>'
            for param in self.params:
                s += '<param><value>'
                if isinstance(param,str):s += '<string>' + escape(param) + '</string>'
                elif isinstance(param,int):s += '<i4>' + str(param) + '</i4>'
                elif isinstance(param,float):s += '<double>' + str(param) + '</double>'
                s += '</value></param>'
            s += '</params>'
        s +='</methodCall>'
        return s
