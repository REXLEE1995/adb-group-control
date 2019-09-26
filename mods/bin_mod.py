import subprocess
import os
import re

class bin_mod:
    work_name = "PMTool"
    tempath = os.path.abspath('').rpartition(work_name)
    work_path = tempath[0] + tempath[1]

    def adb(self):
        '''内置adb工具路径'''
        adb = self.work_path + r'\mods\platform-tools\adb.exe '
        return adb

    def run_cmd(self, command):# 执行cmd命令
        '''执行CMD命令
        以列表形式返回执行内容'''
        output = subprocess.Popen(command, stdout=subprocess.PIPE, encoding='utf-8')
        return output.stdout.read().split("\n")

    # 实时输出
    def sh_cmd(self, command):
        p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, encoding='utf-8')
        lines = []
        for line in iter(p.stdout.readline, b''):
            print(">>>", line)
            lines.append(line)
        return lines

    def package(self, apks=1):# 获取安装包的包名
        '''通过apk文件，获取对应的包名
        参数说明：
            <apks> 默认
        返回包名组'''
        aapt = self.work_path + r'\mods\platform-tools\aapt.exe'
        packagelist = []
        if type(apks) == str:
            aapt = self.work_path + r'\mods\platform-tools\aapt.exe'
            cmd = (aapt + ' dump badging ' + apks)
            packagelist.append(re.split('[:=\' ]+', self.run_cmd(cmd)[0])[2])
            return packagelist
        else:
            apks = self.otherapk()
            for apk in apks:
                cmd = (aapt + ' dump badging ' + apk)
                packagelist.append(re.split('[:=\' ]+', self.run_cmd(cmd)[0])[2])
            return packagelist

    # 转换路径‘/，\’
    def convert_path(slef, path: str) -> str:
        return path.replace(r'\/'.replace(os.sep, ''), os.sep)
