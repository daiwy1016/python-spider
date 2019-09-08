#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-09-07 23:18:34
# @Author  : 小戴 (408366645@qq.com)
# @Link    : http://www.phpet.com/
# @Version : $Id$

# -*- coding:UTF-8 -*-
from bs4 import BeautifulSoup
from urllib.request import urlretrieve
import requests
import os
import time
import pdb
import socket

import ssl


# f = open('test.txt','a')
# f.write("c1\n")
# f.close()
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
    except:
        print('捕捉到其他异常')
        

download(url="http://www.abcaa.com/a/1739/2/1.",filename="1.jpg")
print('ok!!!')