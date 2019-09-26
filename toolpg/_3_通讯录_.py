# -*- coding: utf-8 -*-
"""
Created on Tue Jul 23 10:25:38 2019

@author: REXLEE
"""

from tkinter import *
import tkinter.ttk as ttk

class Page:
    def __init__(self, master):
        self.root = master
        self.ischooes = IntVar()

    def createPage(self):
        self.myFrame = Frame(self.root)
        self.myFrame.place(x=20, y=50)
        Label(self.myFrame, text='输入生成数量：').grid(row=1, column=1, pady=20)
        self.entry_vcard_num = ttk.Entry(self.myFrame, font=('微软雅黑', 10), width=28)
        self.entry_vcard_num.grid(row=1, column=2)
        self.checkbox_vcard = ttk.Checkbutton(self.myFrame, text='是否先清除原有通讯录')
        self.checkbox_vcard.config(variable=self.ischooes, onvalue=1, offvalue=0)
        self.checkbox_vcard.grid(row=2, column=1,sticky=W+E)

        
    def getconfig(self):
        if self.entry_vcard_num.get() == '':
            return None
        else:
            return (self.entry_vcard_num.get(),self.ischooes.get())