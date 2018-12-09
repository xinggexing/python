#! /usr/bin/env python
# -*- coding: utf-8 -*-

from multiprocessing import Process
import datetime, time, socket, re,sys
import threading

HTML_ROOT='./static'
WSGI_DIR='./wsgipy'

class HttpServer(object):
    def __init__(self):
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
        file_name = re.match(r'\w+ +(/[^ ]*) ', request_data_line.decode()).group(1)  # 获取路由

        # 动态资源  py文件
        if file_name.endswith('.py'):
            try:
                module=__import__(file_name[1:-3])
            except Exception:
                self.response_headers="HTTP/1.1 404 Not Found\r\n"
                response_body="Not Found"
            else:
                env={}
                response_body=module.application(env,self.start_response)
            response = self.response_headers + "\r\n" + response_body
        else:


            if file_name == '/':
                file_name = '/index.html'

                # 不存在的页面，返回404
            try:
                file = open(HTML_ROOT + file_name, 'rb')
            except Exception as e:
                response_line = "HTTP/1.1 404 Not Found\r\n"
                response_headers = "Server: My Server\r\n"
                response_body="Not Found"
            else:
                file_data = file.read()
                file.close()

                response_line = "HTTP/1.1 200 OK\r\n"
                response_headers = "Server: My Server\r\n"
                # response_body="hello world <br/> hello world"
                response_body = file_data.decode()
            response = response_line + response_headers + "\r\n" + response_body
        con.send(response.encode())
        con.close()


if __name__ == "__main__":
    sys.path.insert(1,WSGI_DIR)
    server=HttpServer()
    server.bind(8000)
    server.start()
