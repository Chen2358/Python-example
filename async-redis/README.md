简单的异步 Redis 客户端


1、Redis 是一个内存数据库，常用于各种 Web 项目中。既可以当做缓存使用，也可以用作 nosql 数据库。Redis 可以通过不同的指令进行不同的操作，比如通过 SELECT 指令进行选择数据库操作， AUTH 指令进行认证， SET 指令设置数据项。这些指令在底层都会被翻译成协议数据发送给 Redis 服务器。其实 Redis 的通信协议非常简单。

Redis 的通信协议是基于文本的，且以行为划分，每行以 \r\n 结束。每一行都有一个消息头，消息头共分为5种,分别如下:

+表示一个正确的状态信息，具体信息是当前行 + 后面的字符；

-表示一个错误信息，具体信息是当前行－后面的字符；

星号 表示消息体总共有多少行，不包括当前行,* 后面是具体的行数；

$ 表示下一行数据长度，不包括换行符长度 \r\n, $ 后面则是对应的长度的数据；

: 表示返回一个数值，：后面是相应的数字节符；

2、环境配置
$ mkdir project && cd project

$ sudo pip3 install tornado==4.1

$ wget http://labfile.oss.aliyuncs.com/courses/518/async-redis.tgz

$ tar xvf async-redis.tgz

$ cd async-redis

$ sudo python3 setup.py install
