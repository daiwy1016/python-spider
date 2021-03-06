# -*- coding:UTF-8 -*-
from bs4 import BeautifulSoup
from urllib.request import urlretrieve
import requests
import os
import time
import pdb
import socket
import ssl
#引入自定义函数
from python_lib import BaseCommon

if __name__ == '__main__':

    #base_folder ='F:/py3project/91hanman/'#以/结束 home
    base_folder ='F:/py3workspace/python-spider/'#以/结束 company
    base_url='https://lieqiman.com'
    #定义一组
    manhua_list=[]
    # manhua_list.append('daxueshiyou=/mh/xe/75.html')
    # manhua_list.append('chongfanquantan=/mh/xe/76.html')
    # manhua_list.append('jieyouzhentanshe=/mh/xe/77.html')
    # manhua_list.append('fanchaqinglv=/mh/xe/78.html')
    # manhua_list.append('geqiangsuoai=/mh/xe/79.html')
    # manhua_list.append('hongseyinji=/mh/xe/80.html')
    # manhua_list.append('jinpaizuoqujia=/mh/xe/81.html')
    manhua_list.append('maopaihuizhang=/mh/xe/82.html')
    manhua_list.append('yaotaodianzhang=/mh/xe/83.html')
    manhua_list.append('buliangfangdong=/mh/xe/84.html')
    manhua_list.append('shuangchongzhangfu=/mh/xe/85.html')
    print(manhua_list)
    print(len(manhua_list))
    #exit()
    for each_manhua_list in manhua_list:
        list_url = []
        each_manhua_list_info = each_manhua_list.split('=')
        base_manga_name=each_manhua_list_info[0]
        base_log=base_folder+base_manga_name+".txt"
        url = base_url+each_manhua_list_info[1]
        print(base_manga_name)
        print(url)

        # base_manga_name='aishangnanguimi'
        # base_log=base_folder+base_manga_name+".txt"
        # url = base_url+'/mh/xe/20.html'
        if base_manga_name not in os.listdir():
             os.makedirs(base_manga_name)
        # if num == 1:
        #     url = 'view-source:https://www.91hanman.com/book/webBookDetail/69'
        # else:
        #     url = 'http://www.shuaia.net/index_%d.html' % num
        #TODO:
        #url = base_url+'/mh/xe/20.html'
        headers = {
                "User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
                "Referer": "http://www.google.com/bot.html"
        }
        ssl._create_default_https_context = ssl._create_unverified_context
        req = requests.get(url = url,headers = headers,verify=False,stream=True)
        req.encoding = 'gbk'
        html = req.text
        #过滤空格
        html=html.replace('&nbsp;', '')
        bf = BeautifulSoup(html, 'lxml')

        #简介
        about = bf.find_all('div',class_='wikicon')
        about_2 = BeautifulSoup(str(about), 'lxml')
        [s.extract() for s in about_2("a")]#去除指定标签
        [s.extract() for s in about_2("strong")]#去除指定标签
        #pdb.set_trace()
        about_3 = about_2.find_all('p')
        #print(str(about_3).encode('utf-8'))
        #print(len(about_3))
        #pdb.set_trace()
        #print(about_2.original_encoding)
        c=0
        for each_about_3 in about_3:
            # c+=1
            # print(c)
            # print(each_about_3.get_text())
            # print(type(each_about_3.get_text()))
            print(each_about_3.get_text().strip()=='')
            if each_about_3.get_text().strip()=='':
                continue
            print(each_about_3.get_text())
            BaseCommon.loglist(base_log,'简介:'+each_about_3.get_text())
        #exit();
        #列表
        targets_url = bf.find_all('div',class_='sections')
        for each_url in targets_url:
            #pdb.set_trace() # 运行到这里会自动暂停
            bf_2 = BeautifulSoup(str(each_url), 'lxml')
            [s.extract() for s in bf_2("p")]#去除指定标签
            targets_url_2 = bf_2.find_all('a')
            for each_url_2 in targets_url_2:
                print(each_url_2.get('href'))
                print(each_url_2.get_text())
                #pdb.set_trace()
                BaseCommon.loglist(base_log,each_url_2.get_text() + '=' + base_url +each_url_2.get('href'))
                list_url.append(each_url_2.get_text() + '=' + base_url +each_url_2.get('href'))

            #pdb.set_trace() # 运行到这里会自动暂停

            # for each in targets_url:
            #     list_url.append(each.img.get('alt') + '=' + each.get('href'))

        print('连接采集完成')
        print(list_url)
        print(len(list_url))

        count=0
        status_count=0
        if base_manga_name=='maopaihuizhang':
            status_count=65
        for each_img in list_url:
            #pdb.set_trace()
            img_info = each_img.split('=')
            target_url = img_info[1]
            filename = img_info[0]


            count +=1
            if(count < status_count):
                print(count)
                continue

            folder=base_folder+base_manga_name+'/'+str(count)
            #pdb.set_trace()
            print(os.path.exists(folder));
            if os.path.exists(folder) ==  False:
                if folder not in os.listdir():
                    os.makedirs(folder)
            #pdb.set_trace() # 运行到这里会自动暂停

            print('下载：' + filename)
            headers = {
                "User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
                "Referer": "http://www.google.com/bot.html"
            }
            img_req = requests.get(url = target_url,headers = headers,verify=False,stream=True)
            img_req.encoding = 'utf-8'
            img_html = img_req.text
            img_bf_1 = BeautifulSoup(img_html, 'lxml')
            img_url = img_bf_1.find_all('div', class_='detailcontent1')
            img_bf_2 = BeautifulSoup(str(img_url), 'lxml')#str 返回一个字符串 把对象转换字符串
            img_bf_3 =img_bf_2.find_all('img')


            #img_bf_3 =img_bf_2.find_all('img')
            i=0
            for each_img_2 in img_bf_3:
                i += 1
                #img_bf_4 = BeautifulSoup(str(each_img_2), 'lxml')#str 返回一个字符串 把对象转换字符串
                img_url = each_img_2.get('src')
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
