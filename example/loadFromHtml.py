#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

# Author: Kin Lo <kinabcd@gmail.com>
import argparse
import sys
from pyquery import PyQuery as pq
from rtorrent.remotecontrol import RemoteControl

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('uri', help='request URI')

args = parser.parse_args()
rtctl = RemoteControl()
q = pq(url=args.uri)
tagas = q('a')
count = 0
for taga in tagas: 
    href = pq(taga).attr('href')
    if href.startswith('magnet:') :
        rtctl.load(href)
        count += 1
print('import', count, 'magnet')

