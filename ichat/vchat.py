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
		payload_size = struct.calcsize("L")
		cv2.namedWindow('Remote', cv2.WINDOW_NORMAL)
		while True:
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
			self.interval = 3
		self.fx = 1 / (self.interval + 1)
		if self.fx < 0.3:
			self.fx = 0.3
		if version == 4:
			self.sock = socket(AF_INET, SOCK_STREAM)
		else:
			self.sock = socket(AF_INET6, SOCK_STREAM)
		# self.cap = cv2.VideoCapture(0)
		#congbendishipin huoqu
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

		while self.cap.isOpened():
			ret, frame = self.cap.read()
			sframe = cv2.resize(frame, (0, 0),fx=self.fx,fy=self.fx)
			data = pickle.dumps(frame)
			zdata = zlib.compress(data, zlib.Z_BEST_COMPRESSION)
			try:
				self.sock.sendall(struct.pack("L", len(zdata) + zdata))
			except:
				break
			for i in range(self.interval):
				self,cap.read()


