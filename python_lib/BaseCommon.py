#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-09-09 06:23:33
# @Author  : 小戴 (408366645@qq.com)
# @Link    : http://www.phpet.com/
# @Version : $Id$

from urllib.request import urlretrieve
import os
import time
import pdb
import socket
import logging

def loglist(file,data):
    f = open(file,'a')
    f.write(data+"\n")
    f.close()
def download(url,filename):
    socket.setdefaulttimeout(60)
    #pdb.set_trace() # 运行到这里会自动暂停
    try:
        urlretrieve(url = url,filename = filename)
    except socket.timeout:
        count = 1
        while count <= 5:
            try:
                urlretrieve(url = url,filename = filename)                                                
                break
            except socket.timeout:
                err_info = 'Reloading for %d time'%count if count == 1 else 'Reloading for %d times'%count
                print(err_info)
                count += 1
        if count > 5:
            print("downloading picture fialed!")
    except Exception as e:
        print('捕捉到其他异常')
        logging.exception(e)
        count = 1
        while count <= 3:
            try:
                urlretrieve(url = url,filename = filename)                                                
                break
            except:
                err_info = '捕捉到其他异常:Reloading for %d time'%count if count == 1 else '捕捉到其他异常:Reloading for %d times'%count
                print(err_info)
                count += 1
        if count > 3:
            print("downloading fialed!")

