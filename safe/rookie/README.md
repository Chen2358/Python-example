1、subprocess.Popen()可以实现在一个新的进程中启动一个子程序

第一个参数就是子程序的名字，shell=True则是说明程序在Shell中执行。stdout、stderr、stdin的值都是subprocess.PIPE，则表示用管道的形式与子进程交互。

2、socket服务端

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    s.bind(('0.0.0.0',7676))
    
    s.listen(1024)

3、socket客户端

def connectHost(ht,pt):

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    sock.connect((ht,int(pt)))
