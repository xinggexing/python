#! /usr/bin/env python
# -*- coding: utf-8 -*-



'''

from threading import Thread,current_thread
import time,datetime

def func1(add):
    time.sleep(1)
    print(add)

def func2(add):
    time.sleep(1)
    print(add)
    print(current_thread())


print('开始:',datetime.datetime.now())
t1=Thread(target = func1,args = (123,))
t2=Thread(target = func2,args = (456,))
t1.start()
t2.start()
print(t1.ident)
print(t1.is_alive())
time.sleep(1)
t2.join()
print('结束:',datetime.datetime.now())



from multiprocessing import Process,Manager

mgr=Manager()
lt=mgr.list()

def func1(lt):
    lt.append(111)

def func2(lt):
    lt.append(222)

p1=Process(target = func1,args = (lt,))
p2=Process(target = func2,args = (lt,))
p1.start()
p2.start()
p2.join()
print(lt)

'''





# from queue import Queue
# 线程的
# q=Queue(8)
# q.put(2)
# q.put(9)
# print(q.get())
# # print(q.get())
# # print(q.get())
# q.join()



# from multiprocessing import Manager
# # 进程的
# m=Manager()
# q=m.Queue(4) # 进程的队列
# q.put(22)
# q.put(33)
# print(q.get())




'''

from multiprocessing import Process,Manager

manager=Manager()   # 管理器
sharde_list=manager.list()  # 在公共进程中开启一个list空间，用来进程通信

def func(li):
    li.append('1111')

p=Process(target = func,args = (sharde_list,))
p.start()
p.join()
print(sharde_list)
'''


'''
一般常用的空间类型是：
1.  manager.list()
2.  manager.dict()
3.  manager.Queue()
https://pan.baidu.com/s/1qSdcsVG7lJBGr0lNo9as4A

'''

'''
from threading import Thread,Lock
import datetime
a=0
lock=Lock()
def func1(n):
    global a
    for i in range(n):
        lock.acquire() # 上锁
        a+=1
        lock.release() # 解锁

def func2(n):
    global a
    for i in range(n):
        with lock:   上下文管理器原理
            a-=1

print(datetime.datetime.now())
t1=Thread(target = func1,args = (1000000,))
t2=Thread(target = func2,args = (1000000,))
t1.start()
t2.start()
t1.join()
t2.join()
print(a)
print(datetime.datetime.now())
'''




'''
from threading import Thread
from multiprocessing import Process,Manager
from queue import Queue
import random

# q=Queue(3)
mgr=Manager()
q=mgr.Queue()

def func1(q):
    while True:
        item=random.randint(0,100)
        q.put(item)
        print('put:',item)

def func2(q):
    while True:
        item=q.get()
        print('get:',item)

# t1=Thread(target = func1,args = (q,))
# t2=Thread(target = func2,args = (q,))
# t1.start()
# t2.start()
# t2.join()

p1=Process(target = func1,args = (q,))
p2=Process(target = func2,args = (q,))
p1.start()
p2.start()
p2.join()
'''


'''
from threading import Thread
from queue import Queue
import random
q=Queue(5)
# 生产者
class Producer(Thread):
    def __init__(self,queue):
        super().__init__()
        self.queue=queue

    def run(self):
        while True:
            item=random.randint(0,100)
            self.queue.put(item)
            print('put {}'.format(item))

# 消费者
class Consumer(Thread):
    def __init__(self,queue):
        super().__init__()
        self.queue=queue

    def run(self):
        while True:
            item=self.queue.get()
            print('get {}'.format(item))
            self.queue.task_done() #

p=Producer(q)
c=Consumer(q)
p.start()
c.start()
'''



'''可重复利用的线程'''
'''
from threading import Thread
from queue import Queue
class MyThread(Thread):
    def __init__(self):
        super().__init__()
        self.queue=Queue()
        self.daemon=True # 守护进程
        self.start() # 实例化时直接启动线程

    def run(self):
        while True:
            func,args,kwargs=self.queue.get()
            func(*args,**kwargs)
            self.queue.task_done()     # 调用task_done，计数器-1

    def applay_async(self,func,args=(),kwargs={ }):
        self.queue.put((func,args,kwargs))

    def join(self):
        self.queue.join()

def func():
    print(1111)
p=MyThread()
p.applay_async(func)
p.join()
'''


'''生产者与消费者模式——进程'''
from multiprocessing import Process,Manager
import random

m=Manager()  # 会生成一个公共进程，守护进程
q=m.Queue()
class Producer(Process):
    def __init__(self,queue):
        super().__init__()
        self.queue=queue

    def run(self):
        while True:
            item=random.randint(0,100)
            self.queue.put(item)
            print('put {}'.format(item))


class Consumer(Process):
    def __init__(self,queue):
        super().__init__()
        self.queue=queue

    def run(self):
        while True:
            item=self.queue.get()
            print('get {}'.format(item))
            self.queue.task_done()


p=Producer(q)
c=Consumer(q)
p.start()
c.start()
p.join()  # 前面有守护进程，需要阻塞
c.join()



