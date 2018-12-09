#! /usr/bin/env python
# -*- coding: utf-8 -*-

'''
如果我们考虑的是，同时服务多个客户端，那么他不算！

如果某一个协程被网络阻塞了，那么整个线程（进程）都被阻塞。
协程本身不能避开阻塞。 任意时刻，只有一个协程在执行。

从执行单元上来看，它的确属于并发。
'''
'''
from greenlet import greenlet
import random,time

# 生产者
def producer():
    while True:
        item=random.randint(0,100)
        print('生产了：',item)
        c.switch(item)   # 切换到消费者，并将item传入消费者
        time.sleep(1)

def consumer():
    while True:
        item=p.switch()   # 切换到生产者，并将item传入生产者
        print('消费了：',item)

p=greenlet(producer)   # 将函数变成协程
c=greenlet(consumer)
c.switch()   # 让消费者先进入暂停状态

'''


'''
虽然，我们有了 基于 epoll 的回调式编程模式，但是却难以使用。

即使我们可以通过配合 生成器协程 进行复杂的封装，以简化编程难度。
但是仍然有一个大的问题： 封装难度大，现有代码几乎完全要重写

gevent，通过封装了 libev（基于epoll） 和 greenlet 两个库。
帮我们做好封装，允许我们以类似于线程的方式使用协程。

以至于我们几乎不用重写原来的代码就能充分利用 epoll 和 协程 威力。

'''


'''gevent服务器'''
'''
import gevent
from gevent import monkey;monkey.patch_socket()  # from gevent.monkey import patch_socket;patch_socket()
import socket

server=socket.socket()
server.bind(('',8888))
server.listen(100)

def recv(con):
    while True:
        data=con.recv(1024)
        if data:
            print('消息是：',data.decode())
            con.send(data)
        else:
            con.close()
            break

while True:
    con,addr=server.accept()
    gevent.spawn(recv,con)  # 生成一个协程

'''



'''
问题一： 协程之间不是能通过switch通信嘛？
    是的，由于 gevent 基于 greenlet，所以可以。

问题二： 那为什么还要考虑通信问题？
    因为 gevent 不需要我们使用手动切换，
    而是遇到阻塞就切换，因此我们不会去使用switch ！

'''


'''gevent通信'''
from gevent.monkey import patch_socket;patch_socket()
import gevent
from gevent.queue import Queue
import random,time

queue=Queue(3)

def producer(queue):
    while True:
        item=random.randint(0,100)
        queue.put(item)
        print('生产了：',item)
        time.sleep(1)

def consumer(queue):
    while True:
        item=queue.get()
        print('消费了：',item)
        time.sleep(1)

p=gevent.spawn(producer,queue)   # 将函数封装成协程，并开始调度
c=gevent.spawn(consumer,queue)
gevent.joinall([p,c])    # 阻塞等待（阻塞就切换协程）

