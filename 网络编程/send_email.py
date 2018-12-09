#! /usr/bin/env python
# -*- coding: utf-8 -*-

import smtplib
from email.mime.text import MIMEText
#设置服务器所需信息
#163邮箱服务器地址
mail_host = 'smtp.yeah.net'
#163用户名
mail_user = '15******93'
#密码(部分邮箱为授权码)
mail_pass = 'Woaiw*********'
#邮件发送方邮箱地址
sender = '15833436593@yeah.net'
#邮件接受方邮箱地址，注意需要[]包裹，这意味着你可以写多个邮件地址群发
receivers = ['912345454@qq.com']

#设置email信息
content='你好，我是...'
#邮件内容设置
message = MIMEText(content,'plain','utf-8')  #  MIMEText(content, 'html', 'utf-8')
#邮件主题
message['Subject'] = '我的主题主题'
#发送方信息
message['From'] = sender
#接受方信息
message['To'] = receivers[0]

#登录并发送邮件
try:
    smtpObj = smtplib.SMTP()
    #连接到服务器
    smtpObj.connect(mail_host,25)
    #登录到服务器
    smtpObj.login(mail_user,mail_pass)
    #发送   sender 发件人邮箱；to_addrs 邮件接收者地址。多个采用字符串列表['接收地址1','接收地址2','接收地址3',...]单个：'接收地址' ； message 发送的内容
    smtpObj.sendmail(sender,receivers,message.as_string())
    #退出
    smtpObj.quit()
    print('success')
except smtplib.SMTPException as e:
    print('error',e) #打印错误

'''


#!/usr/bin/python3
# smtplib模块主要负责发送邮件：是一个发送邮件的动作，连接邮箱服务器，登录邮箱，发送邮件（有发件人，收信人，邮件内容）。
import smtplib
# email模块主要负责构造邮件：指的是邮箱页面显示的一些构造，如发件人，收件人，主题，正文，附件等
from email.mime.text import MIMEText
from email.header import Header

# =============================
# 定义变量
# =============================
# 第三方 SMTP 服务
mail_host = "smtp.yeah.net"  # 设置服务器
mail_user = "1584522456333@yeah.net"  # 用户名
mail_pass = "Woa3442sdx32"  # 授权码 qq邮箱获取地址：https://jingyan.baidu.com/article/6079ad0eb14aaa28fe86db5a.html

sender = '15353750593@yeah.net'  # 发送邮件的邮箱
to_addrs = ['912456154@qq.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱

# =============================
# 配置邮件内容；参考：https://www.cnblogs.com/yufeihlf/p/5726619.html
# =============================
mail_msg = """
<p>Python 邮件发送测试,此处是正文...</p>
<p><a href="http://www.runoob.com">这是一个链接</a></p>
"""
message = MIMEText(mail_msg, 'html', 'utf-8')
message['From'] = Header("菜鸟教程", 'utf-8')  #发送者
message['To'] = Header("测试", 'utf-8') #接收者

subject = 'Python SMTP 邮件测试'
message['Subject'] = Header(subject, 'utf-8')
# =============================
# 发送邮件配置
# =============================
try:
    smtpObj = smtplib.SMTP()# 实例化SMTP()
    smtpObj.connect(mail_host, 25)  # mail_host 设置服务器；25 为 SMTP 默认端口号
    smtpObj.login(mail_user, mail_pass) # mail_user 发件人用户名；mail_pass 发件人邮箱授权码
    smtpObj.sendmail(sender, to_addrs, message.as_string())# sender 发件人邮箱；to_addrs 邮件接收者地址。多个采用字符串列表['接收地址1','接收地址2','接收地址3',...]单个：'接收地址' ； message 发送的内容
    smtpObj.quit() # 用于结束SMTP会话。
    print("邮件发送成功")
except smtplib.SMTPException:
    print("Error: 无法发送邮件")

'''