'''
定义各种常量和路径
'''
import os

SHELL_STATUS_STOP = 0 # Shell 进程停止标识
SHELL_STATUS_RUN = 1 #Shell 进程运行标识

# 使用ps.path.expanduser('~') 获取当前操作系统平台的当前用户目录
HISTORY_PATH = os.path.expanduser('~') + os.sep + '.shell_history' #命令日志的存储路径
