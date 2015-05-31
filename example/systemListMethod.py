#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

# Author: Kin Lo <kinabcd@gmail.com>

from rtorrent.remotecontrol import RemoteControl
rtctl = RemoteControl()
print(rtctl.systemlistMethod())
