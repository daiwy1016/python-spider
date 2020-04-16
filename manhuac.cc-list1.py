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


import json
#引入自定义函数
from python_lib import BaseCommon

if __name__ == '__main__':

    #base_folder ='F:/py3project/91hanman/'#以/结束 home
    #base_folder ='F:/py3workspace/python-spider/'#以/结束 company
    base_folder = os.getcwd()+"\\"
    base_url='https://www.manhuaw.cc'
    base_config_file=base_folder+'\\'+sys.argv[0][sys.argv[0].rfind(os.sep) + 1:-3]+'.ini'
    #判断配置文件是否存在 不存在建立
    if os.path.exists(base_config_file) ==  False:
        BaseCommon.loglist(base_config_file,"")
    print(base_config_file)
    #定义一组
    manhua_list=[]
    manhua_vip_list = []
    manhua_vip_list.append('1-vip-1=https://www.manhuaw.cc/index/api/getpage/tp/1-vip-1')
    manhua_vip_list.append('1-vip-2=https://www.manhuaw.cc/index/api/getpage/tp/1-vip-2')
    manhua_vip_list.append('1-vip-3=https://www.manhuaw.cc/index/api/getpage/tp/1-vip-3')
    manhua_vip_list.append('1-vip-4=https://www.manhuaw.cc/index/api/getpage/tp/1-vip-4')
    manhua_vip_list.append('1-vip-5=https://www.manhuaw.cc/index/api/getpage/tp/1-vip-5')
    manhua_vip_list.append('1-vip-6=https://www.manhuaw.cc/index/api/getpage/tp/1-vip-6')
    manhua_vip_list.append('1-vip-7=https://www.manhuaw.cc/index/api/getpage/tp/1-vip-7')
    manhua_vip_list.append('1-vip-8=https://www.manhuaw.cc/index/api/getpage/tp/1-vip-8')
    manhua_vip_list.append('1-vip-9=https://www.manhuaw.cc/index/api/getpage/tp/1-vip-9')
    manhua_vip_list.append('1-vip-10=https://www.manhuaw.cc/index/api/getpage/tp/1-vip-10')


    for each_manhua_vip_list in manhua_vip_list:
        each_manhua_vip_list_info = each_manhua_vip_list.split('=')
        #保存以便读取
        if os.path.exists(base_folder + each_manhua_vip_list_info[0] + '.txt') ==  False:
            #获取列表
            myVipUrul = each_manhua_vip_list_info[1]
            headers = {
                    "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
                    "Referer": base_url
            }
            # 发送请求，获取响应结果
            response_list = requests.get(url=myVipUrul, headers=headers, verify=False)
            response_json = response_list.text
            BaseCommon.loglist(base_folder + each_manhua_vip_list_info[0] + '.txt',response_json)
            # 将响应内容转换为Json对象
            jsonobj = json.loads(response_json)
            # 从Json对象获取想要的内容
            totalRow = jsonobj['result']['list']
            manhua_list = totalRow
            #manhua_list.append('manhuac-鸭王（无删减）=1175')#83 中断
            response_list.close()

        else:
            print('已有跳过，保存');
            with open(base_folder + each_manhua_vip_list_info[0] + '.txt', "r") as f:  # 打开文件
                data = f.read()  # 读取文件
                # 将响应内容转换为Json对象
                jsonobj = json.loads(data)
                # 从Json对象获取想要的内容
                totalRow = jsonobj['result']['list']
                manhua_list = totalRow
                f.close()


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
            #each_manhua_list_info = each_manhua_list.split('=')
            base_manga_name= each_manhua_list['title']

            url = base_url+"/index/book/index/id/"+each_manhua_list['id']
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
            base_manhua_folder = base_folder+base_manga_name +"\\"
            base_log=base_folder+base_manga_name +"\\"+base_manga_name+".txt"
            BaseCommon.loglist(base_folder + base_manga_name +"\\"+base_manga_name+"_about.txt",each_manhua_list['title'])
            BaseCommon.loglist(base_folder + base_manga_name +"\\"+base_manga_name+"_about.txt",'题材:'+each_manhua_list['ticai'])
            BaseCommon.loglist(base_folder + base_manga_name +"\\"+base_manga_name+"_about.txt",'类型:'+each_manhua_list['keyword'])
            BaseCommon.loglist(base_folder + base_manga_name +"\\"+base_manga_name+"_about.txt",'作者:'+each_manhua_list['auther'])
            BaseCommon.loglist(base_folder + base_manga_name +"\\"+base_manga_name+"_about.txt",'简介:'+each_manhua_list['desc'])

            # if num == 1:
            #     url = 'view-source:https://www.91hanman.com/book/webBookDetail/69'
            # else:
            #     url = 'http://www.shuaia.net/index_%d.html' % num
            #TODO:
            #url = base_url+'/mh/xe/20.html'
            # headers = {
            #         "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
            #         "Referer": base_url
            # }
            # ssl._create_default_https_context = ssl._create_unverified_context
            # print("请求：url："+url)
            # #网页下载太长 需要加入参数 stream=True 来判断完整性下载
            # req = requests.get(url = url,headers = headers,stream=True,verify=False)
            # req.encoding = 'UTF-8'
            # html = req.text
            # print("开始请求成功")
            # #过滤空格
            # #html=html.replace('&nbsp;', '')
            # bf = BeautifulSoup(html, 'lxml')
            # #print(bf)
            # ##=======================获取简介===============
            # #about = bf.find_all('div',class_='book-desc')
            # #about_2 = BeautifulSoup(str(about), 'lxml')
            # #[s.extract() for s in about_2("a")]#去除指定标签
            # #[s.extract() for s in about_2("strong")]#去除指定标签
            # #pdb.set_trace()
            # about_3 = bf.find('p',class_="book-desc")
            # print(about_3)
            # #pdb.set_trace()
            # #忽略特殊编码
            # jianjie=about_3.get_text()
            # jianjie_1=jianjie.encode('GBK','ignore')
            # jianjie_2=jianjie_1.decode('GBK')
            # print(jianjie_2)
            # BaseCommon.loglist(base_log,'简介:'+jianjie_2)
            # # 防止被反爬，打开后关闭
            # req.close()
            #=======================获取章节列表地址 多少话===============
            #https://www.manhuaw.cc/index/api/isread/id/1175
            #https://www.manhuaw.cc/index/book/index/id/1175
            #https://www.manhuaw.cc/index/api/chapter_list/tp/1175-1-1-72
            #https://www.manhuaw.cc/index/api/chapter_list/tp/1175-1-1-10

            if os.path.exists(base_manhua_folder+base_manga_name+"_json.txt") ==  False:

                reqUrl = base_url + "/index/api/chapter_list/tp/" + each_manhua_list['id'] + "-1-1-10"
                headers = {
                        "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
                        "Referer": base_url
                }
                # 发送请求，获取响应结果
                response_list = requests.get(url=reqUrl, headers=headers, verify=False)
                response_json = response_list.text
                # 将响应内容转换为Json对象
                jsonobj = json.loads(response_json)
                # 从Json对象获取想要的内容
                totalRow = jsonobj['result']['totalRow']
                response_list.close()
                        #=======================获取章节列表地址===============
                #https://www.manhuaw.cc/index/api/isread/id/1175
                #https://www.manhuaw.cc/index/book/index/id/1175
                #https://www.manhuaw.cc/index/api/chapter_list/tp/1175-1-1-72
                #https://www.manhuaw.cc/index/api/chapter_list/tp/1175-1-1-10
                reqListUrl = base_url + "/index/api/chapter_list/tp/" + each_manhua_list['id'] + "-1-1-" + totalRow
                headers = {
                        "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
                        "Referer": reqUrl
                }
                # 发送请求，获取响应结果
                response_list = requests.get(url=reqListUrl, headers=headers, verify=False)
                response_json = response_list.text
                BaseCommon.loglist(base_manhua_folder+base_manga_name+"_json.txt",response_json)

                # 将响应内容转换为Json对象
                jsonobj = json.loads(response_json)
                # 从Json对象获取想要的内容
                totalRow = jsonobj['result']['list']
                response_list.close()
                #=======================获取章节列表===============
                for each_url in totalRow:
                    BaseCommon.loglist(base_log,each_url['title'] + '=' +each_url['imagelist'])
                    list_url.append(each_url['title'] + '=' + base_url +"/index/book/capter/id/"+each_url['id'])
            else:
                print('漫画列表 '+base_manga_name+' 已有，跳过服务器获取');
                with open(base_manhua_folder+base_manga_name+"_json.txt", "r") as f:  # 打开文件
                    data = f.read()  # 读取文件
                    # 将响应内容转换为Json对象
                    jsonobj = json.loads(data)
                    # 从Json对象获取想要的内容
                    totalRow = jsonobj['result']['list']
                    response_list.close()
                    #=======================获取章节列表===============
                    for each_url in totalRow:
                        BaseCommon.loglist(base_log,each_url['title'] + '=' +each_url['imagelist'])
                        list_url.append(each_url['title'] + '=' + base_url +"/index/book/capter/id/"+each_url['id'])
                    f.close()



            #print(str(about_3).encode('utf-8'))
            #print(len(about_3))
            #pdb.set_trace()
            #print(about_2.original_encoding)

            # c=0
            # for each_about_3 in about_3:
            #     # c+=1
            #     # print(c)
            #     # print(each_about_3.get_text())
            #     # print(type(each_about_3.get_text()))
            #     print(each_about_3.get_text().strip()=='')
            #     if each_about_3.get_text().strip()=='':
            #         continue
            #     print(each_about_3.get_text())
            #     BaseCommon.loglist(base_log,'简介:'+each_about_3.get_text())

            #exit();
            #=======================获取章节列表===============
            # targets_url = bf.find_all('ul',class_='chapter_list_panel')
            # for each_url in targets_url:
            #     #pdb.set_trace() # 运行到这里会自动暂停
            #     bf_2 = BeautifulSoup(str(each_url), 'lxml')
            #     #[s.extract() for s in bf_2("p")]#去除指定标签
            #     targets_url_2 = bf_2.find_all('a')
            #     for each_url_2 in targets_url_2:
            #         print(each_url_2.get('href'))

            #         #忽略特殊编码
            #         chaptername=each_url_2.get_text()
            #         chaptername_1=chaptername.encode('GBK','ignore')
            #         chaptername_2=chaptername_1.decode('GBK')
            #         print(chaptername_2)
            #         #pdb.set_trace()
            #         BaseCommon.loglist(base_log,chaptername_2 + '=' + base_url +each_url_2.get('href'))
            #         list_url.append(chaptername_2 + '=' + base_url +each_url_2.get('href'))

                #pdb.set_trace() # 运行到这里会自动暂停

                # for each in targets_url:
                #     list_url.append(each.img.get('alt') + '=' + each.get('href'))
            #=======================JSON获取章节列表===============

            list_url = totalRow;
            print('连接采集完成')
            print(list_url)
            print(len(list_url))
            count=0
            if not config.has_section(base_manga_name):  # 检查是否存在section
                config.add_section(base_manga_name)
                config.set(base_manga_name, "chaptercount", '0')  #修改
                config.set(base_manga_name, "url", "/index/book/index/id/"+each_manhua_list['id'])  #保存采集列表地址
                config.write(open(base_config_file, "w"))
            #获取当前章节
            if not config.has_option(base_manga_name, "chaptercount"):
                config.set(base_manga_name, "chaptercount", '0')  #修改
                config.set(base_manga_name, "url", "/index/book/index/id/"+each_manhua_list['id'])  #保存采集列表地址
                config.write(open(base_config_file, "w"))
            manhua_chapter_count_curr= int(config.get(base_manga_name, "chaptercount"))
            for each_img in list_url:
                #pdb.set_trace()
                count +=1
                if(count < manhua_chapter_count_curr):
                    print(count)
                    continue
                #判断是否有结束章节
                #pdb.set_trace()
                if not config.has_option(base_manga_name, "chaptercountend"):
                    #pdb.set_trace()
                    print("设置结束章节："+str(len(list_url)))
                    config.set(base_manga_name, "chaptercountend", str(len(list_url)))  #修改
                    config.write(open(base_config_file, "w"))
                #判断结束章节 跳出循环
                config.read(base_config_file, encoding="GBK")
                manhua_chapter_count_end= int(config.get(base_manga_name, "chaptercountend"))
                #pdb.set_trace()
                print("当前的结束章节1："+str(manhua_chapter_count_end))
                if(count > manhua_chapter_count_end):
                    print(count)
                    break

                config.set(base_manga_name, "chaptercount", str(count))  #修改
                config.write(open(base_config_file, "w"))
                folder=base_folder+base_manga_name+'/'+str(count)
                #pdb.set_trace()
                print(os.path.exists(folder));
                if os.path.exists(folder) ==  False:
                    if folder not in os.listdir():
                        os.makedirs(folder)
                #pdb.set_trace() # 运行到这里会自动暂停
                #img_info = each_img.split('=')
                filename = each_img['title']
                print('下载：' + filename)

                # target_url = img_info[1]
                # if target_url == '':
                #     referer_url=url
                # else:
                #     referer_url=target_url
                # headers = {
                #     "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
                #     "Referer": referer_url
                # }
                # print(headers)
                # img_req = requests.get(url = target_url,headers = headers,verify=False)

                # img_req.encoding = 'utf-8'
                # img_html = img_req.text
                # img_bf_1 = BeautifulSoup(img_html, 'lxml')
                # #=======================获取图片列表===============
                # img_url = img_bf_1.find_all('div', class_='comicpage')
                # img_bf_2 = BeautifulSoup(str(img_url), 'lxml')#str 返回一个字符串 把对象转换字符串
                # img_bf_3 =img_bf_2.find_all('img',class_='lazy')

                img_bf_3 = each_img['imagelist'].split(',')

                print("本章节图片数量："+str(len(img_bf_3)))
                #img_bf_3 =img_bf_2.find_all('img')
                # 防止被反爬，打开后关闭
                #img_req.close()
                i=0
                for each_img_2 in img_bf_3:
                    i += 1
                    #img_bf_4 = BeautifulSoup(str(each_img_2), 'lxml')#str 返回一个字符串 把对象转换字符串
                    #img_url = each_img_2.get('data-original')
                    img_url = each_img_2

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
                    #pdb.set_trace() # 运行到这里会自动暂停
        print('下载完成！')
        #os.system('shutdown -s -f -t 59')
