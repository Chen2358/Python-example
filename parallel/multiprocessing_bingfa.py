#coding:  utf-8

'''
基于进程的并发

1、mpi4py依赖库
https://blog.csdn.net/sinat_30967935/article/details/82988659
2、mpi4py库
https://www.jianshu.com/p/ba6f7c9415a0
'''

#产生一个进程
'''
import multiprocessing

def foo(i):
    print("called function in  process: %s" %i)
    return

if __name__ == '__main__':
    Process_obj = []
    for i in range(5):
        p = multiprocessing.Process(target=foo, args=(i,))
        Process_obj.append(p)
        p.start()
        p.join()

'''

#为进程命名
'''
import multiprocessing
import  time

def foo():
    name = multiprocessing.current_process().name
    print("starting %s \n" % name)
    time.sleep(3)
    print("Existing %s  \n" % name)
    
if __name__ == '__main__':
    process_with_name = multiprocessing.Process(name='foo_process', target=foo)     #命名进程
    process_with_name.daemon = True
    process_with_default_name = multiprocessing.Process(target=foo)                 #默认名字
    process_with_name.start()
    process_with_default_name.start()
    
    process_with_name.join()
    process_with_default_name.join()
'''

#在后台运行进程
'''
import multiprocessing
import time

def foo():
    name = multiprocessing.current_process().name
    print("starting %s " % name)
    time.sleep(3)
    print("existing %s " % name)
    
if __name__ == '__main__':
    background_process = multiprocessing.Process(name='background_process', target=foo)
    background_process.daemon =True
    No_background_process = multiprocessing.Process(name='No_background_process', target=foo)
    No_background_process.daemon = False
    background_process.start()
    No_background_process.start()
'''

#杀掉进程
'''
import multiprocessing
import time

def foo():
    print('starting function')
    time.sleep(0.1)
    print('exiting function')
    
if __name__ == '__main__':
    p = multiprocessing.Process(target=foo)
    print('Process before execution: ', p, p.is_alive())
    p.start()
    print('Process running: ', p, p.is_alive())
    p.terminate()                                           #杀进程
    print('Process terminated: ', p, p.is_alive())
    p.join()
    print('Process joined: ', p, p.is_alive())
    print('Process exit  code: ', p.exitcode)  #-15             #exitcode: <0进程被-1*的信号杀死并以此 作为ExitCode退出; >0：进程有错误；==0：无错误退出
'''

#在子类中使用进程
"""
import multiprocessing

class MyProcess(multiprocessing.Process):
    '''
    (1)继承Process;
    (2)重写__init__
    (3)重写run()实现  Process启动时执行的任务 
    '''
    def run(self):
        print('called run method in process: %s' % self.name)
        return
    
if __name__ == '__main__':
    jobs = []
    for i in range(5):
        p = MyProcess()
        jobs.append(p)
        p.start()
        p.join()
"""

#进程间交换对象
#Multiprocessing中的Communication Channel有队列（queue）和  管道（pipe）

#使用队列交换对象：Queue返回一个进程共享的对象，是线程安全和进程安全的。任何可可序列化的对象都 可以通过它进行交换
'''
import multiprocessing
import random
import time

class Producer(multiprocessing.Process):
    
    def __init__(self, queue):
        multiprocessing.Process.__init__(self)
        self.queue = queue
        
    def run(self):
        for i in range(10):
            item = random.randint(0, 256)
            self.queue.put(item)
            print('Process Producer: item %d appended to queue %s'  % (item, self.name))
            time.sleep(1)
            print('The size of queue is %s' % self.queue.qsize())
            

class Consumer(multiprocessing.Process):
    
    def __init__(self, queue):
        multiprocessing.Process.__init__(self)
        self.queue = queue
        
    def run(self):
        while True:
            if self.queue.empty():
                print('The queue is empty')
                break
            else:
                time.sleep(2)
                item = self.queue.get()
                print('Process Consumer: item  %d popped from by %s \n' % (item, self.name))
                time.sleep(1)
                
if __name__  == '__main__':
    queue = multiprocessing.Queue()
    process_producer = Producer(queue)
    process_consumer = Consumer(queue)
    process_producer.start()
    process_consumer.start()
    
    process_producer.join()
    process_consumer.join()
'''

#使用管道交换对象
#管道完成以下：(1)返回一对被管道连接 的对象；(2)对象有 send/receive()方法可以通信
'''
import multiprocessing

def create_items(pipe):
    output_pipe, _ = pipe
    for item in range(10):
        output_pipe.send(item)
    output_pipe.close()
    
def multiply_items(pipe_1, pipe_2):
    close, input_pipe = pipe_1
    close.close()
    output_pipe,  _ = pipe_2
    try:
        while True:
            item = input_pipe.recv()
            output_pipe.send(item  * item)
    except EOFError:
        output_pipe.close()
        
if __name__ ==  '__main__':
    #第一个进程管道发出数字
    pipe_1 = multiprocessing.Pipe(True)
    process_pipe_1  = multiprocessing.Process(target=create_items, args=(pipe_1,))
    process_pipe_1.start()
    
    #第二个进程管道接收数字 并计算
    pipe_2  = multiprocessing.Pipe(True)
    process_pipe_2 = multiprocessing.Process(target=multiply_items, args=(pipe_1, pipe_2,))
    process_pipe_2.start()
    pipe_1[0].close()
    pipe_2[0].close()
    try:
        while True:
            print(pipe_2[1].recv())
    except EOFError:
        print('end')
'''

#进程间同步
'''
import multiprocessing

from multiprocessing import Barrier, Lock, Process
from time import time
from datetime import datetime

def test_with_barrier(synchronizer, serializer):
    name = multiprocessing.current_process().name
    synchronizer.wait()
    now = time()
    with serializer:
        print("process %s ----> %s" % (name, datetime.fromtimestamp(now)))
        
def test_without_barrier():
    name = multiprocessing.current_process().name
    now = time()
    print("process %s ----> %s" % (name, datetime.fromtimestamp(now)))


if __name__ == '__main__':
    synchronizer = Barrier(2)
    serializer = Lock()
    Process(name='p1 - test_with_barrier', target=test_with_barrier, args=(synchronizer, serializer)).start()
    Process(name='p2 - test_with_barrier', target=test_with_barrier, args=(synchronizer, serializer)).start()
    Process(name='p3 - test_without_barrier', target=test_without_barrier).start()
    Process(name='p4 - test_without_barrier', target=test_without_barrier).start()
'''

#进程间管理进程状态
#管理者对象
'''
import multiprocessing

def worker(dictionary, key, item):
    dictionary[key] = item
    print("key = %d value = %d" % (key, item))
              
if  __name__ == '__main__':
    mgr = multiprocessing.Manager()
    dictionary = mgr.dict()
    jobs = [multiprocessing.Process(target=worker, args=(dictionary, i, i * 2)) for i in range(10)]
    for j in jobs:
        j.start()
    for j in jobs:
        j.join()
    print('Results: ', dictionary)
'''

#使用进程池
'''
import multiprocessing

def func_square(data):
    result  = data * data
    return result

if __name__ == '__main__':
    inputs = list(range(100))
    pool = multiprocessing.Pool(processes=4)
    pool_outputs  = pool.map(func_square, inputs)
    pool.close()
    pool.join()
    print('Pool:   ', pool_outputs)
   
'''

#使用 mpi4py模块
#mpiexec  -n 5 python  helloWorld_MPI.py
'''
from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
print("Hello world from process ", rank)
'''

#点对点通信
#mpiexec -n 9 python multiprocessing_bingfa.py
'''
from mpi4py import MPI
comm = MPI.COMM_WORLD
rank = comm.rank
print("my rank is: ", rank)

if rank == 0:
    data = 10000000
    destination_process = 4
    comm.send(data, dest=destination_process)
    print("sending data  %s" % data + "to process % d" % destination_process)
    
if rank == 1:
    destination_process = 8
    data = "hello"
    comm.send(data, dest=destination_process)
    print("sending data % s:" % data + "to process %d" % destination_process)
    
if rank == 4:
    data = comm.recv(source = 0)
    print("data received is = % s" % data)
    
if rank == 8:
    data1 = comm.recv(source = 1)
    print('data1 received is = %s' % data1)
'''

#避免死锁
#mpiexec -n 9 python multiprocessing_bingfa.py
"""
from mpi4py import MPI
comm = MPI.COMM_WORLD
rank = comm.rank
print("my rank is: ", rank)

'''
#死锁：send()、recv()都是阻塞的，都要等数据传输完成后才会结束
if rank == 1:
    data_send = 'a'
    destination_process = 5
    source_process = 5
    data_received = comm.recv(source=source_process)
    comm.send(data_send, dest=destination_process)
    print("sending data  %s" % data_send + "to process % d" % destination_process)
    print("data received is = %s" %  data_received)
    
if rank == 5:
    data_send = 'b'
    destination_process = 1
    source_process = 1
    data_received = comm.recv(source=source_process)
    comm.send(data_send, dest=destination_process)
    print("sending data  %s" % data_send + "to process % d" % destination_process)
    print("data received is = %s" %  data_received)
'''
'''
#解决1：交换发送者和接收者顺序
if rank == 1:
    data_send = 'a'
    destination_process = 5
    source_process = 5
    comm.send(data_send, dest=destination_process)
    data_received = comm.recv(source=source_process)
    print("sending data  %s" % data_send + " to process % d" % destination_process)
    print("data received is = %s" %  data_received)
    
if rank == 5:
    data_send = 'b'
    destination_process = 1
    source_process = 1
    comm.send(data_send, dest=destination_process)
    data_received = comm.recv(source=source_process)  
    print("sending data  %s" % data_send + " to process % d" % destination_process)
    print("data received is = %s" %  data_received)
'''

#解决2：使用Sendrecv

if rank == 1:
    data_send = 'a'
    destination_process = 5
    source_process = 5
    data_received = comm.sendrecv(data_send, dest=destination_process, source=source_process)
    print("sending data  %s" % data_send + " to process % d" % destination_process)
    print("data received is = %s" %  data_received)
    
if rank == 5:
    data_send = 'b'
    destination_process = 1
    source_process = 1
    data_received = comm.sendrecv(data_send, dest=destination_process, source=source_process)
    print("sending data  %s" % data_send + " to process % d" % destination_process)
    print("data received is = %s" %  data_received)
"""

#集体通信：使用briadcase通讯
#buf = comm.bcast(data_to_share, rank_of_root_process):将root消息中包含的信息发送给属于 comm 通讯组其他的进程，每个进程必须通过相同的 root 和 comm 来调用它。
#mpiexec -n 10 python multiprocessing_bingfa.py
'''                 
from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()

if rank == 0:
    variable_to_share = 100
else:
    variable_to_share = None
variable_to_share = comm.bcast(variable_to_share,  root=0)      #函数中参数为要发送的数据和发送者的进程
print("process =  %d" % rank + " variable shared = %d"  % variable_to_share)
'''

#集体通信：使用scatter通讯
#recvbuf  = comm.scatter(sendbuf, rank_of_root_process):将相同的数据发送给所有在监听 的进程
#mpiexec -n 11 python multiprocessing_bingfa.py
'''
from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()

if rank == 0:
    array_to_share = [x for x in range(0, 11) ]
else:
    array_to_share = None
    
recvbuf = comm.scatter(array_to_share, root=0)      #第i个变量发送 给第i个进程
print("process = %d" %  rank + " recvbug = %d" % recvbuf)
'''

#集体通信：使用gather通讯
#recvbuf = comm.gather(sendbuf, rank_of_root_process):将所有进程发送数据向root进程的
#mpiexec -n 5 python multiprocessing_bingfa.py
'''
from mpi4py import MPI

comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()
data = (rank+1) ** 2
data = comm.gather(data, root=0)
if rank == 0:
    print("rank = %s" % rank + "...receiving data to other process")
    for i in range(1, size):
        data[i] = (i+1) ** 2
        value = data[i]
        print(" process %s receiving %s from process %s" %(rank, value, i))
'''

#集体通信：使用Alltoal通讯
#结合了scatter和gather
#mpiexec -n 5 python multiprocessing_bingfa.py
'''
from mpi4py import MPI
import numpy

comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()
a_size = 1

senddata = (rank+1) * numpy.arange(size, dtype=int)
recvdata = numpy.empty(size * a_size, dtype=int)

comm.Alltoall(senddata, recvdata)
print(" Process %s sending %s receiving %s" % (rank, senddata, recvdata))
'''

#简化操作
#mpiexec -n 3 python multiprocessing_bingfa.py
'''
import numpy

from mpi4py import MPI
comm = MPI.COMM_WORLD
size = comm.size
rank = comm.rank
array_size = 3
recvdata = numpy.zeros(array_size, dtype=numpy.int)
senddata = (rank+1)*numpy.arange(size,dtype=numpy.int)
print("process %s sending %s " % (rank , senddata))
comm.Reduce(senddata, recvdata, root=0, op=MPI.SUM)
print('on task', rank, 'after Reduce:    data = ', recvdata)
'''

#优化通讯

from mpi4py import MPI
import numpy as np
UP = 0
DOWN = 1
LEFT = 2
RIGHT = 3
neighbour_processes = [0,0,0,0]

if __name__ == "__main__":
    comm = MPI.COMM_WORLD
    rank = comm.rank
    size = comm.size
    grid_rows = int(np.floor(np.sqrt(comm.size)))
    grid_column = comm.size // grid_rows
    if grid_rows*grid_column > size:
        grid_column -= 1
    if grid_rows*grid_column > size:
        grid_rows -= 1
    if (rank == 0) :
        print("Building a %d x %d grid topology:" % (grid_rows, grid_column) )
    cartesian_communicator = comm.Create_cart( (grid_rows, grid_column), periods=(True, True), reorder=True)
    my_mpi_row, my_mpi_col = cartesian_communicator.Get_coords( cartesian_communicator.rank )
    neighbour_processes[UP], neighbour_processes[DOWN] = cartesian_communicator.Shift(0, 1)
    neighbour_processes[LEFT], neighbour_processes[RIGHT] =  cartesian_communicator.Shift(1, 1)
    print ("Process = %s row = %s column = %s ----> neighbour_processes[UP] = %s neighbour_processes[DOWN] = %s neighbour_processes[LEFT] =%s neighbour_processes[RIGHT]=%s" % (
    rank, my_mpi_row, my_mpi_col,neighbour_processes[UP],
    neighbour_processes[DOWN], neighbour_processes[LEFT],
    neighbour_processes[RIGHT]))













