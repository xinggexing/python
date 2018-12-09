#! /usr/bin/env python
# -*- coding: utf-8 -*-
''''''

'''
传输模型与套接字：
    传输模型：
        七层模型：
            应用层
            表示层
            会话层
            网络层
            传输层
            链路层
            物理层
            
        四层模型：
            应用层
            传输层：
                TCP：
                    可靠、有连接的、一对一连接、面向字节流服务、速度慢
                udp：
                    不可靠、无连接、可一对一、多、多对多连接  、面向报文服务、速度快
            网络层
            数据链路层
            
        tcp协议： 传输控制协议
            建立连接（三次握手）：
                     第一次握手：建立连接时，客户端A发送SYN包(SYN=j)到服务器B，并进入SYN_SEND状态，等待服务器B确认
                     第二次握手：服务器B收到SYN包，必须确认客户A的SYN(ACK=j+1)，同时自己也发送一个SYN包(SYN=k)，即SYN+ACK包，此时服务器B进入SYN_RECV状态。
                     第三次握手：客户端A收到服务器B的SYN＋ACK包，向服务器B发送确认包ACK(ACK=k+1)，此包发送完毕，客户端A和服务器B进入ESTABLISHED状态，完成三次握手。
                     
            数据传输
            断开连接（四次挥手）：
                    （1） TCP客户端发送一个FIN，用来关闭客户到服务器的数据传送。
                    （2） 服务器收到这个FIN，它发回一个ACK，确认序号为收到的序号加1。和SYN一样，一个FIN将占用一个序号。
                    （3） 服务器关闭客户端的连接，发送一个FIN给客户端。
                    （4） 客户端发回ACK报文确认，并将确认序号设置为收到序号加1
                    
            
        ip地址跟端口：
            port： 0 - 65535
            
    套接字：    源ip地址和目的ip地址以及源端口号和目的端口号的组合     
                socket = ip address + tcp/udp + port    
        三种套接字：
            客户端套接字
            监听套接字
            对等连接套接字
        import socket
        server=socket.socket()
        server.bind(('',8888))
        server.listen(100)
        con,addr=server.accept()  # 会阻塞
        data=con.recv(1024)  # 会阻塞
        con.send(data)
        con.close()
        server.close()
    
非阻塞套接字与IO多路复用：
    非阻塞套接字：
        server.setblocking(False)
        异常处理  
        代码重排
        避开阻塞
        资源浪费
        吃满cpu
        
    IO多路复用：
        epoll
        相当于把监听任务交给操作系统
        惰性：自己查询
        回调事件：自己调用
        注册事件：把普通套接字阻塞的两个地方都注册为触发事件 
        import selectors
        selector=selectors.EpollSelector()
        selector.register(server,selectors.EVENT_READ,_accept) 
                           参数                        函数
        events=selector.select()
    
    
多进程多线程：
    线程：共享内存，是程序执行的最小单元
    进程：独立内存
    并行：
        真正一起执行
    并发：
        看上去一起执行
    多进程并行：
        多个cpu
        p=multiprocessing.Process(target=func,args=(con,))
    多线程并发：
        全局解析器锁（GIL）
        轮询调度
        遇到阻塞就切换
    并发服务器：
        来一个客户，就扔到一个进程/线程里面，避开阻塞
    其他操作：
        等待结束  join
        当前进程/线程   current_process() / current_thread()
        中止进程  p.terminate()
    标识：
        进程/线程    p.pid  /   t.ident
        进程/线程名（name=None）
        生存状态（三种）：     p.is_alive（）
    守护模式：
        主进程/线程结束了，守护进程/线程就跟着结束
        daemon=True
    面向对象化：
        继承
        重写__init__
        重写run：
            p.start()--> run() --> target

并发通信：
    进程通信：
        内存空间独立
        manager=Manager()   # 生成一个公共的守护进程
        manager.list()    .dict()/.Queue()   # 生成一个公共空间   
    线程通信：
        内存空间共享
        资源竞争问题
        互斥锁
    安全队列：
        先入先出（FIFO）
        Queue（3）
        put（）
        get（）
        task_done()  # 计数器
        join()   # 等待结束
    生产者与消费者：
        生产者：存数据
        消费者：取数据
        面向对象化
        用来完成通信
        
进程池与线程池：
    线程的重复利用：
        主线程当成生产者
        子线程当成消费者
    线程池实现：
        多个可重复利用的线程
    内置池：
        线程池：multiprocessing.pool.ThreadPool
        进程池：multiprocessing.Pool
        
            p=Pool()
            p.apply_async(func,args=())
            p.close()
            p.join()
    并发服务器：
        进程池
        线程池
        避开阻塞

协程
'''
