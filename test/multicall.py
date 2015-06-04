import rtorrent
rt = rtorrent.RemoteControl()
print(rt.sendCall('d.multicall', ['default', 'd.is_open=', 'd.get_hash=']))
