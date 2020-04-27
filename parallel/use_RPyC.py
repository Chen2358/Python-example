#coding: utf-8

#pip install rpyc

#先执行python rpyc_classic.py 运行服务器在执行 python use_RPyC.py


import rpyc
import sys
c = rpyc.classic.connect("localhost")
c.execute("print('hi python cookbook')")
c.modules.sys.stdout = sys.stdout
c.execute("print('hi here')")






















