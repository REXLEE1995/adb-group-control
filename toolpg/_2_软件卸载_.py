# -*- coding: utf-8 -*-
"""
Created on Tue Jul 23 10:25:38 2019

@author: REXLEE
"""
from tkinter import *
import tkinter.filedialog
import tkinter.ttk as ttk
from mods.bin_mod import bin_mod

class Page:
    def __init__(self, master):
        self.root = master

    def createPage(self):
        self.myFrame = Frame(self.root)
        self.myFrame.place(x=20, y=50)

        Label(self.myFrame, text='选择APK：').grid(row=1, column=1, pady=20)
        self.entry_apk_package = ttk.Entry(self.myFrame, font=('微软雅黑', 10), width=28)
        self.entry_apk_package.grid(row=1, column=2)
        self.Bn_search1 = ttk.Button(self.myFrame, text='浏览', command=self.Bn_search_F1)
        self.Bn_search1.grid(row=1, column=3)
        Label(self.myFrame, text='(选择APK查看对应包名)').grid(row=2, column=2, pady=0, sticky=W)
        Label(self.myFrame, text='卸载应用(包名)：').grid(row=3, column=1, pady=20)
        self.entry_pack_name = ttk.Entry(self.myFrame, font=('微软雅黑', 10), width=28)
        self.entry_pack_name.grid(row=3, column=2)


    def Bn_search_F1(self):
        default_dir = r""  # 设置默认打开目录
        self.filename = tkinter.filedialog.askopenfilename(title=u"选择文件",filetypes=[("apk格式", "apk")])
        self.entry_apk_package.delete(0, END)
        self.entry_apk_package.insert(0, self.filename)
        if self.filename:
            self.entry_pack_name.delete(0, END)
            self.entry_pack_name.insert(0, bin_mod().package(self.filename))

    def getconfig(self):
        if self.entry_pack_name.get()=='':
            return None
        else:
            return (self.entry_pack_name.get())
