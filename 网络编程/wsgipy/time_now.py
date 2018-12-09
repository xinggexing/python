#! /usr/bin/env python
# -*- coding: utf-8 -*-
import datetime



def index(env,start_response):
    '''
    env={
        "Method":"GET",
        "PATH_INFO":"/"
        }
    '''
    status="200 OK"
    headers=[
        ("Content-Type","text/plain")
    ]
    start_response(status,headers)
    return str(datetime.datetime.now())


urls=[
    ('/index',index),
]

