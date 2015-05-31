#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

# Author: Kin Lo <kinabcd@gmail.com>

import rtorrent
rtctl = rtorrent.RemoteControl()
print(rtctl.systemlistMethod())
