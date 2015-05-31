#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

# Author: Kin Lo <kinabcd@gmail.com>
import sys
import argparse
import feedparser
from rtorrent.remotecontrol import RemoteControl

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('uri', help='request URI')

args = parser.parse_args()
rtctl = RemoteControl()
d = feedparser.parse(args.uri)
for feed in d.entries:
    print( feed.title )
    for link in feed.links:
        if link.type == 'application/x-bittorrent' :
            rtctl.load(link.href)

