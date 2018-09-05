#!/usr/bin/env python3
# coding: utf-8

import os
import sys
import shlex
import getpass
import socket
import signal
import subprocess
import platform
from func import *


# 字典表，用于存储命令与函数的映射
built_in_cmds = {}

#解析命令
def tokenize(string):
	'''
	. 将 sting 按shell 的语法规则进行分割；即按空格符将命令与参数分开
	. 返回 string 的分割列表
	. 例如 ls -l /home 分割后:['ls', '-l', '/home']
	'''
	return shlex.split(string)

#预处理
def preprocess(tokens):
	#用于存储处理后的token
	processed_token = []
	for token in tokens:
		if token.startswith('$'):
			# os.getenv() 用于获取环境变量的值
			#变量不存在则返回空
			processed_token.append(os.getenv(token[1:]))
		else:
			processed_token.append(token)
	return processed_token

#自定义的信号处理函数，当当前进程被强制中断时触发
def handler_kill(signum, frame):
	raise OSError("Killed!")

#执行命令
def execute(cmd_tokens):
	with open(HISTORY_PATH, 'a') as history_file:
		history_file.write(' '.join(cmd_tokens) + os.linesep) #各命令组成部分以空格连接并且最后命令以换行结尾
	if cmd_tokens:
		#获取命令
		cmd_name = cmd_tokens[0]
		#获取命令参数
		cmd_args = cmd_tokens[1:]
		#如果当前命令在命令表中则传入参数，执行相应的函数
		if cmd_name in built_in_cmds:
			return built_in_cmds[cmd_name](cmd_args)
		#监听Ctrl-C 信号
		signal.signal(signal.SIGINT, handler_kill)
		
		#如果当前系统不是 Windows则创建子进程
		if platform.system() != "Windows":
			#Unix 平台调用子进程执行命令
			p = subprocess.Popen(cmd_tokens)
			
			#父进程从子进程读取数据，直到读到 EOF
			#此处主要用来等待子进程终止运行
			p.communicate()
		else:
			#Windows 平台
			command = ""
			command = ' '.join(cmd_tokens)
			#执行命令
			os.system(command)
	#返回状态
	return SHELL_STATUS_RUN

#打印命令提示符
def display_cmd_prompt():
	#获取当前用户名
	user = getpass.getuser()
	#获取当前运行Python 程序的机器的主机名
	hostname = socket.gethostname()
	#获取当前工作路径
	cwd = os.getcwd()
	#获取路径cwd 的最低一级目录
	base_dir = os.path.basename(cwd)
	#如果用户当前位于用户的根目录下，使用‘~’ 代替根目录
	home_dir = os.path.expanduser('~')
	if cwd == home_dir:
		base_dir = '~'
	#输出命令提示符
	if platform.system() != 'Windows':
		sys.stdout.write("[\033[1;33m%s\033[0;0m@%s \033[1;36m%s\033[0;0m]$" % (user, hostname, base_dir))
	else:
		sys.stdout.write("[%s@%s %s]$" % (user, hostname, base_dir))
	#强制刷新
	sys.stdout.flush()

#忽略信号
def ignore_signals():
	if platform.system() != "Windows":
		#忽略Crtl-Z 信号
		signal.signal(signal.SIGTSTP, signal.SIG_IGN)
	#忽略Ctrl-C 信号
	signal.signal(signal.SIGINT, signal.SIG_IGN)


def shell_loop():
	status = SHELL_STATUS_RUN

	while status == SHELL_STATUS_RUN:
		# 打印命令提示符，形如 `[<user>@<hostname> <base_dir>]$`
		display_cmd_prompt()

		# 忽略 Ctrl-Z 或 Ctrl-C 信号
		ignore_signals()
		
		try:
			# 读取命令
			cmd = sys.stdin.readline()

			#解析命令，将命令拆分，返回一个列表
			cmd_tokens = tokenize(cmd)

			#预处理函数
			#将命令中的环境变量用真实值替换
			cmd_tokens = preprocess(cmd_tokens)
			# 执行命令并返回 shell 的状态
			status = execute(cmd_tokens)
		except:
			#错误处理
			#sys.exc_info() 函数返回一个包含三个值的元祖（type，value，traceback），这三个值产生于最近一次被处理的异常
			_, err, _ = sys.exc_info()
			print(err)



def register_command(name, func):
	'''
	注册命令，使命令和相应的函数建立映射关系
	@param name: 命令名
	@param func: 函数名
	'''
	built_in_cmds[name] = func

def init():
	'''
	注册命令
	'''
	register_command("cd", cd)
	register_command("exit", exit)
	register_command("getenv", getenv)
	register_command("history", history)



def main():
	#初始化，即建立命令与函数映射关系
	init()
	#处理命令主程序
	shell_loop()

if __name__ == '__main__':
	main()
