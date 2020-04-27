#coding: utf-8

import Pyro4

@Pyro4.expose
class Server(object):
    def welcomeMessage(self, name):
        return ("Hi welcome " + str (name))

def startServer():
    server = Server()						#实例化Server
    daemon = Pyro4.Daemon()					#启动守护进程
    ns = Pyro4.locateNS()					#必须运行name server，得到地址
    uri = daemon.register(server)			#将server注册为Pyro4的对象
    ns.register("server", uri)
    print("Ready. Object uri =", uri)
    daemon.requestLoop()					#启动事件循环

if __name__ == "__main__":
    startServer()
