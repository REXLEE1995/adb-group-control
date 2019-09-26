import tkinter as tk
from tkinter import *
from tkinter import messagebox
from mods.getphone_mod import GetPhone
import time
import datetime
import logging
from .mainpg import Mainpg
from mods.bin_mod import *
from mods.thread_mod import ThreadClass
from threading import Thread
import ctypes
import inspect


class Mainpg_fun(Mainpg):

    def __init__(self, root):
        super(Mainpg_fun, self).__init__(root)
        self.adb = bin_mod().adb()
        self.run_cmd = bin_mod().run_cmd
        self.sh_cmd = bin_mod().sh_cmd
        self.mytools_num = []

    # 连接设备
    def connect_bn_f(self):
        if self.connect_bn["text"] == '断开连接':
            os.popen(self.adb+'kill-server')
            x=self.phonelist_tree.get_children()
            for item in x:
                self.phonelist_tree.delete(item)
            self.connect_bn.config(text='重新连接')
            return
        self.phonelist = GetPhone().usb_connect()
        if self.phonelist==None:
            messagebox.showinfo('通知', '请检查设备是否正确连接')
        else:
            for p in self.phonelist:
                self.phonelist_tree.insert('', 'end', values=('', p[1], p[0]))
            self.connect_bn.config(text = '断开连接')

    # 刷新列表
    def refresh_bn_f(self):
        if self.connect_bn["text"] == '重新连接' or self.connect_bn["text"] == '连接设备':
            messagebox.showinfo('通知', '请先连接设备')
            return
        x = self.phonelist_tree.get_children()
        for item in x:
            self.phonelist_tree.delete(item)
        self.phonelist = GetPhone().usb_connect()
        if self.phonelist==None:
            messagebox.showinfo('通知', '无设备')
        else:
            for p in self.phonelist:
                self.phonelist_tree.insert('', 'end', values=('', p[1], p[0]))

    # adb终端
    def terminal_bn_f(self):
        try:
            pid = (self.phonelist_tree.item(self.phonelist_tree.selection()[0], "values"))[2]
            os.popen('start ' + self.adb + '-s %s shell' % pid)
        except:
            messagebox.showinfo('通知', '请先选择设备')

    # 抓取log
    def log_bn_f(self):
        if self.log_bn["text"] == '抓取LOG':
            try:
                pid = (self.phonelist_tree.item(self.phonelist_tree.selection()[0], "values"))[2]
                pname = (self.phonelist_tree.item(self.phonelist_tree.selection()[0], "values"))[1]
                nowtime = datetime.datetime.now().strftime('%Y%m%d%H')
                filename = pname + '_log_' + nowtime + ".log"
                cmd1 = 'start ' + self.adb + '-s %s logcat -v time -s "tencent"' % pid
                cmd2 = self.adb + '-s %s logcat -v time -s "tencent">%s' % (pid, filename)

                self.thread1 = Thread(target=os.system, args=(cmd1,))
                self.thread2 = Thread(target=self.sh_cmd, args=(cmd2,))
                self.thread1.start()
                self.thread2.start()
                self.log_bn.config(text='停止抓取')
            except:
                messagebox.showinfo('通知', '请先选择设备')
        else:
            self.log_bn.config(text='抓取LOG')
            #停止进程
            print(self.thread2.ident)
            self.stop_thread(self.thread2)
            self.stop_thread(self.thread1)

    # 载入所有
    def choose_bn_f(self):
        if self.phonelist_tree.get_children() and self.choose_bn['text'] == '载入所有':
            self.choose_bn['text'] = '清空所有'
            for item in self.phonelist_tree.get_children():
                if self.phonelist_tree.item(item, "values")[0] == '':
                    self.phonelist_tree.set(item, column='#1', value=('√'))
        else:
            self.choose_bn['text'] = '载入所有'
            for item in self.phonelist_tree.get_children():
                if self.phonelist_tree.item(item, "values")[0] == '√':
                    self.phonelist_tree.set(item, column='#1', value=(''))

    # 删除.Msg
    def deleMsg_bn_f(self):
        try:
            pid = (self.phonelist_tree.item(self.phonelist_tree.selection()[0], "values"))[2]
            pname = (self.phonelist_tree.item(self.phonelist_tree.selection()[0], "values"))[1]
            cmd = self.adb + '-s %s shell rm -rf sdcard/tencent/.Msg' %pid
            self.run_cmd(cmd)
            logging.info('设备:%s .Msg文件夹删除 成功' % pname)
        except:
            messagebox.showinfo('通知', '请先选择设备')

    # # 闪烁手机
    # def twinkle_bn_f(self):
    #     try:
    #         pid = (self.phonelist_tree.item(self.phonelist_tree.selection()[0], "values"))[2]
    #         infos = os.popen(self.adb + "-s %s shell dumpsys power" %pid).readlines()
    #         for i in infos:
    #             if "Display Power: state=" in i:
    #                 info = i.split("=")[1].strip("\n")  # 分割，然后去掉"\n"
    #                 if info == "OFF":
    #                     os.popen(self.adb + ' -s %s shell input keyevent 26' % pid)
    #                     time.sleep(1)
    #         cmd = self.adb + '-s %s shell settings put system screen_brightness 1' %pid
    #         cmd2 = self.adb + '-s %s shell settings put system screen_brightness 255' %pid
    #         for num in range(4):
    #             if (num % 2) == 0:
    #                 os.popen(cmd)
    #             else:
    #                 os.popen(cmd2)
    #             time.sleep(0.5)
    #     except:
    #         messagebox.showinfo('通知', '请先选择设备')

    # 展示软件列表&包名
    def package_bn_f(self):
        try:
            pid = (self.phonelist_tree.item(self.phonelist_tree.selection()[0], "values"))[2]
            pname = (self.phonelist_tree.item(self.phonelist_tree.selection()[0], "values"))[1]
            nowtime = datetime.datetime.now().strftime('%Y%m%d')
            path = 'temp\\' + pname+'_Packagelist\\'
            if not os.path.exists(path):
                os.makedirs(path)
                filename = path + 'Packagelist_' + nowtime + ".txt"
            else:
                filename = path + 'Packagelist_' + nowtime + ".txt"
            logcat_file = open(filename, 'w')
            logcmd = self.adb + '-s {0} shell pm list packages'.format(pid)
            self.pro = subprocess.Popen(logcmd, stdout=logcat_file, stderr=subprocess.PIPE)
            packagelist = subprocess.getstatusoutput(logcmd)# 包列表
            currentPackage = subprocess.getstatusoutput(self.adb + 'shell dumpsys window | findstr mCurrentFocus ')# 当前包名
            top = tk.Toplevel(self.root)
            top.wm_attributes('-topmost', 1)
            top.title('--包名列表(%s)' % pname)
            top.geometry('%dx%d+%d+%d' % (300, self.root.winfo_height(), self.root.winfo_x()+285, self.root.winfo_y()))  # 设置窗口大小
            t = tk.Text(top)
            t.pack(fill=BOTH, expand=True)
            t.insert('1.0', "------------------------------\n")
            t.insert('2.0', "当前应用的包名及activity：\n")
            t.insert('3.0', "{}\n".format(currentPackage[1]))
            t.insert('4.0', "------------------------------\n")
            t.insert('5.0', "所有包列表：\n")
            t.insert('6.0', "{}".format(packagelist[1]))
            # 插入文本，用引号引起来“2.0” 这个是插入文本的坐标，且1与0之间为点，而不是逗号，切记
            top.mainloop()
        except:
            messagebox.showinfo('通知', '请先选择设备')

    # 微信清缓存
    def more_bn_f(self):
        try:
            pid = (self.phonelist_tree.item(self.phonelist_tree.selection()[0], "values"))[2]
            pname = (self.phonelist_tree.item(self.phonelist_tree.selection()[0], "values"))[1]
            cmd = self.adb + '-s %s shell pm clear com.tencent.mm' %pid
            msg = self.run_cmd(cmd)
            if msg[0] == 'Success':
                logging.warning('设备:%s 微信清空 成功' % pname)
        except:
            messagebox.showinfo('通知', '请先选择设备')

    # 已连接设备的双击功能
    def phonelist_Double_f(self, event):
        for item in self.phonelist_tree.selection():
            if self.phonelist_tree.item(item, "values")[0]=='':
                self.phonelist_tree.set(item, column='#1', value=('√'))
            else:
                self.phonelist_tree.set(item, column='#1', value=(''))

    # 设置工具标题
    def tooltree_click_f(self, event):
        try:
            # 切换分页
            self.toolpgtabControl.select(int(self.tooltree.item(self.tooltree.selection(), "values")[0])-1)
            # 设置页签头
            self.toolhead['text'] = ('            └ '+self.tooltree.item(self.tooltree.selection(), "values")[1])
        except:
            pass

    # 勾选工具
    def tooltree_click1_f(self,event):
        try:
            temp_choose = self.tooltree.item(self.tooltree.selection(), "values")[1]
            temp_choose_num = self.tooltree.item(self.tooltree.selection(), "values")[0]
            target = self.choose_Label['text'].split(' >> ')
        except:
            pass
        for item in self.tooltree.selection():
            if temp_choose in target:
                self.mytools_num.remove(temp_choose_num)
                target.remove(temp_choose)
                target =" >> ".join(target)
                self.choose_Label['text'] = target
                self.tooltree.set(item, column='#3', value=(''))
            else:
                self.mytools_num.append(temp_choose_num)
                # 勾选状态
                self.tooltree.set(item, column='#3', value=('√'))
                # 目标内容
                self.choose_Label['text'] = self.choose_Label['text']+temp_choose+' >> '

    # 清空工具
    def toolchoose_Button_f(self):
        for item in self.tooltree.get_children():
            if self.tooltree.item(item,"values")[2] == '√':
                self.tooltree.set(item, column='#3', value=(''))
        self.choose_Label['text'] = ''

    #手机ID复制（ctrl+c方法）
    def copy_pid_f(self, event):
        logging.info('已复制到剪贴板：'+(self.phonelist_tree.item(self.phonelist_tree.selection()[0], "values"))[2])
        self.root.clipboard_clear()
        self.root.clipboard_append((self.phonelist_tree.item(self.phonelist_tree.selection()[0], "values"))[2])

    # 关闭程序提示
    def closeWindow(self):
        ans = tk.messagebox.askokcancel(title='确认', message='是否要退出程序？')
        if ans:
            self.root.destroy()
        else:
            return

    # 迷你窗口
    def mini_bn_f(self):
        if self.root.winfo_width() > 285:
            self.root.geometry('285x480')
            self.mini_bn.config(text='》')
        else:
            alignstr = '%dx%d+%d+%d' % (
            1050, 600, (self.root.winfo_screenwidth() - 1050) / 2, (self.root.winfo_screenheight() - 650) / 2)

            self.root.geometry(alignstr)
            self.mini_bn.config(text='—')


    def _async_raise(self, tid, exctype):
        """raises the exception, performs cleanup if needed"""
        tid = ctypes.c_long(tid)
        if not inspect.isclass(exctype):
            exctype = type(exctype)
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
        if res == 0:
            raise ValueError("invalid thread id")
        elif res != 1:
            # """if it returns a number greater than one, you're in trouble,
            # and you should call it again with exc=NULL to revert the effect"""
            ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
            raise SystemError("PyThreadState_SetAsyncExc failed")

    def stop_thread(self, thread):
        self._async_raise(thread.ident, SystemExit)

    # RUN按钮
    def run_fun(self):
        equipment = []
        for item in self.phonelist_tree.get_children():  # 获取设备列表
            if self.phonelist_tree.item(item, "values")[0] == '√':
                equipment.append(
                    (self.phonelist_tree.item(item, "values")[1], self.phonelist_tree.item(item, "values")[2]))
        # 检查勾选状态
        if len(equipment) == 0 or len(self.mytools_num) == 0:
            if len(equipment) == 0:
                messagebox.showinfo('通知', '请先选择设备以及要执行的功能')
            elif len(self.mytools_num) == 0:
                messagebox.showinfo('通知', '请先选择要执行的功能')
            if self.root.winfo_width() == 285:
                alignstr = '%dx%d+%d+%d' % (
                    1050, 600, (self.root.winfo_screenwidth() - 1050) / 2,
                    (self.root.winfo_screenheight() - 650) / 2)
                self.root.geometry(alignstr)
                self.mini_bn.config(text='—')
            return
        # 检查配置情况
        message = ''
        for num in self.mytools_num:
            if self.config[int(num)]()==None:
                for item in self.tooltree.get_children():
                    if self.tooltree.item(item, "values")[0] == num:
                        message = message+'【'+self.tooltree.item(item, "values")[1]+'】'
        if message != '':
            messagebox.showinfo('通知', message + '\n\t功能没有配置参数')
        else:
            ThreadClass().thread_start(equipment, self.mytools_num, self.config)


