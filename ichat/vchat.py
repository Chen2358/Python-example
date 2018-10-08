#!/usr/bin/env python3
# -*-coding: utf-8 -*-

from socket import *
import threading
import cv2
import sys
import struct
import pickle
import zlib
import numpy as np

#双向C/S连接
class Video_Server(threading.Thread):

	def __init__(self, port, version):
		threading.Thread.__init__(self)
		self.setDameon(True)
		self.ADDR = ('', port)
		if version == 4:
			self.sock = socket(AF_INET, SOCK_STREAM)
		else:
			self.sock = socket(AF_INET6, SOCK_STREAM)

	def __del__(self):
		self.sock.close()
		#服务器端连接成功后尝试创建一个窗口用于显示接收道德视频
		try:
			cv2.destoryAllWindows()
		except:
			pass

	def run(self):
		print("VIDEO server starts...")
		self.sock.bind(self.ADDR)
		self.sock.listen(1)
		conn, addr = self.sock.accept()
		print("remote VIDEO client success connected...")
		data = "".encode("utf-8")
		payload_size = struct.calcsize("L")	#记录当前从缓冲区读入的数据长度
		cv2.namedWindow('Remote', cv2.WINDOW_NORMAL)
		while True:
			#对payload_size区分帧的边界，避免多个帧或不到一个帧
			#超过payload_size时，剩余部分和下次读出的数据流合并，不足时将合并西祠读取的数据流到当前帧中
			while len(data) < payload_size:
				data += conn.recv(81920)
			packed_size = data[:payload_size]	
			data = data[payload_size:]
			msg_size = struct.unpack("L", packed_size)[0]
			while len(data) < msg_size:
				data += conn.recv(81920)
			zframe_data = data[:msg_size]
			data = data[msg_size:]
			frame_data = zlib.decompress(zframe_data)
			frame = pickle.loads(frame_data)
			cv2.imshow('Remote', frame)
			if cv2.waitKey(1) & 0xFF == 27:
				break


class Video_Client(threading.Thread):

	def __init__(self, ip, port, level, version):
		threading.Thread.__init__(self)
		self.setDaemon(True)
		self.ADDR = (ip, port)
		if level <= 3:
			self.interval = level
		else:
			self.interval = 3	#最大帧间隔为3
		self.fx = 1 / (self.interval + 1)
		#限制最坏情况的缩放比例为0.3
		if self.fx < 0.3:
			self.fx = 0.3
		if version == 4:
			self.sock = socket(AF_INET, SOCK_STREAM)
		else:
			self.sock = socket(AF_INET6, SOCK_STREAM)
		# self.cap = cv2.VideoCapture(0)
		#从本次视频获取
		self.cap = cv2.VideoCapture('test.mp4')

	def __del__(self):
		self.sock.close()
		self.cap.release()

	
	def run(self):
		print("VIDEO client starts...")
		while True:
			try:
				self.sock.connect(self.ADDR)
				break
			except:
				time.sleep(3)
				continue
		print("VIDEO client connected...")

		while self.cap.isOpened():	#cap 变量用于捕获默认摄像头的输出
			ret, frame = self.cap.read()
			#视频缩放的数据压缩
			sframe = cv2.resize(frame, (0, 0),fx=self.fx,fy=self.fx) #第二个参数为缩放中心，后两个参数为缩放比例
			#将捕获的帧用户pickle.dumps方法打包
			data = pickle.dumps(frame)
			zdata = zlib.compress(data, zlib.Z_BEST_COMPRESSION)
			try:
				#使用sock.sendall方法发送
				self.sock.sendall(struct.pack("L", len(zdata) + zdata))	#struct.pack方法为每批数据加了一个头，用户接收方确认接收数据的长度
			except:
				break
			for i in range(self.interval):
				self,cap.read()


