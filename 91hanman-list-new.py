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
    base_folder ='F:/py3project/91hanman/'#以/结束
    base_url='https://www.91hanman.com'
    #base_folder ='F:/py3workspace/python-spider/'#以/结束
    manhua_list=[]
    manhua_list.append('https://www.91hanman.com/book/webBookDetail/60=过人')
    manhua_list.append('https://www.91hanman.com/book/webBookDetail/61=从今天开始当城主')
    manhua_list.append('https://www.91hanman.com/book/webBookDetail/62=影帝X影帝')
    manhua_list.append('https://www.91hanman.com/book/webBookDetail/63=快意十三刀')
    manhua_list.append('https://www.91hanman.com/book/webBookDetail/64=废柴特工')
    print(manhua_list)
    for each_manhua_list in manhua_list:
        list_url = []
        each_manhua_list_info = each_manhua_list.split('=')
        base_manga_name=each_manhua_list_info[1]
        base_log=base_folder+base_manga_name+".txt"
        url = each_manhua_list_info[0]
        print(base_manga_name)
        print(url)

        # base_folder ='F:/py3project/91hanman/'
        # #base_folder ='F:/py3workspace/python-spider/'
        # base_url='https://www.91hanman.com'
        # base_manga_name='过人'
        # base_log=base_folder+base_manga_name+".txt"
        if base_manga_name not in os.listdir():
             os.makedirs(base_manga_name)
        # if num == 1:
        #     url = 'view-source:https://www.91hanman.com/book/webBookDetail/69'
        # else:
        #     url = 'http://www.shuaia.net/index_%d.html' % num
        #TODO:
        #url = base_url+'/book/webBookDetail/60'
        headers = {
                "User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
                "Referer": "http://www.google.com/bot.html"
        }
        req = requests.get(url = url,headers = headers)
        req.encoding = 'utf-8'
        html = req.text
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
            # if(count <= 37):
            #     print(count)
            #     continue
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
        os.system('shutdown -s -f -t 59')
