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

#python addTask_main.py

from addTask import add

if __name__ == '__main__':
    result = add.delay(5,5)
