#! /usr/bin/env python
# -*- coding: utf-8 -*-

'''

'''



'''进程服务器'''
'''
from multiprocessing import Process
import datetime,time,socket
import threading


server=socket.socket()
server.bind(('',8888))
server.listen(22)

def recv(con):
    while True:
        data=con.recv(1024)
        if data:
            print(data.decode())
            con.send(data)
        else:
            con.close()
            break


while True:
    con,addr=server.accept()
    p=Process(target = recv,args = (con,))
    p.start()

'''



# print('out start %s'%datetime.datetime.now())
#
# def aa():
#     print('in start %s'%datetime.datetime.now())
#     time.sleep(4)
#     print('in close %s' % datetime.datetime.now())
#
# process= Process(target = aa)
# process.start()
# time.sleep(4)
#
#
# print('out close %s'%datetime.datetime.now())




'''线程服务器'''
import threading,socket

server=socket.socket()
server.bind(('',8888))
server.listen(22)

def recv(con):
    while True:
        data=con.recv(1024)
        if data:
            print(data.decode())
            con.send(data)
        else:
            con.close()
            break


while True:
    con,addr=server.accept()
    t=threading.Thread(target = recv,args = (con,))
    t.start()
