# -*- coding:UTF-8 -*-
from bs4 import BeautifulSoup
from urllib.request import urlretrieve
import requests
import os
import time
import pdb
import socket
import configparser
import sys

from python_lib import BaseCommon


if __name__ == '__main__':
    #base_folder ='F:/py3project/91hanman/'#以/结束
    #base_folder ='F:/py3workspace/python-spider/'#以/结束
    base_folder = os.getcwd()+"\\"
    base_url='https://www.91hanman.com'
    base_config_file=base_folder+'\\'+sys.argv[0][sys.argv[0].rfind(os.sep) + 1:-3]+'.ini'
    #判断配置文件是否存在 不存在建立
    if os.path.exists(base_config_file) ==  False:
        BaseCommon.loglist(base_config_file,"")
        #BaseCommon.loglist(base_config_file,"[currentManga]"+"\n"+"mangacount = 0"+"\n"+"[currentChapter]"+"\n"+"chaptercount = 0"+"\n")
    
    print(base_config_file)
    
    manhua_list=[]
    manhua_list.append('https://www.91hanman.com/book/webBookDetail/77=斗罗大陆4终极斗罗')
    manhua_list.append('https://www.91hanman.com/book/webBookDetail/425=英雄再临')
    manhua_list.append('https://www.91hanman.com/book/webBookDetail/556=铁姬钢兵')
    manhua_list.append('https://www.91hanman.com/book/webBookDetail/260=百层塔')
    manhua_list.append('https://www.91hanman.com/book/webBookDetail/265=尸兄')
    manhua_list.append('https://www.91hanman.com/book/webBookDetail/269=东邻西厢')
    manhua_list.append('https://www.91hanman.com/book/webBookDetail/270=玄界之门')
    manhua_list.append('https://www.91hanman.com/book/webBookDetail/287=传武')
    manhua_list.append('https://www.91hanman.com/book/webBookDetail/311=重生之都市修仙')
    manhua_list.append('https://www.91hanman.com/book/webBookDetail/328=朕也不想这样')
    manhua_list.append('https://www.91hanman.com/book/webBookDetail/331=武炼巅峰')
    manhua_list.append('https://www.91hanman.com/book/webBookDetail/332=王牌御史')
    manhua_list.append('https://www.91hanman.com/book/webBookDetail/407=驭灵师')
    print(manhua_list)
    manhua_list_count=0
    #ConfigParser 初始化对象
    config = configparser.ConfigParser()
    config.read(base_config_file, encoding="GBK")

    for each_manhua_list in manhua_list:
        manhua_list_count +=1

        list_url = []
        each_manhua_list_info = each_manhua_list.split('=')
        base_manga_name=each_manhua_list_info[1]
        base_log=base_folder+base_manga_name+".txt"
        url = each_manhua_list_info[0]
        print(base_manga_name)
        print(url)

        if not config.has_section(base_manga_name):  # 检查是否存在section
            config.add_section(base_manga_name)
            config.set(base_manga_name, "mangacount", '0')  #修改
            config.write(open(base_config_file, "w"))
        #获取当前第几个漫画
        manhua_list_count_curr= int(config.get(base_manga_name, "mangacount"))
        print(manhua_list_count_curr)




        if(manhua_list_count < manhua_list_count_curr):
            print(manhua_list_count)
            continue
        #保存配置
        config.set(base_manga_name, "mangacount", str(manhua_list_count))  #修改
        config.write(open(base_config_file, "w"))



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
        #网页下载太长 需要加入参数 stream=True 来判断完整性下载
        req = requests.get(url = url,headers = headers,stream=True,verify=False)
        req.encoding = 'utf-8'
        html = req.text
        bf = BeautifulSoup(html, 'lxml')
        targets_url = bf.find_all(class_='detail-chapters-list-item')
        for each_url in targets_url:
            #pdb.set_trace() # 运行到这里会自动暂停
            bf_2 = BeautifulSoup(str(each_url), 'lxml')
            print(bf_2.a.get('href'))
            #忽略特殊编码
            chaptername=bf_2.a.span.span.get_text()
            chaptername_1=chaptername.encode('GBK','ignore')
            chaptername_2=chaptername_1.decode('GBK')
            print(chaptername_2)

            BaseCommon.loglist(base_log,chaptername_2 + '=' + base_url +bf_2.a.get('href'))
            list_url.append(chaptername_2 + '=' + base_url +bf_2.a.get('href'))

        #pdb.set_trace() # 运行到这里会自动暂停

        # for each in targets_url:
        #     list_url.append(each.img.get('alt') + '=' + each.get('href'))

        print('连接采集完成')
        print(list_url)
        print(len(list_url))

        count=0
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
            print(str(count)+'下载：' + filename)
            headers = {
                "User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
                "Referer": "http://www.google.com/bot.html"
            }
            img_req = requests.get(url = target_url,headers = headers,stream=True,verify=False)
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
