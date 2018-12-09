#! /usr/bin/env python
# -*- coding: utf-8 -*-

from multiprocessing import Process
import datetime, time, socket, re,sys
import threading

HTML_ROOT='./static'
WSGI_DIR='./wsgipy'

class HttpServer():
    def __init__(self,application):
        self.application=application
        self.server = socket.socket()
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)   # SO_REUSEADDR  允许套接口和一个已在使用中的地址捆绑  在调用bind()之前设置

    def bind(self,port):
        self.server.bind(('', port))

    def start(self):
        self.server.listen(100)
        while True:
            con, addr = self.server.accept()
            p = Process(target = self.recv, args = (con,))
            p.start()

    def start_response(self,status,headers):
        response_headers="HTTP/1.1"+status+"\r\n"
        for key,value in headers:
            response_headers+="%s:%s\r\n"%(key,value)
        self.response_headers=response_headers

    def recv(self,con):
        data = con.recv(1024)
        print(data.decode())
        request_data = data.splitlines()

        request_data_line = request_data[0]     # GET / HTTP/1.1
        #   匹配  '''GET / HTTP/1.1'''    file_name  为uri
        # 获取路由
        file_name = re.match(r'\w+ +(/[^ ]*) ', request_data_line.decode()).group(1)
        env={
            'PATH_INFO':file_name,
        }
        response_body=self.application(env,self.start_response)
        response = self.response_headers + "\r\n" + response_body
        con.send(response.encode())
        con.close()


# if __name__ == "__main__":
#     sys.path.insert(1,WSGI_DIR)
    # server=HttpServer()
    # server.bind(8000)
    # server.start()
