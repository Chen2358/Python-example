#!/usr/bin/env python3
# encoding: utf-8

'''
尝试暴力破解zip文件
1、zipfile模块是python中自带的模块，提供了对zip文件的创建读、写、追加、解压以及列出zip文件列表的工具；
2、argparse模块来解析命令行参数
运行 
python3 decodeZip.py -f 1.zip -w pwd.txt

'''

import zipfile
import argparse
import os
from os.path import *


#解压文件
def tryZipPwd(zipFile, password, savePath):
	try:
		zipFile.extractall(path=savePath, pwd=password.encode('utf-8'))
		print('[+] Zip file decompression success, password: %s' % (password))
		return True
	except:
		print('[-] Zip file decompression failed, password: %s' % (password))

def main():
	#创建 ArgumentParser对象
	parser = argparse.ArgumentParser(description='Burte Crack Zip')
	#添加参数
	parser.add_argument('-f', dest='zFile', type=str, help='The zip file path.')
	parser.add_argument('-w', dest='pwdFile', type=str, help='password dictionary file.')
	zFilePath = None
	pwdFilePath = None

	try:
		options = parser.parse_args()
		zFilePath = options.zFile
		pwdFilePath = options.pwdFile
	except:
		print(parser.parse_args(['-h']))
		exit(0)

	if zFilePath == None or pwdFilePath == None:
		print(parser.parse_args('-h'))
		exit(0)
	#创建ZipFile对象，循环读取密码文件
	with zipfile.ZipFile(zFilePath) as zFile:
		with open(pwdFilePath) as f:
			for pwd in f.readlines():
				p, f = split(zFilePath)
				dirName = f.split('.')[0]
				dirPath = join(p, dirName)
				try:
					os.mkdir(dirPath)
				except:
					pass
				#调用解压缩函数，根据返回值判断是否找到密码，找到则退出循环
				ok = tryZipPwd(zFile, pwd.strip('\n'), dirPath)
				if ok:
					break

if __name__ == '__main__':
	main()
