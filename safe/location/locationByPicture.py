#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtWebKitWidgets import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import QtWidgets,QtCore, QtGui
import piexif
import sys


class MainWindow(QWidget):
	def __init__(self):
		super(MainWindow, self).__init__()
		self.lat = ''									#纬度
		self.lng = ''									#经度
		self.fileName = ''								#图片路径
		self.setWindowTitle('Image positioning')					#设置窗口标题
		self.verticalLayout_2 = QtWidgets.QVBoxLayout()					#创建垂直布局
		self.verticalLayout = QtWidgets.QVBoxLayout()
		self.horizontalLayout= QtWidgets.QHBoxLayout()					#创建水平布局
		
		#创建QTextEdit
		self.textEdit = QtWidgets.QTextEdit()
		#设置布局尺寸
		sizePolicy =QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.textEdit.sizePolicy().hasHeightForWidth())
		self.textEdit.setSizePolicy(sizePolicy)
		self.textEdit.setMaximumSize(QtCore.QSize(16777215, 30))
		self.horizontalLayout.addWidget(self.textEdit)				#将QTextEdit添加到水平布局中

		#创建selectButton
		self.selectButton = QtWidgets.QPushButton('Select')
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.selectButton.sizePolicy().hasHeightForWidth())
		self.selectButton.setSizePolicy(sizePolicy)
		self.horizontalLayout.addWidget(self.selectButton)

		#创建positionButton
		self.positionButton =QtWidgets.QPushButton('Position')
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,QtWidgets.QSizePolicy.Preferred)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.positionButton.sizePolicy().hasHeightForWidth())
		self.positionButton.setSizePolicy(sizePolicy)
		self.horizontalLayout.addWidget(self.positionButton)
		spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
		self.horizontalLayout.addItem(spacerItem)
		self.verticalLayout.addLayout(self.horizontalLayout)

		#创建QWebView
		self.webView = QWebView()
		self.webView.load(QUrl('http://map.baidu.com/'))
		self.verticalLayout.addWidget(self.webView)
		self.verticalLayout_2.addLayout(self.verticalLayout)
		self.setLayout(self.verticalLayout_2)

		self.positionButton.clicked.connect(self.reload)				#连接clicked信号到self.reload()槽
		self.selectButton.clicked.connect(self.getPosition)				#连接clicked信号到self。getPosition()槽

	#将GPS经纬度元组转换成度
	def d2l(self, gpsData):									
		d = gpsData[0][0] / gpsData[0][1]						#度
		m = gpsData[1][0] / gpsData[1][1]						#分
		s = gpsData[2][0] / gpsData[2][1]						#秒
		return str(d + (m + s / 60) / 60)

	#获取相片中经纬度并通过QWebView调用百度URI API 实现定位
	def getPosition(self):
		fileDialog = QFileDialog()							#创建文件对话框对象
		self.fileName= fileDialog.getOpenFileName()[0]					#打开文件对话框并获取选择的相片路径
		self.textEdit.setText(self.fileName)						#将相片路径名显示到QTextEdit上
		exifData = piexif.load(self.fileName)						#加载图片并返回Exif数据字典

		#判断是否包含GPS数据
		if exifData['GPS']:
			for k, v in exifData['GPS'].items():
				print('--->>', k, v)
			try:
				self.lat = self.d2l(exifData['GPS'][2])				#获取GPS信息中的纬度（度分秒）
				self.lng = self.d2l(exifData['GPS'][4])				#获取GPS信息中的经度（度分秒）
				print('lat: ', self.lat)
				print('lng: ', self.lng)
			except:
				msg = QMessageBox.information(self, 'Error', 'To locate failure!')	#信息提示框
		else:
			msg = QMessageBox.information(self, 'Warning', "This picture doesn't containt the GPS information!")

	#QWebView 加载URL（默认加载）
	def reload(self):
		#加载页面
		self.webView.load(QUrl('http://api.map.baidu.com/geocoder?location=%s,%s&coord_type=gcj02&output=html&src=personal|img_pos' % (self.lat,  self.lng)))

if __name__ == '__main__':
	app = QtWidgets.QApplication(sys.argv)
	window = MainWindow()
	window.show()
	app.exec()
