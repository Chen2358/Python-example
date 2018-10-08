1、FTP 服务器

FTP服务器（File Transfer Protocol Server）是在互联网上提供文件存储和访问服务的计算机，它们依照FTP协议提供服务。
FTP是File Transfer Protocol(文件传输协议)。顾名思义，就是专门用来传输文件的协议。简单地说，支持FTP协议的服务器就是FTP服务器。

FTP是仅基于TCP的服务，不支持UDP。与众不同的是FTP使用2个端口，一个数据端口和一个命令端口（也可叫做控制端口）。通常来说这两个端口是21（命令端口）和20（数据端口）。但FTP 工作方式的不同，数据端口并不总是20。这就是主动与被动FTP的最大不同之处。主要有两种工作模式：

（1）主动FTP

FTP服务器的控制端口是21，数据端口是20，所以在做静态映射的时候只需要开放21端口即可，他会用20端口和客户端主动的发起连接。

（2）被动FTP

服务器的控制端口是21，数据端口是随机的，且是客户端去连接对应的数据端口，所以在做静态的映射话只开放21端口是不可以的。此时需要做DMZ。

2、pyftpdlib 库，可以简单假设一个FTP服务器

（1）安装：sudo pip3 install pyftpdlib

（2）启动：sudo python3 -m pyftpdllib -p 21

3、argparse 解析命令行，在解析命令行时可以根据添加参数时指定的help关键字的内容自动生成帮助文档


#用描述创建了ArgumentParser对象

parser = argparse.ArgumentParser(description = 'FTP Scanner')

#添加-H命令dest可以理解为咱们解析时获取-H参数后面值的变量名,help是这个命令的帮助信息

parser.add_argument('-H',dest='hostName',help='The host list with ","space')

parser.add_argument('-f',dest='pwdFile',help='Password dictionary file')


