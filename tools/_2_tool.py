# -*- coding: utf-8 -*-
"""
Created on Fri Jul  5 11:20:41 2019

@author: REXLEE
"""
import logging
from mods.bin_mod import *


class toolclass:

    def __init__(self, phone, config):
        self.mod = bin_mod()
        self.phoneid = phone[1]
        self.phonename = phone[0]
        self.apk = config
        self.adb = self.mod.adb()
        self.cmd = self.mod.run_cmd

    def start(self):
        logging.info('正在对设备:%s 进行软件卸载操作' % self.phonename)
        command = self.adb + ' -s %s uninstall %s' % (self.phoneid, self.apk)
        if self.cmd(command)[0]=='Success':
            logging.info('设备:%s 软件卸载 成功（包名：%s）' % (self.phonename, self.apk))
        elif self.cmd(command)[0] == 'Failure [DELETE_FAILED_INTERNAL_ERROR]':
            logging.info('设备:%s 软件卸载 失败 无法卸载系统应用（包名：%s）' % (self.phonename, self.apk))
        else:
            logging.info('设备:%s 软件卸载 失败 应用不存在（包名：%s）' % (self.phonename, self.apk))