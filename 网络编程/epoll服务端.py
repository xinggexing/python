#! /usr/bin/env python
# -*- coding: utf-8 -*-


'''非阻塞'''
'''
import selectors
import socket

server=socket.socket()
server.setblocking(False)   # 一定要在bind、listen之前
server.bind(('',8888))
server.listen(22)
all_con=[]  # 存储用户

while True:
    try:
        con,addr=server.accept()
        con.setblocking(False)
        all_con.append(con)
    except BlockingIOError:
        pass
    
    tem_con=all_con[:]
    
    while True:
        try:
            for conn in tem_con:
                data=conn.recv(1024)
                if data:
                    print(data.decode())
                    conn.send(data)
                else:
                    conn.close()
                    all_con.remove(conn)
        except BlockingIOError:
            pass

'''

'''IO多路复用'''
import selectors
import socket

# 会根据操作系统决定用epoll还是selectors
# selector=selectors.DefaultSelector()
selector=selectors.EpollSelector()
server=socket.socket()
server.bind(('',8888))
server.listen(22)

def recv(con):
    data=con.recv(1024)
    if data:
        print(data.decode())
        con.send(data)
    else:
        con.close()
        selector.unregister(con)  # 取消注册事件

def _accept(server):
    con,addr=server.accept()
    selector.register(con,selectors.EVENT_READ,recv)


selector.register(server,selectors.EVENT_READ,_accept)  # （套接字 ， 可读事件 ， 回调函数名）

while True:
    events=selector.select()
    '''
    [(SelectorKey(fileobj=<socket.socket fd=4, family=AddressFamily.AF_INET, type=SocketKind.SOCK_STREAM, proto=0, laddr=('0.0.0.0', 8888)>, fd=4, events=1, data=<function _accept at 0x7f4740a570d0>), 1)]
    
    fileobj 对等连接套接字    data 回调函数
    '''
    # print(events)
    for key,_ in events:
        callback=key.data
        callback(key.fileobj)