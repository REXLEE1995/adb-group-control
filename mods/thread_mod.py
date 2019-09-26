# -*- coding: utf-8 -*-
"""
Created on Tue Jul  2 15:05:29 2019

@author: REXLEE
"""

from threading import Thread
import logging
import datetime
import importlib


class ThreadClass:

    def thread_start(self, equipment, toollist, config):#线程执行方法
        self.threads = []
        #运行开始，记录开始时间
        self.starttime = datetime.datetime.now()
        logging.info('运行开始时间：%s' % self.starttime.strftime('%H:%M:%S'))
        for phone in equipment:
            thread = Thread(target=Plan().myplan, args=(phone, toollist, config,))
            thread.start()
            # self.threads.append(thread)
        # for thread in self.threads:
        #     thread.join()


class Plan:

    def myplan(self, phone, toollist, config):
        for num in toollist:
            tempimport = importlib.import_module('tools.'+'_'+num+'_tool')
            temp = tempimport.toolclass(phone, config[int(num)]())
            temp.start()
