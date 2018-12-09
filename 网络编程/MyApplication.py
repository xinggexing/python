#! /usr/bin/env python
# -*- coding: utf-8 -*-


import datetime
from MyServer import HttpServer


class Application:
    '''路由'''
    def __init__(self,urls):
        self.urls=urls

    # 类实例像函数一样调用
    def __call__(self, env,start_response):
        # env = {
        #     "Method": "GET",
        #     "PATH_INFO": "/"
        # }
        # 获取路径
        path=env.get('PATH_INFO','/')
        if path.startswith('/statics'):
            file_name=path[8:]
            # 文件是否存在
            try:
                file = open('./statics' + file_name, 'rb')
            except Exception as e:
                status = "404 Not Found"
                headers = []
                start_response(status,headers)
                return 'not found'   # response_body
            else:
                file_data = file.read()
                file.close()
                status = "200 OK"
                headers = []
                start_response(status, headers)
                # response_body="hello world <br/> hello world"
                return file_data.decode()

        # self.urls = ('/',index)
        for url,handler in self.urls:
            if path==url:
                return handler(env,start_response)

        # 路由不存在则 没找到
        status = "404 Not Found"
        headers = []
        start_response(status, headers)
        return 'not found'


def index(env,start_response):
    status="200 OK"
    headers=[
        ("Content-Type","text/plain")
    ]
    start_response(status,headers)
    return str(datetime.datetime.now())


if __name__=='__main__':
    urls=[
        ('/',index),
    ]
    app=Application(urls)
    http_server=HttpServer(app)
    http_server.bind(8000)
    http_server.start()
