# -*-* coding: utf-8 -*-


import os
from file_reader import YamlReader


BASE_PATH = os.path.split(os.path.dirname(os.path.abspath(__file__)))[0]
CONFIG_FILE = os.path.join(BASE_PATH, 'config', 'config.yml')
DATA_PATH = os.path.join(BASE_PATH, 'data')
DRIVER_PATH = os.path.join(BASE_PATH, 'drivers')
LOG_PATH = os.path.join(BASE_PATH, 'log')
REPORT_PATH = os.path.join(BASE_PATH, 'report')


#读取配置
class Config(object):

	def __init__(self, config=CONFIG_FILE):
		self.config = YamlReader(config).data

	def get(self, element, index=0):
		return self.config[index].get(element)

if __name__ == '__main__':
	c = Config()
	print(c.get('URL'))