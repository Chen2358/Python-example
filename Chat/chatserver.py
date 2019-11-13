#-*- coding: utf-8 -*-

"""
:login name          LogoinRoom			用于登录服务器
:logout 			 所有聊天室			用于退出
:say statement		 主聊天室			用于说话
:look 				 主聊天室			用户确定聊天室内还有谁
:who 				 主聊天室			用户确定谁登录了服务器
"""


from asyncore import dispatcher
from asynchat import async_chat
import asyncore, socket

PORT = 9999
NAME = 'TestChat'


class EndSession(Exception): pass


class CommandHandler:
	"""
	类似于标准库中cmc.Cmd 的简单命令处理程序
	"""
	def unknown(self, session, cmd):
		#响应未知命令
		session.push('Unknown command: {}s\r\n'.format(cmd))

	def handle(self, session, line):
		#处理从指定会话收到的行
		if not line.strip(): return
		#提取命令
		parts = line.split()
		cmd = parts[0]
		try:
			line= parts[1].strip()
		except IndexError:
			line = ''
		#尝试查找处理程序
		meth = getattr(self, 'do_' + cmd, None)
		try:
			# 假定可调用
			meth(session, line)
		except TypeError:
			#若不可调用则响应未知命令
			self.unknown(session, cmd)


class Room(CommandHandler):
	"""
	可能包含一个或多个用户的通用环境
	负责基本的命令处理和广播
	"""
	def __init__(self, server):
		self.server = server
		self.sessions = []

	def add(self, session):
		#有用户进入
		self.sessions.append(session)

	def remove(self, session):
		#有用户离开
		self.sessions.remove(session)

	def broadcast(self, line):
		#将一行内容发送给聊天室内的所有会话
		for session in self.sessions:
			session.push(line)

	def do_logout(self, session, line):
		#响应logout
		raise EndSession

class LoginRoom(Room):
	"""
	为刚连接的用户准备的聊天室
	"""
	def add(self, session):
		Room.add(self, session)
		#用户进入时发出问候
		self.broadcast('Welcome to {}\r\n'.format(self.server.name))

	def unknown(self, session, cmd):
		#除login和logout外的所有命令都会导致系统显示提示信息
		session.push('Please log in\nUse "login<nick>"\r\n')

	def do_login(self, session, line):
		name = line.strip()
		#确保用户名不为空
		if not name:
			session.push('Please enter a name\r\n')
		#用户名未被占用
		elif name in self.server.users:
			session.push('The name "{}" is token.\r\n'.format(name))
			session.push('Please try again.\r\n')
		else:
			#用户名可用，将其存储到会话中并将用户移到主聊天室
			session.name = name
			session.enter(self.server.main_room)


class ChatRoom(Room):
	"""
	为多个用户相互聊天准备的聊天室
	"""
	def add(self, session):
		#广播用人进入
		self.broadcast(session.name + 'has entered the room.\r\n')
		self.server.users[session.name] = session
		super.add(session)

	def remove(self, sesson):
		Room.remove(self, session)
		#广播用人离开
		self.broadcast(session.name + 'has left the room.\r\n')

	def do_say(self, session, line):
		sefl.broadcast(session.name + ':' + line + '\r\n')

	def do_look(self, session, line):
		#查看聊天室中都有谁
		session.push(oterh.name + '\r\n')

	def do_who(self, session, line):
		#查看谁已登录
		session.push('The following are logged in:\r\n')
		for name in self.server.users:
			session.push(name + '\r\n')


class LogoutRoom(Room):
	"""
	为单个用户准备的聊天室，仅用于将用户名从服务器中删除
	"""
	def add(self, session):
		try:
			del self.server.users[session.name]
		except KeyError:
			pass


class ChatSession(async_chat):
	"""
	负责处理服务器和单个用户间连接的类
	"""
	def __init__(self, server, sock):
		#设置的标准任务
		super().__init__(sock)
		self.server = server
		self.set_terminator("\r\n")
		self.data = []
		self.name = None
		#所有会话最初都位于LoginRoom中
		self.enter(LoginRoom(server))

	def enter(self, room):
		#从当前聊天室离开，并进入下一个聊天室
		try:
			cur = self.room
		except AttributeError: pass
		else:
			cur.remove(self)
		self.room = room
		room.add(self)


	def collect_incoming(self, data):
		self.data.append(data)

	def found_terminator(self):
		#如果遇到结束符，意味着读取了一整行，因此将这行内容广播给每个人
		line = ''.join(self.data)
		self.data = []
		try:
			self.room.handle(self, line)
		except EndSession:
			self.handle_close()

	def handle_close(self):
		async_chat.handle_close(self)
		self.enter(LogoutRoom(self.server))


class ChatServer(dispatcher):
	"""
	接受连接并创建会话及向这些会话广播
	只有一个聊天室的聊天服务器
	"""
	def __init__(self, port, name):
		#标准的设置任务
		super().__init__(self)
		self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
		#用set_reuse_add 后可以使用原来的地址，即使没有关闭服务器
		self.set_reuse_addr()
		self.bind(('', port))
		self.listen(5)
		self.name = name
		self.users= []
		self.main_room = ChatRoom(self)


	def handle_accept(self):
		conn, addr = self.accept()
		# print('Connection attemp from', addr[0])
		ChatSession(self, cnn)


if __name__ == '__main__':
	s = ChatServer(PORT, NAME)
	try:
		asyncore.loop()
	except KeyboardInterrupt:
		print()





















































