#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

# Author: Kin Lo <kinabcd@gmail.com>
from rtorrent import scgi
from rtorrent import xmlrpc

class RemoteControl:
    def __init__(self, host='localhost', port=5000, path = '/'):
        self.host = host
        self.port = port
        self.path = path
            

    def sendCall(self, methodName, params = []):
        if not isinstance(params,list): params = [params]
        socket = scgi.get_socket(self)
        x = xmlrpc.XMLRPC(methodName)
        for param in params:
            x.addParam(param)
        data = str(x)
        result = scgi.request(socket=socket, method="GET", uri=self.path, data=data.encode('utf8'))
        socket.close()
        return xmlrpc.parse(result['body'])
    
    def load(self, uri, start =True):
        return self.sendCall('load_start' if start else 'load', uri)

    def systemlistMethod(self) :
        return self.sendCall('system.listMethods')
    


