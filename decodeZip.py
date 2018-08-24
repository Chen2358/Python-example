#!/usr/bin/env python3
# encoding: utf-8

import zipfile
import argparse
import os
from os.path import *

def tryZipPwd(zipFile, password, savePath):
	try:
		zipFile.extractall(path=savePath, pwd=password.encode('utf-8'))
		print('[+] Zip file decompression success, password: %s' % (password))
		return True
	except:
		print('[-] Zip file decompression failed, password: %s' % (password))

def main():
	parser = argparse.ArgumentParser(description='Burte Crack Zip')
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
				ok = tryZipPwd(zFile, pwd.strip('\n'), dirPath)
				if ok:
					break

if __name__ == '__main__':
	main()
