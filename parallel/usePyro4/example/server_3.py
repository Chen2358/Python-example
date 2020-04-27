#coding: utf-8

from __future__ import print_function       #拒绝 隐式导入
import Pyro4
import chainTopology

this = "3"              #当前Server
next = "1"
servername = "example.chainTopology." + this
daemon = Pyro4.core.Daemon()
obj = chainTopology.Chain(this, next)
uri = daemon.register(obj)
ns = Pyro4.locateNS()
ns.register(servername, uri)
print('Server_%s started ' % this)
daemon.requestLoop()
