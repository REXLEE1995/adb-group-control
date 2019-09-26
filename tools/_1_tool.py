# -*- coding: utf-8 -*-
"""
Created on Fri Jul  5 11:20:41 2019

@author: REXLEE
"""
import logging
from mods.bin_mod import *


class toolclass:

    def __init__(self, phone, config):
        self.phoneid = phone[1]
        self.phonename = phone[0]
        self.apk = bin_mod().convert_path(config[0])
        self.adb = bin_mod().adb()
        self.cmd = bin_mod().run_cmd

    def start(self):
        logging.info('正在对设备:%s 进行软件安装操作' % self.phonename)
        command = self.adb + ' -s %s install -r %s' % (self.phoneid, self.apk)
        if self.cmd(command)[1] == 'Success':
            logging.info('设备:%s 软件安装 成功（包名：%s）' % (self.phonename, self.apk))
        else:
            logging.info('设备:%s 软件安装 失败（包名：%s）' % (self.phonename, self.apk))