#-*- coding: utf-8 -*-
'''
分为：存储模块、获取模块、检测模块、接口模块

'''

from flask import Flask, g
from db import RedisClient

__all__ = ['app']
app = Flask(__name__)

def get_conn():
	if not hasattr(g, 'redis'):
		g.redis = RedisClient()
	return g.redis

@app.route('/')
def index():
	return '<h2>Welcome to Proxy Pool System</h2>'


@app.route('/random')
def get_proxy():
	'''
	随机代理
	'''
	conn = get_conn()
	return conn.random()

@app.route('/count')
def get_counts():
	'''
	代理池总量
	'''
	conn = get_conn()
	return str(conn.count())

if __name__== '__main__':
	app.run()







