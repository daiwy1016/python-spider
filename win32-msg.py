#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-09-09 22:26:50
# @Author  : 小戴 (408366645@qq.com)
# @Link    : http://www.phpet.com/
# @Version : $Id$

from datetime import *
import os
import win32api
import win32con
from threading import *

tmNow = datetime.now()
d = date.today()
t = time(23,10,0)
shtdownTime = datetime.combine(d,t)

def ShowHint():    
    while True:
        tmNow = datetime.now()
        timedDelta = (shtdownTime - tmNow).total_seconds()
        if timedDelta < 60:
            win32api.MessageBox(win32con.NULL, u'还有59s关机，赶快保存一下！', u'温馨提醒', win32con.MB_OK)
            break
        else:
            continue
def ShutDown():
    while True:
        tmNow = datetime.now()
        timedDelta = (shtdownTime - tmNow).total_seconds()
        if timedDelta < 60:
            os.system('shutdown -s -f -t 59')
            break
        else:
            continue
            
if __name__ == '__main__':
    # threadShowHint = threading.Thread(target=ShowHint)
    # threadShutDown = threading.Thread(target=ShutDown)
    
    # threadShowHint.start()
    # threadShutDown.start()
    win32api.MessageBox(win32con.NULL, u'还有59s关机，赶快保存一下！', u'温馨提醒', win32con.MB_OK)