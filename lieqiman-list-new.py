# -*- coding:UTF-8 -*-
from bs4 import BeautifulSoup
from urllib.request import urlretrieve
import requests
import os
import time
import pdb
import socket
import ssl
import sys
import configparser
#引入自定义函数
from python_lib import BaseCommon

if __name__ == '__main__':

    #base_folder ='F:/py3project/91hanman/'#以/结束 home
    #base_folder ='F:/py3workspace/python-spider/'#以/结束 company
    base_folder = os.getcwd()+"\\"
    base_url='https://lieqiman.com'
    base_config_file=base_folder+'\\'+sys.argv[0][sys.argv[0].rfind(os.sep) + 1:-3]+'.ini'
    #判断配置文件是否存在 不存在建立
    if os.path.exists(base_config_file) ==  False:
        BaseCommon.loglist(base_config_file,"")
    print(base_config_file)
    #定义一组
    manhua_list=[]
    manhua_list.append('jiatingjiaoshi=/mh/xe/97.html')
    manhua_list.append('mimiriji=/mh/xe/98.html')
    manhua_list.append('zhanjurensheng=/mh/xe/99.html')
    manhua_list.append('guiazhangxuemei=/mh/xe/100.html')
    manhua_list.append('renxingqianqi=/mh/xe/101.html')
    manhua_list.append('zhouyenanyou=/mh/xe/102.html')
    manhua_list.append('natianxiatian=/mh/xe/103.html')
    manhua_list.append('xuanze=/mh/xe/105.html')
    manhua_list.append('chulian=/mh/xe/106.html')
    manhua_list.append('chuanyuemeishijia=/mh/xe/107.html')
    manhua_list.append('wodejiemei=/mh/xe/108.html')
    print(manhua_list)
    print(len(manhua_list))
    manhua_list_count=0
    #ConfigParser 初始化对象
    config = configparser.ConfigParser()
    config.read(base_config_file, encoding="GBK")
    #exit()
    for each_manhua_list in manhua_list:
        manhua_list_count +=1

        list_url = []
        each_manhua_list_info = each_manhua_list.split('=')
        base_manga_name=each_manhua_list_info[0]
        base_log=base_folder+base_manga_name+".txt"
        url = base_url+each_manhua_list_info[1]
        print(base_manga_name)
        print(url)

        if not config.has_section('current'):  # 检查是否存在section
            config.add_section('current')
            config.set('current', "mangacount", '0')  #修改
            config.write(open(base_config_file, "w"))
        #获取当前第几个漫画
        manhua_list_count_curr= int(config.get('current', "mangacount"))
        print(manhua_list_count_curr)
        if(manhua_list_count < manhua_list_count_curr):
            print(manhua_list_count)
            continue
        #保存配置
        config.set('current', "mangacount", str(manhua_list_count))  #修改
        config.write(open(base_config_file, "w"))

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
        #网页下载太长 需要加入参数 stream=True 来判断完整性下载
        req = requests.get(url = url,headers = headers,stream=True,verify=False)
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

                #忽略特殊编码
                chaptername=each_url_2.get_text()
                chaptername_1=chaptername.encode('GBK','ignore')
                chaptername_2=chaptername_1.decode('GBK')
                print(chaptername_2)
                #pdb.set_trace()
                BaseCommon.loglist(base_log,chaptername_2 + '=' + base_url +each_url_2.get('href'))
                list_url.append(chaptername_2 + '=' + base_url +each_url_2.get('href'))

            #pdb.set_trace() # 运行到这里会自动暂停

            # for each in targets_url:
            #     list_url.append(each.img.get('alt') + '=' + each.get('href'))

        print('连接采集完成')
        print(list_url)
        print(len(list_url))

        count=0
        if not config.has_section(base_manga_name):  # 检查是否存在section
            config.add_section(base_manga_name)
            config.set(base_manga_name, "chaptercount", '0')  #修改
            config.write(open(base_config_file, "w"))
        #获取当前章节
        if not config.has_option(base_manga_name, "chaptercount"):
            config.set(base_manga_name, "chaptercount", '0')  #修改
            config.write(open(base_config_file, "w"))
        manhua_chapter_count_curr= int(config.get(base_manga_name, "chaptercount"))
        for each_img in list_url:
            #pdb.set_trace()
            count +=1
            if(count < manhua_chapter_count_curr):
                print(count)
                continue
            config.set(base_manga_name, "chaptercount", str(count))  #修改
            config.write(open(base_config_file, "w"))
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
            print('下载：' + filename)
            headers = {
                "User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
                "Referer": "http://www.google.com/bot.html"
            }
            img_req = requests.get(url = target_url,headers = headers,verify=False)
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
                else:
                    print('图片已存在跳过'+str(i))
    print('下载完成！')
    os.system('shutdown -s -f -t 59')
