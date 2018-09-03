#!/usr/bin/env python3
# coding: utf-8

import sys
import os
import time
import threading
import tty
import cv2
import pyprind

class CharFrame:

	ascii_char = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!1I;:,\"^`'."
	# 像素映射到字符
	def pixelToChar(self, luminance):#接收像素的亮度信息
		return self.ascii_char[int(luminance / 256 * len(self.ascii_char))]

	#将普通帧转为 ASCII字符帧	
	def convert(self, img, limitSize=-1, fill=False, wrap=False):
		'''
		img:OpenCV打开图片返回的对象，numpy.ndarray;
		limitSize:接受一个元祖,表示图片的限宽限高；
		fill：表示是否用空格填充图片至限宽；
		wrap：表是否在行末添加换行符
		'''
		if limitSize != -1 and (img.shape[0] > limitSize[1] or img.shape[1] > limitSize[0]):
			#img.shape:返回一个元祖，含有图片的行数（高），列数（宽）以及颜色通道数。灰色图不包含颜色 通道数
			img = cv2.resize(img, limitSize, interpolation=cv2.INTER_AREA)
			# resize() 缩放图片
		ascii_frame = ''
		blank = ''
		if fill:
			blank += ' ' * (limitSize[0] - img.shape[1])
		if wrap:
			blank += '\n'
		for i in range(img.shape[0]):
			for j in range(img.shape[1]):
				ascii_frame += self.pixelToChar(img[i, j])
			ascii_frame += blank
		return ascii_frame


class I2Char(CharFrame):

	result = None

	def __init__(self, path, limitSize=-1, fill=False, wrap=False):
		self.genCharImage(path, limitSize, fill, wrap)

	def genCharImage(self, path, limitSize=-1, fill=False, wrap=False):
		im = cv2.imread(path, cv2.IMREAD_GRAYSCALE) #读取图片，第二个参数指示打开图片的方式
		if img is None:
			return
		self.result = self.convert(img, limitSize, fill, wrap)

	def show(self, stream=2):
		if self.result is None:
			return

		if stream == 1 and os.isatty(sys.stdout.fileno()):
			self.streamOut = sys.stdout.write
			self.streamFlush = sys.stdout.streamFlush
		elif stream == 2 and os.isatty(sys.stderr.fileno()):
			self.streamOut = sys.stderr.write
			self.streamFlush = sys.stderr.flush
		elif hasattr(stream, 'write'):
			self.streamOut = stream.write
			self.streamFlush = stream.flush
		self.streamOut(self.result)
		self.streamFlush()
		self.streamOut('\n')


class V2Char(CharFrame):

	charVideo = []
	timeInterval = 0.033

	def __init__(self, path):
		if path.endswith('txt'):
			self.load(path)
		else:
			self.genCharVideo(path)

	def genCharVideo(self, filepath):
		self.charVideo = []
		# 读取视频 文件
		cap = cv2.VideoCapture(filepath)
		self.timeInterval = round(1 / cap.get(5), 3)
		# get() 获取视频的属性，get(3)、get(4)返回视频的宽高信息; get(5)返回帧率； get(7) 返回总帧数
		nf = int(cap.get(7))
		print('Generate char video, please wait...')
		for i in pyprind.prog_bar(range(nf)):
			rawFrame = cv2.cvtColor(cap.read()[1], cv2.COLOR_BGR2GRAY)# read() 读取下一帧；cvtColor() 转换图像的颜色空间
			# os.get_terminal_size() 返回当前终端的列数和行数
			frame = self.convert(rawFrame, os.get_terminal_size(), fill=True)
			self.charVideo.append(frame)
		cap.release()

	def export(self, filepath):
		if not self.charVideo:
			return
		with open(filepath, 'w') as f:
			for frame in self.charVideo:
				f.write(frame + '\n')

	def load(self, filepath):
		self.charVideo = []
		for i in open(filepath):
			self.charVideo.append(i[:-1])

	def play(self, stream=1):
		# 光标定位转移编码不兼容 Windows
		if not self.charVideo:
			return
		if stream == 1 and os.isatty(sys.stdout.fileno()):
			self.streamOut = sys.stdout.write
			self.streamFlush = sys.stdout.flush
		elif stream == 2 and os.isatty(sys.stderr.fileno()):
			self.streamOut = sys.stderr.write
			self.streamFlush = sys.stderr.flush
		elif hasattr(stream, 'write'):
			self.streamOut = stream.write
			self.streamFlush = stream.flush

		old_settings = None
		breakflag = None
		# 获得标准输入的文件描述符
		fd = sys.stdin.fileno()

		def getChar():
			nonlocal breakflag
			nonlocal old_settings
			# 保存标准输入的属性
			old_settings = termios.tcgetattr(fd)
			# 设置标准输入为原始模式
			tty.setraw(sys.stdin.fileno())
			# 读取一个字符
			ch = sys.stdin.read(1)
			breakflag = True if ch else False

		#创建线程
		getchar = threading.Thread(target=getChar)
		#设置为守护进程
		getchar.daemon = True
		#启动守护线程
		getchar.start()
		#输入的字符画行数
		rows = len(self.charVideo[0]) // os.get_terminal_size()[0]
		for frame in self.charVideo:
			# 接收到输入则退出循环
			if breakflag is True:
				break
			self.streamOut(frame)
			self.streamFlush()
			time.sleep(self.timeInterval)
			# 共rows 行，光标上移 rows -1 行回到开始处
			self.streamOut('\003[{}A\r'.format(rows - 1))
		# 恢复标准输入为原来的属性
		termios.tcsetattr(fd, termios.TCSADRAIM, old_settings)
		# 光标下移 rows-1行到最后一行，清空最后一行
		self.streamOut('\033[{}B\033[K'.format(row - 1))
		# 清空最后一帧的所有行（从倒数第二行起）
		for i in range(rows-1):
			#光标上移一行
			self.streamOut('\033[1A')
			#清空所在行
			self.streamOut('\r\033[K')
		info = 'User interrupt!\n' if breakflag else 'Finished!\n'
		self.streamOut(info)


if __name__ == '__main__':
	import argparse
	#设置命令行参数
	parser = argparse.ArgumentParser()
	parser.add_argument('file', help='Video file or charvideo file')
	parser.add_argument('-e', '--export', nargs='?', const='charvideo.txt', 
						help='Export charvideo file')
	#获取参数
	args = parser.parse_args()
	v2char = V2Char(args.file)
	if args.export:
		v2char.export(args.export)
	v2char.play()
