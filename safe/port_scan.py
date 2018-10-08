#!/usr/bin/env python3
# -*- conding: utf-8 -*-

'''
Usage: port_scan.py <host> <start_port>-<end_port>
'''

import sys
import thread
from socket import *

#测试TCP端口连接
def tcp_test(port):
	sock = socket(AF_INET, SOCK_STREAM)
	sock.settimeout(10)
	result = sock.connect_ex((target_ip,port))
	if result == 0:
		lock.acquire()
		print("Opened Port: ", port)
		lock.release()

if __name__ == '__main__':
	host = sys.argv[1]
	portstrs = sys.argv[2].split('-')

	start_port = int(portstrs[0])
	end_port = int(portstrs[1])

	target_ip = gethostbyname(host)

	lock = thread.allocate_lock()

	for port in range(start_port, end_port):
		thread.start_new_thread(tcp_test, (port,))	#创建一个线程
		
		
另
python-nmap 是可以在Python中使用nmap端口扫描器的包
sudo apt-get install namp python-nmap
https://xael.org/pages/python-nmap-en.html
