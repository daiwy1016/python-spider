#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-09-09 06:23:33
# @Author  : 小戴 (408366645@qq.com)
# @Link    : http://www.phpet.com/
# @Version : $Id$

from urllib.request import urlretrieve
import urllib
import os
import time
import pdb
import socket
import logging

def logginconfig():
    logging.basicConfig(level=logging.DEBUG,#控制台打印的日志级别
                    filename='new.log',
                    filemode='a',##模式，有w和a，w就是写模式，每次都会重新写日志，覆盖之前的日志
                    #a是追加模式，默认如果不写的话，就是追加模式
                    format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'#日志格式
                    )


def loglist(file,data,mode='a'):
    f = open(file,mode)
    f.write(data+"\n")
    f.close()
def download(url,filename):
    socket.setdefaulttimeout(60)
    #pdb.set_trace() # 运行到这里会自动暂停
    try:
        opener = urllib.request.build_opener()
        opener.addheaders = [('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
        urllib.request.install_opener(opener)
        #urlretrieve(url = url,filename = filename)
        urllib.request.urlretrieve(url = url,filename = filename)
    except socket.timeout:
        count = 1
        while count <= 5:
            try:
                urlretrieve(url = url,filename = filename)
                break
            except socket.timeout:
                err_info = 'Reloading for %d time'%count if count == 1 else 'Reloading for %d times'%count
                print(err_info)
                print('timeout-url:'+url)
                count += 1
        if count > 5:
            print('url:'+url)
            print("downloading picture fialed!")
    except Exception as e:
        print('other-url1:'+url)
        print('捕捉到其他异常')
        logging.exception(e)
        count = 1
        while count <= 3:
            try:
                #urlretrieve(url = url,filename = filename)
                opener = urllib.request.build_opener()
                opener.addheaders = [('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
                urllib.request.install_opener(opener)
                #urlretrieve(url = url,filename = filename)
                urllib.request.urlretrieve(url = url,filename = filename)
                break
            except:
                err_info = '捕捉到其他异常:Reloading for %d time'%count if count == 1 else '捕捉到其他异常:Reloading for %d times'%count
                print(err_info)
                count += 1
        if count > 3:
            print('other-url2:'+url)
            print("downloading fialed!")

# 对重编码的网址下载图片
# def down(outs, folder_path):
#     global x
#     for out in outs:
#         # 获取新编码的URL地址
#         res = requests.get(out)
#         # 防止被反爬，打开后关闭
#         res.close()
#         bf = BytesIO()
#         bf.write(res.content)
#         img = Image.open(bf)
#         print(f'正在下载第{x}张图片')
#         img.save(folder_path + f"{x}.jpg")
#         x += 1

# 对获取的图片源网址进行重编码
def bianma(results):
    outs = []
    for s in results:
        # 用正则筛选出中文部分
        pattern = re.compile('[\u4e00-\u9fa5]+')
        result = re.search(pattern, s)
        su = result.group(0)
        # 把中文部分重洗编码
        li = urllib.parse.quote(su)
        # 把原URL地址中文部分替换成编码后的
        out = re.sub(pattern, li, s)
        outs.append(out)
    # 对列表进行去重并且按照原来的次序排列
    outs_cp = sorted(set(outs), key=outs.index)
    return outs_cp
# 获取抓取的图片源网址
def crawl(url, header):
    res = requests.get(url, headers=header)
    # 防止被反爬，打开后关闭
    res.close()
    res = res.text
    pattern = re.compile('http.*?apic.*?jpg')
    result = re.findall(pattern, res)
    return result
