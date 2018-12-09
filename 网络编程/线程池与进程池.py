#! /usr/bin/env python
# -*- coding: utf-8 -*-

'''线程池的简单实现'''
# from queue import Queue
# from threading import Thread,current_thread
# class ThreadPool(object):
#     def __init__(self,n):
#         self.queue=Queue()
#         for i in range(n):
#             Thread(target = self.func,daemon = True).start()
#
#     def func(self):
#         while True:
#             item=self.queue.get()
#             item()
#             print(current_thread())
#             self.queue.task_done()
#
#     def applay_async(self,item):
#         self.queue.put(item)
#
#     def join(self):
#         self.queue.join()
#
#
# def func():
#     print(111)
#
# t=ThreadPool(5)
# t.applay_async(func)
# t.applay_async(func)
# t.join()  # 等待子线程结束



'''内置进程池'''
# from multiprocessing import Pool
# def func():
#     print(111)
#
# p=Pool()
# p.apply_async(func)
# p.close()        # 关闭提交任务
# p.join()



'''内置线程池'''
# from multiprocessing.pool import ThreadPool
# def func():
#     print(111)
#
# t=ThreadPool()
# t.apply_async(func)
# t.close()
# t.join()



'''进程池实现并发服务器'''
# from multiprocessing import Pool,cpu_count
# import socket
# server=socket.socket()
# server.bind(('',8888))
# server.listen(30)
#
# def recv(con,addr):
#     while True:
#         data=con.recv(1024)
#         if data:
#             print('来自{}的消息:{}'.format(addr,data.decode()))
#             con.send(data)
#         else:
#             con.close()
#             break
#
# p=Pool(cpu_count())
# while True:
#     con,addr=server.accept()
#     p.apply_async(recv,args=(con,addr))



'''线程池实现并发服务器'''
# from multiprocessing.pool import ThreadPool
# import socket
# server=socket.socket()
# server.bind(('',8888))
# server.listen(100)
#
# def recv(con,addr):
#     while True:
#         data=con.recv(1024)
#         if data:
#             print('来自{}的信息：{}'.format(addr,data.decode()))
#             con.send(data)
#         else:
#             con.close()
#             break
#
#
# t=ThreadPool(5)
# while True:
#     con,addr=server.accept()
#     t.apply_async(recv,args=(con,addr))




'''进程池和线程池来实现并发服务器'''
from multiprocessing import Pool,cpu_count
from multiprocessing.pool import ThreadPool
import socket
server=socket.socket()
server.bind(('',8888))
server.listen(100)

def recv(con,addr):
    while True:
        data=con.recv(1024)
        if data:
            con.send(data)
            print('来自{}的信息：{}'.format(addr,data.decode()))
        else:
            con.close()
            break


def conn(server):
    t = ThreadPool(4)     # 每个进程4个线程
    while True:
        con,addr=server.accept()
        print('客户端{}已连上'.format(addr))
        t.apply_async(recv,args = (con,addr))


p=Pool(cpu_count())
for i in range(cpu_count()):
    p.apply_async(conn,args=(server,))
p.close()
p.join()  # 等待子进程结束


