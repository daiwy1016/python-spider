#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-09-07 23:18:34
# @Author  : 小戴 (408366645@qq.com)
# @Link    : http://www.phpet.com/
# @Version : $Id$

# -*- coding:UTF-8 -*-

from python_lib import BaseCommon
import time
from lxml import etree
import requests
from urllib import request
from bs4 import BeautifulSoup
import sys
import io
import os

import configparser


import win32api
import win32con



def loglist(file,data):
    f = open(file,'a')
    #
    f.write(data+"\n")
    f.close()



win32api.MessageBox(0,'1','2')

exit()

# print(sys.argv[0][sys.argv[0].rfind(os.sep) + 1:-3])
# i=0
# for each_i in range(10):
#     i+=1
#     if i<5:
#         #print(i)
#         continue
#     print(i)
# exit()
# s="1"
# i=int(s)

# print(type(i))
# exit()
#ConfigParser 初始化对象
config = configparser.ConfigParser()
config.read("config.ini", encoding="GBK")

mangacount=config.get("currentManga", "mangacount")
print(mangacount)
config.set("currentChapter", "chaptercount", "69")  #修改db_port的值为69
config.write(open("config.ini", "w"))

print(os.getcwd())



print(config.has_option("currentChapter", "chaptercount") )
exit()


# url='https://www.91hanman.com/page/get/68/414/false'
# headers = {
#                     "User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
#         }
# req = requests.get(url = url,headers = headers,verify=False)
# req.encoding = 'utf-8'
# html = req.text
#html=req.content.decode()
#html=str(req.content,"utf-8")
html ='狐妖小红娘-总300•……我还没动手_韩国漫画'
#sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='gb18030')
bf = BeautifulSoup(html, 'lxml')
#print(bf.prettify('utf-8'))

#print(req.read().decode('utf-8'))
#print(str(bf.title.text).encode('utf-8').decode('utf-8'))
s=bf.text
s1=s.encode('GBK','ignore')
s2=s1.decode('GBK')

# s1=s.encode('GB18030')
# s2=s1.decode('GB18030')
print(s2)
loglist('test.txt',s2)

print("ok!!!")
exit()




url = "http://www.baidu.com/"
req = request.Request(url)
response1 = request.urlopen(req)
html1 = etree.HTML(response1.read())
print("这个是response1: ", response1)#打印出response1是什么鬼
print("这个是type(response1: " , type(response1))#打印出response1的类型
print("这个是type(html1): " , type(html1)) #打印html1的类型
print("这个是html1: " , html1)#打印出response1的用etree解析为html网页元素
#打印网页的文本信息,由于这个response1只能调用一次所以这里会打印出空
print(response1.read().decode())#打印出网页源码的文本信息

print('*'*70)

response2 = requests.get(url)
html2 = etree.HTML(response2.text)
print("这个是response2: ",response2)#打印出response2的内容
print("这个是type(response2): " , type(response2))#打印出response2的类型
print("这个是type(response2.text): " , type(response2.text))#打印出response2用text输出是的类型
print(type(response2.content.decode()))#打印出内容解码的类型
print("这个是type(html2): ", type(html2))#打印出response2用etree解析为网页元素信息的html2的类型
print("这个是html2 :", html2)#打印出response2用etree解析为网页元素信息的html2
#打印网页的文本信息,用resquests有三种方法可以打印出网页的信息,这三种方法打印出来的都一样的
response2.encoding = 'utf-8'#给网页指定编码信息,是为了用text输出网页文本信息的
print(response2.text)#打印出网页的文本信息
print(response2.content.decode())#打印出网页源码的文本信息,这样写是为了避免出现中文乱码
print(str(response2.content,"utf-8"))#打印出网页源码的文本信息,这样写是为了避免出现中文乱码


exit()


# f = open('test.txt','a')
# f.write("c1\n")
# f.close()






# BaseCommon.download(url="http://www.abcaa.com/a/1739/2/1.",filename="1.jpg")
# time.sleep(1)
# print('ok!!!')
for index in range(10):
    index+=10
    print(index)
