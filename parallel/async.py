#coding: utf-8
'''
异步编程
'''

#使用concurrent.futures模块
'''
import concurrent.futures
import time

number_list = [x for x in range(11)]

def evaluate_item(x):
    #计算总和
    result_item = count(x)
    return result_item

def count(number):
    for i in range(0, 10000000):
        i = i + 1
    return i * number

if __name__ == "__main__":
    #顺序执行
    start_time = time.time()
    for item in number_list:
        print(evaluate_item(item))
    print("Sequential execution in" + str(time.time() - start_time), "seconds")
    
    #线程池执行
    start_time_1 = time.time()
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(evaluate_item, item) for item in number_list]
        for future in concurrent.futures.as_completed(futures):
            print(future.result())
    print("Thread pool execution in " + str(time.time() - start_time_1), "seconds")
    
    #进程池
    start_time_2 = time.time()
    with concurrent.futures.ProcessPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(evaluate_item, item) for item in number_list]
        for future in concurrent.futures.as_completed(futures):
            print(future.result())
    print("Process pool executionin " + str(time.time() - start_time_2), "seconds")
'''

#使用Asyncio管理事件循环
'''
import asyncio
import datetime
import time

def func_1(end_time, loop):
    print("func_1 called")
    if (loop.time() + 1.0) < end_time:
        loop.call_later(1,  func_2, end_time, loop)
    else:
        loop.stop()
        
def func_2(end_time, loop):
    print("func_2 called")
    if (loop.time() + 1.0) < end_time:
        loop.call_later(1,  func_3, end_time, loop)
    else:
        loop.stop()

def func_3(end_time, loop):
    print("func_3 called")
    if (loop.time() + 1.0) < end_time:
        loop.call_later(1,  func_1, end_time, loop)
    else:
        loop.stop()     

def func_4(end_time, loop):
    print("func_5 called")
    if (loop.time() + 1.0) < end_time:
        loop.call_later(1,  func_4, end_time, loop)
    else:
        loop.stop()
        
loop = asyncio.get_event_loop()

end_loop = loop.time() + 0.9
loop.call_soon(func_1, end_loop, loop)
loop.run_forever()
loop.close()
'''

#使用Asyncio管理协程
'''
import asyncio
import time
from random import randint

@asyncio.coroutine
def StartState():
    print("Start State called \n")
    input_value = randint(0, 1)
    time.sleep(1)
    if input_value == 0:
        result = yield from State2(input_value)
    else:
        result  = yield from State1(input_value)
    print("Resume of the Transition: \nStart State calling " + result)
    
@asyncio.coroutine
def State1(transition_value):
    outputValue = str("State 1 with transition value = %s \n" %  transition_value)
    input_value = randint(0, 1)
    time.sleep(1)
    print("...Evaluation...")
    if input_value == 0:
        result = yield from State3(input_value)
    else:
        result = yield from State2(input_value)
    result = "State 1 calling " + result
    return outputValue + str(result)

@asyncio.coroutine
def State2(transition_value):
    outputValue= str("State 2 with transition value = %s \n" % transition_value)
    input_value = randint(0, 1)
    time.sleep(1)
    print("...Evaluting...")
    if input_value ==  0:
        result = yield from State1(input_value)
    else:
        result = yield from State1(input_value)
    result = "State 2 calling " + result
    return outputValue + str(result)

@asyncio.coroutine
def State3(transition_value):
    outputValue = str("State 3 with transition value = %s \n" % transition_value)
    input_value = randint(0, 1)
    time.sleep(1)
    print("...Evaluting...")
    if input_value == 0:
        result = yield from State1(input_value)
    else:
        result = yield from EndState(input_value)
    result = "State 3 calling" + result
    return outputValue + str(result)

@asyncio.coroutine
def EndState(transition_value):
    outputValue = str("End State with transition value = %s \n" % transition_value)
    print("...Stop Computation...")
    return outputValue

if __name__ == '__main__':
    print("Finite State Machine simulation with Asyncio Coroutine")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(StartState())
'''

#使用Asyncio 控制任务
'''
import asyncio

@asyncio.coroutine
def fact(number):
    f = 1
    for i in range(2, number + 1):
        print("Asyncio.Task: Compute factorial(%s)" % (i))
        yield from asyncio.sleep(1)
        f *= i
    print("Asyncio.Task - factorial(%s) = %s" % (number, f))
    
@asyncio.coroutine
def fib(number):
    a, b = 0, 1
    for i in range(number):
        print("Asyncio.Task: Compute fibonacci (%s)" % (i))
        yield from asyncio.sleep(1)
        a, b = b, a + b
    print("Asyncio.Task - fibonacci(%s) = %s" % (number, a))
    
@asyncio.coroutine
def binomialCoeff(n, k):
    result = 1
    for i in range(1, k+1):
        result = result * (n-i+1) / i
        print("Asyncio.Task: Compute binomialCoeff (%s)" % (i))
        yield from asyncio.sleep(1)
    print("Asyncio.Task - binomialCoeff(%s, %s) = %s" % (n, k, result))
    
if __name__ == '__main__':
    tasks = [asyncio.Task(fact(10)),
             asyncio.Task(fib(10)),
             asyncio.Task(binomialCoeff(20, 10))]
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()
'''

#使用Asyncio和Futures
#python async.py x y

import asyncio
import sys

@asyncio.coroutine
def first_coroutine(future, N):
    """前n个数的和"""
    count = 0
    for i in range(1, N + 1):
        count = count + i
    yield from asyncio.sleep(3)
    future.set_result("first coroutine (sum of N integers) result = " + str(count))

@asyncio.coroutine
def second_coroutine(future, N):
    count = 1
    for i in range(2, N + 1):
        count *= i
    yield from asyncio.sleep(4)
    future.set_result("second coroutine (factorial) result = " + str(count))

def got_result(future):
   print(future.result())

if __name__ == "__main__":
   N1 = int(sys.argv[1])
   N2 = int(sys.argv[2])
   loop = asyncio.get_event_loop()
   future1 = asyncio.Future()
   future2 = asyncio.Future()
   tasks = [
       first_coroutine(future1, N1),
       second_coroutine(future2, N2)]
   future1.add_done_callback(got_result)
   future2.add_done_callback(got_result)
   loop.run_until_complete(asyncio.wait(tasks))
   loop.close()





















