#coding: utf-8

'''
分布式编程
'''

# 使用Celery实现分布式任务

# (1)安装celery: pip install celry
# (2)安装Erlang: http://www.erlang.org/download.html
# (3)安装并运行RabbitMQ：http://www.rabbitmq.com/download.html
# (4)安装Flower: pip install -U flower

#使用Celery创建任务

#celery -A addTask.addTask worker  --loglevel=info
#报错：not enough values to unpack (expected 3, got 0),在win10上运行celery4.x版本就会出现这个问题，解决办法是安装一个eventlet: pip install eventlet
#celery -A addTask worker  --loglevel=info -P eventlet

from celery import Celery

app = Celery('addTask', broker='amqp://guest@localhost//')

@app.task
def add(x, y):
    return x + y

