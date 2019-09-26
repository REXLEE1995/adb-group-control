# -*- coding: utf-8 -*-
"""
Created on Fri Jul  5 11:20:41 2019

@author: REXLEE
"""

from mods.get_vcardfile import *


class toolclass:

    def __init__(self, phone, config):
        self.phoneid = phone[1]
        self.phonename = phone[0]
        self.num = config[0]
        self.isclear = config[1]

        self.adb = bin_mod().adb()
        self.work_path = bin_mod.work_path

    def start(self):
        # 创建vcf文件
        contactspath = self.__get_vcardfile()
        if self.isclear == 1:
            self.__vcard_clean_data()
            self.__vcard_add_data(contactspath)
        else:
            self.__vcard_add_data(contactspath)

    def __get_vcardfile(self):
        get_vcardfile(self.num)
        path = self.work_path + r'\temp\_vcard_temp\contacts.vcf'
        contactspath = path
        return contactspath

    def __vcard_clean_data(self):
        logging.info('正在对设备:%s 进行通讯录清空操作' % self.phonename)
        command = self.adb + (' -s %s shell pm clear com.android.providers.contacts' % self.phoneid)
        code = bin_mod().run_cmd(command)[0]
        if code == 'Success':
            logging.warning('设备:%s 通讯录清空 成功' % self.phonename)
        else:
            logging.warning('设备:%s 通讯录清空 失败' % self.phonename)

    def __vcard_add_data(self,contactspath):
        logging.info('正在对设备:%s 生成通讯录数据' % self.phonename)
        command = self.adb + '-s %s push %s /sdcard/contacts.vcf' % (self.phoneid, contactspath)
        code = bin_mod().run_cmd(command)[0].split(':')[1]
        if code != ' error':
            command = self.adb + (
                        ' -s %s shell am start -t "text/x-vcard" -d "file:///sdcard/contacts.vcf" -a android.intent.action.VIEW com.android.contacts' %
                        self.phoneid)
            bin_mod().run_cmd(command)[0]
            logging.warning('设备:%s 通讯录数据生成 成功' % self.phonename)
        else:
            logging.warning('设备:%s 通讯录数据生成 失败' % self.phonename)