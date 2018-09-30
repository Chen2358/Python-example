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
		self.lat = ''												#
		self.lng = ''												#
		self.fileName = ''											#
		self.setWindowTitle('Image positioning')					#
		self.verticalLayout_2 = QtWidgets.QVBoxLayout()				#
		self.verticalLayout = QtWidgets.QVBoxLayout()
		self.horizontalLayout= QtWidgets.QHBoxLayout()				#

		#
		self.textEdit = QtWidgets.QTextEdit()
		#
		sizePolicy =QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.textEdit.sizePolicy().hasHeightForWidth())
		self.textEdit.setSizePolicy(sizePolicy)
		self.textEdit.setMaximumSize(QtCore.QSize(16777215, 30))
		self.horizontalLayout.addWidget(self.textEdit)				#

		#
		self.selectButton = QtWidgets.QPushButton('Select')
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.selectButton.sizePolicy().hasHeightForWidth())
		self.selectButton.setSizePolicy(sizePolicy)
		self.horizontalLayout.addWidget(self.selectButton)

		#
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

		#
		self.webView = QWebView()
		self.webView.load(QUrl('http://map.baidu.com/'))
		self.verticalLayout.addWidget(self.webView)
		self.verticalLayout_2.addLayout(self.verticalLayout)
		self.setLayout(self.verticalLayout_2)

		self.positionButton.clicked.connect(self.reload)					#
		self.selectButton.clicked.connect(self.getPosition)					#

	#
	def d2l(self, gpsData):					#
		d = gpsData[0][0] / gpsData[0][1]	#
		m = gpsData[1][0] / gpsData[1][1]	#
		s = gpsData[2][0] / gpsData[2][1]	#
		return str(d + (m + s / 60) / 60)

	#
	def getPosition(self):
		fileDialog = QFileDialog()			#
		self.fileName= fileDialog.getOpenFileName()[0]						#
		self.textEdit.setText(self.fileName)								#
		exifData = piexif.load(self.fileName)								#

		#
		if exifData['GPS']:
			for k, v in exifData['GPS'].items():
				print('--->>', k, v)
			try:
				self.lat = self.d2l(exifData['GPS'][2])						#
				self.lng = self.d2l(exifData['GPS'][4])						#
				print('lat: ', self.lat)
				print('lng: ', self.lng)
			except:
				msg = QMessageBox.information(self, 'Error', 'To locate failure!')	#
		else:
			msg = QMessageBox.information(self, 'Warning', "This picture doesn't containt the GPS information!")

	#
	def reload(self):
		self.webView.load(QUrl('http://api.map.baidu.com/geocoder?location=%s,%s&coord_type=gcj02&output=html&src=personal|img_pos' % (self.lat,  self.lng)))

if __name__ == '__main__':
	app = QtWidgets.QApplication(sys.argv)
	window = MainWindow()
	window.show()
	app.exec()