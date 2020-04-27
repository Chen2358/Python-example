#coding: utf-8
'''
基于线程的并发
'''


#定义线程
'''
import threading

def func(i):
	print("fuction called by thread %i\n" %i)
	return

threads = []

for i in range(5):
	t = threading.Thread(target=func, args=(i,))
	threads.append(t)
	t.start()
	t.join()
'''

#确定当前线程
'''
import threading
import time

def first_func():
	print(threading.currentThread().getName() + str(' is Starting '))
	time.sleep(2)
	print(threading.currentThread().getName() + str(' is Exiting '))

def second_func():
	print(threading.currentThread().getName() + str(' is Starting '))
	time.sleep(2)
	print(threading.currentThread().getName() + str(' is Exiting '))

def third_func():
	print(threading.currentThread().getName() + str(' is Starting '))
	time.sleep(2)
	print(threading.currentThread().getName() + str(' is Exiting '))

if __name__ == '__main__':
	t1 = threading.Thread(target=first_func, name='first_func')
	t2 = threading.Thread(target=second_func, name='second_func')
	t3 = threading.Thread(target=third_func)
	t1.start()
	t2.start()
	t3.start()
	t1.join()
	t2.join()
	t3.join()
'''

#实现一个线程 
'''
import threading
import _thread
import time

exitFlag = 0

class myThread(threading.Thread):						#1、定义Thread子类
	
	def __init__(self, threadID, name, counter):		#2、重写__init__方法
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.name = name
		self.counter = counter

	def run(self):										#3、重写 run方法 ，线程执行				
		print("Starting " + self.name)
		print_time(self.name, self.counter, 5)
		print("Exiting " + self.name)

def print_time(threadNmae, delay, counter):
	while counter:
		if exitFlag:
			thread.exit()
		time.sleep(delay)
		print("%s: %s" % (threadNmae, time.ctime(time.time())))
		counter -= 1

thread1 = myThread(1, "Thread-1", 1)
thread2 = myThread(2, 'Thread-2', 2)

thread1.start()
thread2.start()

thread1.join()
thread2.join()
print("Exiting Main Thread")
'''

#使用Lock进行 进程同步
'''
import threading

shared_resource_with_lock = 0
shared_resource_with_no_lock = 0
COUNT = 100000

shared_resource_lock = threading.Lock()

#有锁
def increment_with_lock():
	global shared_resource_with_lock
	for i in range(COUNT):
		shared_resource_lock.acquire()		#获得锁，locked
		shared_resource_with_lock += 1
		shared_resource_lock.release()		#释放锁, unlocked

def decrement_with_lock():
	global shared_resource_with_lock
	for  i in range(COUNT):
		shared_resource_lock.acquire()
		shared_resource_with_lock -= 1
		shared_resource_lock.release()

#没有锁，并不一定会出错，重复多次会出错
def increment_without_lock():
	global shared_resource_with_no_lock
	for i in range(COUNT):
		shared_resource_with_no_lock += 1

def decrement_without_lock():
	global shared_resource_with_no_lock
	for i in range(COUNT):
		shared_resource_with_no_lock -= 1

if __name__ == '__main__':
	t1 = threading.Thread(target=increment_with_lock)
	t2 = threading.Thread(target=decrement_with_lock)
	t3 = threading.Thread(target=increment_without_lock)
	t4 = threading.Thread(target=decrement_without_lock)
	t1.start()
	t2.start()
	t3.start()
	t4.start()
	t1.join()
	t2.join()
	t3.join()
	t4.join()
	print("The result of shared resource with lock  is %s" % shared_resource_with_lock)
	print("The result of shared resource with not lock is %s" % shared_resource_with_no_lock)

'''

#使用RLock进行线程同步
'''
import threading
import time

class Box(object):

	lock = threading.RLock()

	def __init__(self):
		self.total_items = 0

	def execute(self, n):
		Box.lock.acquire()
		self.total_items += n
		Box.lock.release()

	def add(self):
		Box.lock.acquire()
		self.execute(1)
		Box.lock.release()

	def remove(self):
		Box.lock.acquire()
		self.execute(-1)
		Box.lock.release()

def adder(box, items):
	while items > 0:
		print('adding 1 item in the box')
		box.add()
		time.sleep(1)
		items -= 1

def remover(box, items):
	while items  > 0:
		print('removing 1 item in  the box')
		box.remove()
		time.sleep(1)
		items -= 1

if __name__ == '__main__':
	items = 5
	print('putting %s items in the box.' %items)
	box = Box()
	t1 = threading.Thread(target=adder, args=(box, items))
	t2 = threading.Thread(target=remover, args=(box, items))
	t1.start()
	t2.start()

	t1.join()
	t2.join()
	print('%s items still remain in the box' % box.total_items)
'''

#使用信号量进行线程同步
'''
import threading
import time
import random

semaphore = threading.Semaphore(0)

def consumer():
	print("conusmer is waiting.")
	semaphore.acquire()		#信号量的计数器为0，阻塞acquire()方法，直到得到另一个线程的通知
	print("Consumer notify: consumed item number %s" % item)

def producer():
	global item
	time.sleep(10)
	item = random.randint(0, 1000)
	print("producer notify: produced item number %s" % item)
	semaphore.release()

if  __name__ == '__main__':
	for i in range(0, 5):
		t1 = threading.Thread(target=producer)
		t2 = threading.Thread(target=consumer)
		t1.start()
		t2.start()
		t1.join()
		t2.join()
	print('program terminated')

'''

#使用条件进行线程同步
'''
from threading import Thread, Condition
import time

items = []
condition = Condition()

class consumer(Thread):

	def __init__(self):
		Thread.__init__(self)

	def consume(self):
		global condition
		global items
		condition.acquire()
		#缓存队列为空，等待
		if len(items) == 0:
			condition.wait()		#wait()会释放锁，等待其他线程notify()后会重新尝试获得锁
			print('Consumer notify: no item to consumer')
		#缓存队列不为空时，消费一个item
		items.pop()
		print("Consumer notify: consumed 1 item")
		print("Consumer notify: items to consumer are" + str(len(items)))

		#缓存队列不满时，通知生产者
		condition.notify()
		condition.release()

	def run(self):
		for i in range(0, 20):
			time.sleep(2)
			self.consume()

class producer(Thread):

	def __init__(self):
		Thread.__init__(self)

	def produce(self):
		global condition
		global items
		condition.acquire()
		#缓存队列满了
		if len(items) == 10:
			condition.wait()	
			print("Producer notify: items producted are " + str(len(items)))
			print("Producer notify: stop the production!")
		#缓存队列没满是，生产一个item
		items.append(1)
		print("Producer notify: total items producted " + str(len(items)))
		#缓存队列不为空时，通知消费者
		condition.notify()
		condition.release()

	def run(self):
		for i in range(1, 20):
			time.sleep(1)
			self.produce()

if __name__ == '__main__':
	producer = producer()
	consumer = consumer()
	consumer.start()
	producer.start()
	consumer.join()
	producer.join()
'''

#一个使用条件的案例

#开3个线程，按照顺序打印‘ABC’ 10次
''''
from threading import Thread, Condition

condition  = Condition()
current = 'A'

class ThreadA(Thread):

	def run(self):
		global current
		for _ in range(10):
			with condition:
				while current != 'A':
					condition.wait()
				print("A")
				current = "B"
				condition.notify_all()

class ThreadB(Thread):

	def run(self):
		global current
		for _ in range(10):
			with condition:
				while current != 'B':
					condition.wait()
				print("B")
				current = "C"
				condition.notify_all()

class ThreadC(Thread):

	def run(self):
		global current
		for _ in range(10):
			with condition:
				while current != 'C':
					condition.wait()
				print("C")
				current = "A"
				condition.notify_all()

if __name__ == '__main__':
	a = ThreadA()
	b = ThreadB()
	c = ThreadC()

	a.start()
	b.start()
	c.start()

	a.join()
	b.join()
	c.join()
'''

#使用事件进行线程同步
'''
from threading import Thread, Event
import time
import random

items = []
event = Event()

class consumer(Thread):

	def  __init__(self, items, event):
		Thread.__init__(self)
		self.items = items
		self.event = event

	def run(self):
		while True:
			time.sleep(2)
			self.event.wait()
			item = self.items.pop()
			print("Consumer notify: %d popped from list by %s" % (item, self.name))

class producer(Thread):

	def __init__(self, items, event):
		Thread.__init__(self)
		self.items = items
		self.event = event

	def run(self):
		global item
		for i in range(100):
			time.sleep(2)
			item = random.randint(0, 256)
			self.items.append(item)
			print("Producer notify: item %d append to list by %s" % (item, self.name))
			print("Producer notify: event set by %s" % self.name)
			self.event.set()	#设置事件内部变量为True，然后通知消费者
			print("produce notify: event cleared by %s " % self.name)
			self.event.clear()

if __name__ == '__main__':
	t1 = producer(items, event)
	t2 = consumer(items, event)
	
	t1.start()
	t2.start()

	t1.join()
	t2.join()
'''

#使用with用法
#可用于Lock、RLock、Condition、Semaphore
'''
import threading
import logging

logging.basicConfig(level=logging.DEBUG, format='(%(threadName)-10s) %(message)s',)

def threading_with(statement):
	with statement:
		logging.debug('%s acquired via with ' % statement)

def threading_not_with(statement):
	statement.acquire()
	try:
		logging.debug('%s acquire directly' % statement)
	finally:
		statement.release()

if __name__ == '__main__':
	lock = threading.Lock()
	rlock = threading.RLock()
	condition = threading.Condition()
	mutex = threading.Semaphore(1)     #信号量为1时，表示互斥
	threading_synchronization_list = [lock, rlock, condition, mutex]

	for statement in threading_synchronization_list:
		t1 = threading.Thread(target=threading_with, args=(statement,))
		t2 = threading.Thread(target=threading_not_with, args=(statement,))

		t1.start()
		t2.start()

		t1.join()
		t2.join()

'''

#使用queue 进行线程通信

from threading import Thread, Event
from queue import Queue
import time
import random

class producer(Thread):

	def __init__(self, queue):
		Thread.__init__(self)
		self.queue = queue

	def run(self):
		for i in range(10):
			item = random.randint(0, 256)
			self.queue.put(item)				#往队列中放一个item 
			print('producer notify: item %d append to queue by %s' % (item, self.name))

class consumer(Thread):

	def __init__(self, queue):
		Thread.__init__(self)
		self.queue = queue

	def run(self):
		while True:
			item =  self.queue.get()			#从队列中删除一个item，并返回
			print('Consumer notify: %d poped from queue by %s' % (item, self.name))
			self.queue.task_done()				#每次item被处理时都需要调用task_done()，标记任务已处理

if __name__ == '__main__':
	queue = Queue()
	t1 = producer(queue)
	t2 = consumer(queue)
	t3 = consumer(queue)
	t4 = consumer(queue)
	
	t1.start()
	t2.start()
	t3.start()
	t4.start()

	t1.join()
	t2.join()
	t3.join()
	t4.join()
















