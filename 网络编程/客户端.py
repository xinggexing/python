#! /usr/bin/env python
# -*- coding: utf-8 -*-

import socket

client=socket.socket()
client.connect(('127.0.0.1',8888))

while True:
    data=input('>>')
    client.send(data.encode())
    msg=client.recv(1024)
    # print(msg)
