#! /usr/bin/env python
# -*- coding: utf-8 -*-


'''
import socket
import selectors

select=selectors.EpollSelector()
# select1=selectors.DefaultSelector()
server=socket.socket()
server.bind(('',8888))
server.listen(100)

def recv(con):
    data=con.recv(1024)
    if data:
        print('消息：{}'.format(con))
        con.send(data)
    else:
        con.close()
        select.unregister(con)


def accept(server):
    # con,addr=server.accept()
    con=server.accept()
    print(con)
    select.register(con[0],selectors.EVENT_READ,recv)


select.register(server,selectors.EVENT_READ,accept)

while True:
    events=select.select()
    # print(events)
    for key,_ in events:
        callable=key.data
        fileobj=key.fileobj
        callable(fileobj)


'''
'''
from multiprocessing import Process
import time,datetime

def func1(add):
    time.sleep(1)
    print(add)

def func2(add):
    time.sleep(1)
    print(add)

print('开始:',datetime.datetime.now())
p1=Process(target = func1,args = (123,))
p2=Process(target = func2,args = (456,))
p1.daemon=True
p2.daemon=True
p1.start()
p2.start()

# p2.join()
print('结束:',datetime.datetime.now())



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
        q.task_done()

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


#   -
from threading import Thread
from multiprocessing import Process,Manager
from queue import Queue
import random

mgr=Manager()
q=mgr.Queue()

class producer(Process):
    def __init__(self,queue):
        super().__init__()
        self.queue=queue

    def run(self):
        while True:
            item=random.randint(0,100)
            self.queue.put(item)
            print('put:', item)


class consumer(Process):
    def __init__(self,queue):
        super().__init__()
        self.queue=queue

    def run(self):
        while True:
            item=self.queue.get()
            print('get:',item)
            self.queue.task_done()


p=producer(q)
c=consumer(q)
p.start()
c.start()
c.join()




# - --  - - -- -
from threading import Thread
from queue import Queue

class MyThread(Thread):
    def __init__(self):
        super().__init__()
        self.queue=Queue()
        self.daemon=True
        self.start()

    def run(self):
        while True:
            func,args,kwargs=self.queue.get()
            func(*args,**kwargs)
            self.queue.task_done()

    def applay_async(self, func,args=(),kwargs={}):
        self.queue.put((func,args,kwargs))

    def join(self, timeout=None):
        self.queue.join()


def func():
    print(33333)

t=MyThread()
t.applay_async(func)
t.join()





from multiprocessing import Pool,cpu_count
from multiprocessing.pool import ThreadPool
import socket

server=socket.socket()
server.bind(('',8888))
server.listen(100)

def recv(con):
    while True:
        data=con.recv(1024)
        if data:
            print('...',data.decode())
            con.send(data)
        else:
            con.close()
            break


def conn(server):
    t=ThreadPool(3)
    while True:
        con,addr=server.accept()
        t.apply_async(recv,(con,))

p=Pool(cpu_count())
for i in range(cpu_count()):
    p.apply_async(conn,(server,))
p.close()
p.join()


'''



