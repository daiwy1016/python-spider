# -*- coding:UTF-8 -*-
from bs4 import BeautifulSoup
from urllib.request import urlretrieve
import requests
import os
import time
import pdb
import socket

from python_lib import BaseCommon


if __name__ == '__main__':

    list_url = []
    base_folder ='F:/py3project/91hanman/'
    #base_folder ='F:/py3workspace/python-spider/'
    base_url='https://www.91hanman.com'
    base_manga_name='ouran'
    base_log=base_folder+base_manga_name+".txt"
    if base_manga_name not in os.listdir():
         os.makedirs(base_manga_name)
    for num in range(1,2):
        # if num == 1:
        #     url = 'view-source:https://www.91hanman.com/book/webBookDetail/69'
        # else:
        #     url = 'http://www.shuaia.net/index_%d.html' % num
        #TODO:
        url = base_url+'/book/webBookDetail/33'
        # headers = {
        #         "User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
        #         "Referer": "http://www.google.com/bot.html"
        # }
        headers = {
                "User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
        }
        #pdb.set_trace() # 运行到这里会自动暂停
        req = requests.get(url = url,headers = headers,stream=True)
        req.encoding = 'utf-8'
        html = req.text
         #过滤
        html=html.replace('•……', '')
        bf = BeautifulSoup(html, 'lxml')
        targets_url = bf.find_all(class_='detail-chapters-list-item')
        for each_url in targets_url:
            #pdb.set_trace() # 运行到这里会自动暂停
            bf_2 = BeautifulSoup(str(each_url), 'lxml')
            print(bf_2.a.get('href'))
            print(bf_2.a.span.span.get_text())
            BaseCommon.loglist(base_log,bf_2.a.span.span.get_text() + '=' + base_url +bf_2.a.get('href'))
            list_url.append(bf_2.a.span.span.get_text() + '=' + base_url +bf_2.a.get('href'))

        #pdb.set_trace() # 运行到这里会自动暂停

        # for each in targets_url:
        #     list_url.append(each.img.get('alt') + '=' + each.get('href'))

    print('连接采集完成')
    print(list_url)
    print(len(list_url))

    count=0
    for each_img in list_url:
        #pdb.set_trace()
        count +=1
        if(count < 46):
            print(count)
            continue
        folder=base_folder+base_manga_name+'/'+str(count)
        #pdb.set_trace()
        print(os.path.exists(folder));
        if os.path.exists(folder) ==  False:
            if folder not in os.listdir():
                os.makedirs(folder)
        #pdb.set_trace() # 运行到这里会自动暂停
        img_info = each_img.split('=')
        target_url = img_info[1]
        filename = img_info[0]
        print(str(count)+'下载：' + filename)
        headers = {
            "User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
            "Referer": "http://www.google.com/bot.html"
        }
        img_req = requests.get(url = target_url,headers = headers)
        img_req.encoding = 'utf-8'
        img_html = img_req.text
        img_bf_1 = BeautifulSoup(img_html, 'lxml')
        img_url = img_bf_1.find_all('div', class_='page-img-list')
        img_bf_2 = BeautifulSoup(str(img_url), 'lxml')#str 返回一个字符串 把对象转换字符串
        img_bf_3 =img_bf_2.find_all('div', class_='nav-chapter-new')


        #img_bf_3 =img_bf_2.find_all('img')
        i=0
        for each_img_2 in img_bf_3:
            i += 1
            img_bf_4 = BeautifulSoup(str(each_img_2), 'lxml')#str 返回一个字符串 把对象转换字符串
            img_url = img_bf_4.div.img.get('data-original')
            # if 'images' not in os.listdir():
            #     os.makedirs('images')
            #print(str(i).zfill(2))
            #print(folder+"/"+str(i).zfill(2) + '.jpg')
            #pdb.set_trace() # 运行到这里会自动暂停
            if os.path.exists(folder+"/"+str(i).zfill(2) + '.jpg') ==  False:
                BaseCommon.download(url = img_url,filename = folder+"/"+str(i).zfill(2) + '.jpg')
                time.sleep(1)


    print('下载完成！')
    #os.system('shutdown -s -f -t 59')
