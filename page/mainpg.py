# -- coding: utf-8 --
"""
Created on Tue Jul 23 10:25:38 2019

@author: REXLEE
"""

from tkinter import *
import tkinter.ttk as ttk
import tkinter as tk
import tkinter.font as tkFont
from toolpg import configPage
from mods.bin_mod import bin_mod
import importlib


class Mainpg(object):

    def __init__(self, root):
        self.root = root
        # 初始化窗口
        self.root.title('安卓助手')
        self.root.attributes("-alpha", 0.9)
        self.root.resizable(width=False, height=False)
        rootsize = '%dx%d+%d+%d' % (285, 480, (self.root.winfo_screenwidth() - 285) / 2, (self.root.winfo_screenheight() - 480) / 2)
        self.root.geometry(rootsize)
        self.root.attributes('-alpha', 0.98,)
        self.root.protocol('WM_DELETE_WINDOW', self.closeWindow)
        self.createpg()

    def createpg(self):
        self.pic_path = bin_mod.work_path + '\\page\\png\\' # 获取图标目录
        self.toolpglist = configPage # 获取页面列表
        self.mainframe = Frame(self.root)
        self.mainframe.pack(fill=BOTH, expand=True)
        self.phonepg()
        ttk.Frame(self.mainframe, width=5,).pack(side=LEFT, fill=Y)

        self.toolpgmain()

    def phonepg(self):
        self.phonepg_Frame = ttk.LabelFrame(self.mainframe, text='手机列表')
        # self.phonepg_Frame.pack_propagate(1)
        self.phonepg_Frame.pack(side=LEFT, fill=Y)
        self.button_frame = ttk.Frame(self.phonepg_Frame)
        self.button_frame.pack(fill=X)

        # ------------------操作按钮1-----------------
        self.phonebn_Frame1 = ttk.Frame(self.button_frame)
        self.phonebn_Frame1.grid(row=1,column=1,sticky=W)
        self.connect_bn = ttk.Button(self.phonebn_Frame1, text='连接设备', width=8, command=self.connect_bn_f)
        self.connect_bn.pack(fill=X, side=LEFT, expand=True)
        self.refresh_bn = ttk.Button(self.phonebn_Frame1, text='刷新列表', width=8, command=self.refresh_bn_f)
        self.refresh_bn.pack(fill=X, side=LEFT, expand=True)
        self.terminal_bn = ttk.Button(self.phonebn_Frame1, text='ADB终端', width=8, command=self.terminal_bn_f)
        self.terminal_bn.pack(fill=X, side=LEFT, expand=True)
        self.log_bn = ttk.Button(self.phonebn_Frame1, text='抓取LOG', width=8, command=self.log_bn_f)
        self.log_bn.pack(fill=X, side=LEFT, expand=True)


        # ------------------操作按钮2------------------------------------------------
        self.phonebn_Frame2 = ttk.Frame(self.button_frame)
        self.phonebn_Frame2.grid(row=2,column=1,sticky=W)
        self.choose_bn = ttk.Button(self.phonebn_Frame2, text='载入所有', width=8, command=self.choose_bn_f)
        self.choose_bn.pack(fill=X, side=LEFT, expand=True)
        # self.twinkle_bn = ttk.Button(self.phonebn_Frame2, text='闪烁手机', width=8, command=self.twinkle_bn_f)
        # self.twinkle_bn.pack(fill=X, side=LEFT, expand=True)
        self.twinkle_bn = ttk.Button(self.phonebn_Frame2, text='删除Msg', width=8, command=self.deleMsg_bn_f)
        self.twinkle_bn.pack(fill=X, side=LEFT, expand=True)
        self.NULL2_bn = ttk.Button(self.phonebn_Frame2, text='软件列表', width=8, command=self.package_bn_f)
        self.NULL2_bn.pack(fill=X, side=LEFT, expand=True)

        self.run_pic = tk.PhotoImage(file=self.pic_path + r"\run_pic.png")
        self.run_bn = ttk.Button(self.phonebn_Frame2, text='RUN ',
                                 width=5,
                                 compound="left",
                                 image=self.run_pic,
                                 command=self.run_fun)
        self.run_bn.pack(fill=X, side=LEFT, expand=True)

        self.mini_bn_frame = tk.Frame(self.button_frame)
        self.mini_bn_frame.grid(row=1,column=2,rowspan=2,sticky=N+E+W+S)
        self.mini_bn = ttk.Button(self.mini_bn_frame, text='》',
                                  width=1,
                                  compound="left",
                                  command=self.mini_bn_f)
        self.mini_bn.pack(fill=Y, expand=True)

        self.phonebn_Frame3 = ttk.Frame(self.button_frame)
        self.phonebn_Frame3.grid(row=3, column=1,columnspan=2,sticky=W+E)

        self.more_button = ttk.Button(self.phonebn_Frame3,text='微信缓存清空',width=26, command = self.more_bn_f).pack(fill=X, side=LEFT, expand=True)


        # ------------------设备列表1------------------------------------------------
        self.phonelist_Frame1 = Frame(self.phonepg_Frame,bd=1, relief="sunken")
        self.phonelist_Frame1.pack(fill=BOTH, expand=True)
        self.phonelist_tree = ttk.Treeview(self.phonelist_Frame1, selectmode="extended", show="headings")
        self.phonelist_tree["columns"] = ("选中", "型号", "PID")
        self.phonelist_tree.heading("#0", text="#")
        self.phonelist_tree.column("#0", minwidth=0, stretch=YES, anchor='center')
        self.phonelist_tree.heading("选中", text="选中")
        self.phonelist_tree.column("选中", minwidth=0, width=50, stretch=YES, anchor='center')
        self.phonelist_tree.heading("型号", text="型号")
        self.phonelist_tree.column("型号", minwidth=0, width=80, stretch=YES, anchor='center')
        self.phonelist_tree.heading("PID", text="PID")
        self.phonelist_tree.column("PID", minwidth=0, width=130, stretch=YES, anchor='center')
        # 垂直滚动条
        self.scrolly1 = ttk.Scrollbar(self.phonelist_Frame1, orient=VERTICAL, command=self.phonelist_tree.yview)
        self.phonelist_tree.configure(yscrollcommand=self.scrolly1.set)
        self.phonelist_tree.pack(fill=BOTH, side=LEFT, expand=True)
        # self.scrolly1.pack(fill=Y, side=LEFT, expand=True)
        self.phonelist_tree.bind('<Double-1>', self.phonelist_Double_f)  # 绑定左键双击事件===========
        self.phonelist_tree.bind('<Control-c>', self.copy_pid_f)  # 绑定左键双击事件===========

    def toolpgmain(self):
        self.toolpg_all = ttk.Frame(self.mainframe)
        self.toolpg_all.pack(side=LEFT, fill=BOTH, expand=True)

        self.toolchoose_Frame = ttk.LabelFrame(self.toolpg_all,height=180, text='执行顺序')
        self.toolchoose_Frame.pack_propagate(0)
        self.toolchoose_Frame.pack(side=BOTTOM, fill=BOTH)
        self.toolchoose_Button = Frame(self.toolchoose_Frame, width=211)
        self.toolchoose_Button.pack_propagate(0)
        self.toolchoose_Button.pack(side=RIGHT, fill=BOTH, expand=0)
        ttk.Button(self.toolchoose_Button,text = '清空内容',command = self.toolchoose_Button_f).pack(fill=BOTH)
        self.choose_Frame = LabelFrame(self.toolchoose_Frame)
        self.choose_Frame.pack(side=RIGHT, fill=BOTH, expand=True)
        self.choose_Label=Label(self.choose_Frame,
              text='',
              font=tkFont.Font(family='微软雅黑', size=12),
              wraplength=600,
              justify='left',
              anchor='nw'
              )
        self.choose_Label.pack(fill=BOTH, expand=True)

        self.tool_top = ttk.Frame(self.toolpg_all)
        self.tool_top.pack(side=BOTTOM, fill=BOTH, expand=True)

        self.toollist = ttk.LabelFrame(self.tool_top, text='工具列表（双击载入）', width=211)
        self.toollist.pack_propagate(0)
        self.toollist.pack(side=RIGHT, fill=BOTH, expand=0)
        ttk.Frame(self.tool_top, width=5).pack(side=RIGHT, fill=BOTH, expand=0)
        self.toollist_Frame1 = Frame(self.toollist)
        self.toollist_Frame1.pack(fill=BOTH, expand=True)
        self.tooltree = ttk.Treeview(self.toollist_Frame1, show="headings")
        self.tooltree["columns"] = ("序号", "工具名称", "选中")
        self.tooltree.heading("#0", text="#")
        self.tooltree.column("#0", minwidth=0, stretch=YES, anchor='center')
        self.tooltree.heading("序号", text="序号")
        self.tooltree.column("序号", minwidth=0, width=35, stretch=YES, anchor='center')
        self.tooltree.heading("工具名称", text="工具名称")
        self.tooltree.column("工具名称", minwidth=0, width=100, stretch=YES, anchor='center')
        self.tooltree.heading("选中", text="选中")
        self.tooltree.column("选中", minwidth=0, width=50, stretch=YES, anchor='center')

        for l in self.toolpglist:
            self.tooltree.insert('', 'end', values=(l.split('_')[1], l.split('_')[2], ''))
        self.tooltree.pack(fill=None, side=LEFT, expand=True)
        self.tooltree.bind('<ButtonRelease-1>', self.tooltree_click_f)  # 绑定左键单击事件===========
        self.tooltree.bind('<Double-1>', self.tooltree_click1_f)  # 绑定左键双击事件===========
        self.tooltree.pack(fill=BOTH, expand=True)

        self.toolpg = ttk.LabelFrame(self.tool_top, text='工具配置')
        self.toolpg.pack(side=RIGHT, fill=BOTH, expand=True)
        self.tablist = []
        self.toolpgtabControl = ttk.Notebook(self.toolpg,padding=-2)
        for tabname in self.toolpglist:
            tab = Label(self.toolpgtabControl,)
            self.toolpgtabControl.add(tab, text=tabname.split("_")[2])  # Add the tab
            self.tablist.append(tab)

        self.toolpgtabControl.pack(fill=BOTH, expand=True)

        self.config = {}
        n = 0
        for tabpage in self.toolpglist:
            tempimport = importlib.import_module('toolpg.'+tabpage)
            temp = tempimport.Page(self.tablist[n])
            temp.createPage()
            self.config[n+1] = temp.getconfig
            n = n+1

        self.toolhead = tk.Label(self.toolpg, text='            └ 软件安装',
                                 font=tkFont.Font(family='微软雅黑', size=10, weight=tkFont.BOLD),
                                 width=67,
                                 anchor=W,
                                 relief='ridge',
                                 pady=3,
                                 bd=1,
                                 fg='MidnightBlue',
                                 bg='AliceBlue')
        self.toolhead.place(x=0, y=0)
