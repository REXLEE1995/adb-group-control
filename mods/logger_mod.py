# -*- coding: utf-8 -*-
"""
Created on Wed Jul  3 09:21:06 2019

@author: REXLEE
"""

import logging
import datetime
from .bin_mod import bin_mod

work_path = bin_mod().work_path

def logger_mod(loglevel=logging.DEBUG):
    logpath = work_path+'\\temp\\_run_log\\'
    logging.basicConfig(
            level = loglevel,
            filename = logpath+"%s.log" % (datetime.datetime.now().strftime('%Y-%m-%d')), #文件名称
            datefmt = '%m-%d %H:%M:%S',#日期格式
            format = '%(asctime)-4s File \'%(pathname)s\', line %(lineno)d, in %(funcName)s(), %(levelname)s -> %(message)s', #格式
            filemode = 'w')#文件模式
    # 将日志输出到控制台
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('in %(filename)s, line %(lineno)d, %(levelname)s -> %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)

if __name__=="__main__":
    print('不支持单独运行文件，请运行run.py')