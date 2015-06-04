#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

# Author: Kin Lo <kinabcd@gmail.com>
from xml.sax.saxutils import escape
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

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

def parse(root):
    if isinstance(root,str):
        root = ET.fromstring(root)
    if root.tag in ['value']:
        for ch in root:
            return parse(ch)
    if root.tag in ['methodResponse']:
        for ch in root:
            if ch.tag == 'fault':
                r = parse(ch)
                r['result'] = 'fault'
                return r
            elif ch.tag == 'params':
                return {'result':'success', 'data':parse(ch)}
            else :
                raise ValueError('Not "fault" nor "params"')
    if root.tag in ['array']:
        r = []
        for data in root:
            if data.tag == 'data':
                for value in data:
                    r.append( parse(value))
            else :
                r.append( parse(c))
        return r
    elif root.tag in ['struct']:
        r = {}
        for m in root:
            if m.tag == 'member':
                for d in m:
                    if d.tag == 'name':
                        name = d.text
                    if d.tag == 'value':
                        value = parse(d)
                r[name] = value
        return r
    elif root.tag in ['string','i4','i8','boolean','double','int']:
        return root.text
    elif root.tag in ['fault']:
        for value in root:
            if value.tag == 'value':
                return parse(value)
    elif root.tag in ['params']:
        for value in root:
            if value.tag == 'param':
                for c in value:
                    return parse(c)
    elif root.tag in ['nil']:
        return None
    else :
        r = {}
        for c in root:
            if r.get(root.tag) is None:
                r[root.tag]=[]
            r[root.tag] = (parse(c))
        return r


