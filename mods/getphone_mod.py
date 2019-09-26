# -- coding: utf-8 --
"""
Created on Wed Jul  3 09:34:26 2019

@author: REXLEE
"""
import logging
from .bin_mod import bin_mod

class GetPhone:
    def __init__(self):#初始化，获取已连设备信息
        self.adb = bin_mod().adb()#获取ADB工具
        self.runcmd = bin_mod().run_cmd
        self.equipment = []
    
    def __about_phone(self, devices):# 信息处理为可用数据
        if devices[1] == 'offline':
            pid = devices[0]
            model = '未知'
            statu = 'offline'
            return pid, model, statu
        if devices[1] == 'unauthorized':
            pid = devices[0]
            model = '未知'
            statu = 'unauthorized'
            return pid, model, statu
        elif devices[1]=='device':
            pid = devices[0]
            model = self.runcmd(self.adb+' -s %s shell getprop ro.product.model' % pid)[0]
            statu = 'online'
            return pid, model, statu
        else:
            logging.info("请检查设备连接状态")
        
    def usb_connect(self):
        logging.info("正在读取设备列表")
        cmd = (self.adb + ' devices')
        self.deviceslist = self.runcmd(cmd)
        if self.deviceslist[1] == '':
            logging.info('未检测到连入设备')
            self.equipment = None
        else:
            for self.devices in self.deviceslist:
                if self.devices == 'List of devices attached':
                    continue
                elif self.devices == '':
                    break
                else:
                    self.equipment.append(self.__about_phone(self.devices.split()))
                    logging.info('添加设备%s' % self.devices)
            logging.info('已读取设备列表%s' % self.equipment)
        return self.equipment

    def wifi_connect(self):
        print("wifi_connect")