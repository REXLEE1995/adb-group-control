# -*- coding: utf-8 -*-
"""
Created on Tue Jul 23 10:25:38 2019

@author: REXLEE
"""
from tkinter import *
import tkinter.filedialog
import tkinter.ttk as ttk

class Page():
    def __init__(self, master):
        self.root = master
        
    def createPage(self):
        self.myFrame = Frame(self.root)
        self.myFrame.place(x=20, y=50)
        Label(self.myFrame,text='选择APK：').grid(row=1, column=1,pady=20)
        self.entry_apk_package = ttk.Entry(self.myFrame,font=('微软雅黑', 10 ),width = 28)
        self.entry_apk_package.grid(row=1, column=2)
        self.Bn_search1 = ttk.Button(self.myFrame, text='浏览', command=self._Bn_search_F1)
        self.Bn_search1.grid(row=1, column=3)

        Label(self.myFrame,text='批量安装路径：').grid(row=2, column=1)
        self.entry_apk_path = ttk.Entry(self.myFrame, font=('微软雅黑', 10), width = 28,state='disabled')
        self.entry_apk_path.grid(row=2, column=2)
        self.Bn_search2 = ttk.Button(self.myFrame,text='浏览', state='disabled', command = self._Bn_search_F2)
        self.Bn_search2.grid(row=2, column=3)
        
    def _Bn_search_F1(self):
        default_dir = r""  # 设置默认打开目录
        self.filename = tkinter.filedialog.askopenfilename(title=u"选择文件",filetypes=[("apk格式", "apk")])
        self.entry_apk_package.delete(0, END)
        self.entry_apk_package.insert(0, self.filename)

    def _Bn_search_F2(self):
        default_dir = r""  # 设置默认打开目录
        self.filename = tkinter.filedialog.askdirectory(title=u"选择文件夹")
        self.entry_apk_path.insert(0, self.filename)
      
    def getconfig(self):
        if self.entry_apk_package.get()=='' and self.entry_apk_path.get()=='':
            return None
        else:
            return (self.entry_apk_package.get(), self.entry_apk_path.get())