python tk/ttk制作 安卓群控助手，多台设备多任务多线程执行
```
仅供学习，禁止商用，转载请注明出处。
```

**更新记录**：



20190926  |  重大更新，将页面重构，代码重构，交互更加方便，任务模快完成，整个程序可以正常运行，并稳定运行。
20190826  |  初版成型，页面布局已经完成，但任务执行模块未实现

# 简介
第一次使用python的tkinter库，一个python简单的GUI编程库
通过ADB命令去控制手机，同时使用多线程，对手机进行批量操作，如，多台设备同时安装软件，生成通讯录测试数据等。
由于公司测试组的工作需要，简单开发的安卓手机助手，有助于提升工作效率。

## 工具界面
![简洁模式](https://img-blog.csdnimg.cn/20190926144821994.png)
![展开功能后](https://img-blog.csdnimg.cn/20190926145008708.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L1ZJUDUxODYwMA==,size_16,color_FFFFFF,t_70)

 1. **手机列表**：主要是获取已连接当前电脑的安卓设备；
 2. **工具列表**：加载已写好的单个工具，比如软件安装、软件卸载等，可以自由扩展多个用于对设备进行控制的小工具；
 3. **工具配置**：针对小工具编写的配置页面，方便进行工具参数的设定，比如生成通讯录数据的条数，安装软件的软件路径，软件卸载的包名。
 4. **执行顺序**：小工具执行的执行顺序，比如先进行软件安装，再进行软件卸载，最后进行通讯录生成。


## 代码结构
![在这里插入图片描述](https://img-blog.csdnimg.cn/20190926145306878.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L1ZJUDUxODYwMA==,size_16,color_FFFFFF,t_70)
- <font color=red>PM2</font>
  * <font color=red>mods</font>
    + <font color=red>platform-tools</font>
    + _ init _.py
    + bin_mod.py
    + get_vcardfile.py
    + getphone_mod.py
    + logger_mod.py
    + thread_mod.py
  * <font color=red>page</font>
  	+ png
  	+ _ init _ .py
  	+ mainpg.py
  	+ mainpg_fun.py
  * <font color=red>toolpg</font>
  	+ _ init _.py
  	+ _1_软件安装_.py
  	+ _2_软件卸载_.py
  	+ _3_通讯录_.py
  	+ ..................
  * <font color=red>tools</font>
    + _1_tool.py
  	+ _2_tool.py
  	+ _3_tool.py
  	+ ............
  * run.py
## 代码内容
__mods__：存放一些公共方法，比如获取已连接的手机列表，获取本地adb工具，直接cmd命令的方法目录
__platform-tools__：为了能使工具在其他windows上可用，我在这里添加了一个自有的adb工具包，直接调用即可，即使本地电脑上没有装adb环境。
![在这里插入图片描述](https://img-blog.csdnimg.cn/20190826150456424.png)
__bin_mod.py__：具体的公共方法文件，含有一系列自定义的方法

```python
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

```
__get_vcardfile.py__：通讯录生成模块，可以生成对应数量的通讯录条数，便于导入到手机端生成数据，通讯录工具模块所调用的文件
```python
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  2 08:40:20 2019

@author: REXLEE
"""

import random
import quopri
import logging

from .bin_mod import bin_mod

work_path = bin_mod.work_path # 获取工作目录

# 生成中文名（百家姓任选一，名字在常用选2个）  
def gen_name():
    first_names = ['赵', '钱', '孙', '李', '周', '吴', '郑', '王', '冯', '陈', '褚', '卫', '蒋', '沈', '韩', '杨', '朱', '秦', '尤', '许',
                    '何', '吕', '施', '张', '孔', '曹', '严', '华', '金', '魏', '陶', '姜', '戚', '谢', '邹', '喻', '柏', '水', '窦', '章',
                    '云', '苏', '潘', '葛', '奚', '范', '彭', '郎', '鲁', '韦', '昌', '马', '苗', '凤', '花', '方', '俞', '任', '袁', '柳',
                    '酆', '鲍', '史', '唐', '费', '廉', '岑', '薛', '雷', '贺', '倪', '汤', '滕', '殷', '罗', '毕', '郝', '邬', '安', '常',
                    '乐', '于', '时', '傅', '皮', '卞', '齐', '康', '伍', '余', '元', '卜', '顾', '孟', '平', '黄', '和', '穆', '萧', '尹',
                    '姚', '邵', '堪', '汪', '祁', '毛', '禹', '狄', '米', '贝', '明', '臧', '计', '伏', '成', '戴', '谈', '宋', '茅', '庞',
                    '熊', '纪', '舒', '屈', '项', '祝', '董', '梁']
    last_names = ['的', '一', '是', '了', '我', '不', '人', '在', '他', '有', '这', '个', '上', '们', '来', '到', '时', '大', '地', '为',
                   '子', '中', '你', '说', '生', '国', '年', '着', '就', '那', '和', '要', '她', '出', '也', '得', '里', '后', '自', '以',
                   '会', '家', '可', '下', '而', '过', '天', '去', '能', '对', '小', '多', '然', '于', '心', '学', '么', '之', '都', '好',
                   '看', '起', '发', '当', '没', '成', '只', '如', '事', '把', '还', '用', '第', '样', '道', '想', '作', '种', '开', '美',
                   '总', '从', '无', '情', '己', '面', '最', '女', '但', '现', '前', '些', '所', '同', '日', '手', '又', '行', '意', '动',
                   '方', '期', '它', '头', '经', '长', '儿', '回', '位', '分', '爱', '老', '因', '很', '给', '名', '法', '间', '斯', '知',
                   '世', '什', '两', '次', '使', '身', '者', '被', '高', '已', '亲', '其', '进', '此', '话', '常', '与', '活', '正', '感',
                   '见', '明', '问', '力', '理', '尔', '点', '文', '几', '定', '本', '公', '特', '做', '外', '孩', '相', '西', '果', '走',
                   '将', '月', '十', '实', '向', '声', '车', '全', '信', '重', '三', '机', '工', '物', '气', '每', '并', '别', '真', '打',
                   '太', '新', '比', '才', '便', '夫', '再', '书', '部', '水', '像', '眼', '等', '体', '却', '加', '电', '主', '界', '门',
                   '利', '海', '受', '听', '表', '德', '少', '克', '代', '员', '许', '稜', '先', '口', '由', '死', '安', '写', '性', '马',
                   '光', '白', '或', '住', '难', '望', '教', '命', '花', '结', '乐', '色', '更', '拉', '东', '神', '记', '处', '让', '母',
                   '父', '应', '直', '字', '场', '平', '报', '友', '关', '放', '至', '张', '认', '接', '告', '入', '笑', '内', '英', '军',
                   '候', '民', '岁', '往', '何', '度', '山', '觉', '路', '带', '万', '男', '边', '风', '解', '叫', '任', '金', '快', '原',
                   '吃', '妈', '变', '通', '师', '立', '象', '数', '四', '失', '满', '战', '远', '格', '士', '音', '轻', '目', '条', '呢',
                   '病', '始', '达', '深', '完', '今', '提', '求', '清', '王', '化', '空', '业', '思', '切', '怎', '非', '找', '片', '罗',
                   '钱', '紶', '吗', '语', '元', '喜', '曾', '离', '飞', '科', '言', '干', '流', '欢', '约', '各', '即', '指', '合', '反',
                   '题', '必', '该', '论', '交', '终', '林', '请', '医', '晚', '制', '球', '决', '窢', '传', '画', '保', '读', '运', '及',
                   '则', '房', '早', '院', '量', '苦', '火', '布', '品', '近', '坐', '产', '答', '星', '精', '视', '五', '连', '司', '巴',
                   '奇', '管', '类', '未', '朋', '且', '婚', '台', '夜', '青', '北', '队', '久', '乎', '越', '观', '落', '尽', '形', '影',
                   '红', '爸', '百', '令', '周', '吧', '识', '步', '希', '亚', '术', '留', '市', '半', '热', '送', '兴', '造', '谈', '容',
                   '极', '随', '演', '收', '首', '根', '讲', '整', '式', '取', '照', '办', '强', '石', '古', '华', '諣', '拿', '计', '您',
                   '装', '似', '足', '双', '妻', '尼', '转', '诉', '米', '称', '丽', '客', '南', '领', '节', '衣', '站', '黑', '刻', '统',
                   '断', '福', '城', '故', '历', '惊', '脸', '选', '包', '紧', '争', '另', '建', '维', '绝', '树', '系', '伤', '示', '愿',
                   '持', '千', '史', '谁', '准', '联', '妇', '纪', '基', '买', '志', '静', '阿', '诗', '独', '复', '痛', '消', '社', '算',
                   '义', '竟', '确', '酒', '需', '单', '治', '卡', '幸', '兰', '念', '举', '仅', '钟', '怕', '共', '毛', '句', '息', '功',
                   '官', '待', '究', '跟', '穿', '室', '易', '游', '程', '号', '居', '考', '突', '皮', '哪', '费', '倒', '价', '图', '具',
                   '刚', '脑', '永', '歌', '响', '商', '礼', '细', '专', '黄', '块', '脚', '味', '灵', '改', '据', '般', '破', '引', '食',
                   '仍', '存', '众', '注', '笔', '甚', '某', '沉', '血', '备', '习', '校', '默', '务', '土', '微', '娘', '须', '试', '怀',
                   '料', '调', '广', '蜖', '苏', '显', '赛', '查', '密', '议', '底', '列', '富', '梦', '错', '座', '参', '八', '除', '跑',
                   '亮', '假', '印', '设', '线', '温', '虽', '掉', '京', '初', '养', '香', '停', '际', '致', '阳', '纸', '李', '纳', '验',
                   '助', '激', '够', '严', '证', '帝', '饭', '忘', '趣', '支', '春', '集', '丈', '木', '研', '班', '普', '导', '顿', '睡',
                   '展', '跳', '获', '艺', '六', '波', '察', '群', '皇', '段', '急', '庭', '创', '区', '奥', '器', '谢', '弟', '店', '否',
                   '害', '草', '排', '背', '止', '组', '州', '朝', '封', '睛', '板', '角', '况', '曲', '馆', '育', '忙', '质', '河', '续',
                   '哥', '呼', '若', '推', '境', '遇', '雨', '标', '姐', '充', '围', '案', '伦', '护', '冷', '警', '贝', '著', '雪', '索',
                   '剧', '啊', '船', '险', '烟', '依', '斗', '值', '帮', '汉', '慢', '佛', '肯', '闻', '唱', '沙', '局', '伯', '族', '低',
                   '玩', '资', '屋', '击', '速', '顾', '泪', '洲', '团', '圣', '旁', '堂', '兵', '七', '露', '园', '牛', '哭', '旅', '街',
                   '劳', '型', '烈', '姑', '陈', '莫', '鱼', '异', '抱', '宝', '权', '鲁', '简', '态', '级', '票', '怪', '寻', '杀', '律',
                   '胜', '份', '汽', '右', '洋', '范', '床', '舞', '秘', '午', '登', '楼', '贵', '吸', '责', '例', '追', '较', '职', '属',
                   '渐', '左', '录', '丝', '牙', '党', '继', '托', '赶', '章', '智', '冲', '叶', '胡', '吉', '卖', '坚', '喝', '肉', '遗',
                   '救', '修', '松', '临', '藏', '担', '戏', '善', '卫', '药', '悲', '敢', '靠', '伊', '村', '戴', '词', '森', '耳', '差',
                   '短', '祖', '云', '规', '窗', '散', '迷', '油', '旧', '适', '乡', '架', '恩', '投', '弹', '铁', '博', '雷', '府', '压',
                   '超', '负', '勒', '杂', '醒', '洗', '采', '毫', '嘴', '毕', '九', '冰', '既', '状', '乱', '景', '席', '珍', '童', '顶',
                   '派', '素', '脱', '农', '疑', '练', '野', '按', '犯', '拍', '征', '坏', '骨', '余', '承', '置', '臓', '彩', '灯', '巨',
                   '琴', '免', '环', '姆', '暗', '换', '技', '翻', '束', '增', '忍', '餐', '洛', '塞', '缺', '忆', '判', '欧', '层', '付',
                   '阵', '玛', '批', '岛', '项', '狗', '休', '懂', '武', '革', '良', '恶', '恋', '委', '拥', '娜', '妙', '探', '呀', '营',
                   '退', '摇', '弄', '桌', '熟', '诺', '宣', '银', '势', '奖', '宫', '忽', '套', '康', '供', '优', '课', '鸟', '喊', '降',
                   '夏', '困', '刘', '罪', '亡', '鞋', '健', '模', '败', '伴', '守', '挥', '鲜', '财', '孤', '枪', '禁', '恐', '伙', '杰',
                   '迹', '妹', '藸', '遍', '盖', '副', '坦', '牌', '江', '顺', '秋', '萨', '菜', '划', '授', '归', '浪', '听', '凡', '预',
                   '奶', '雄', '升', '碃', '编', '典', '袋', '莱', '含', '盛', '济', '蒙', '棋', '端', '腿', '招', '释', '介', '烧', '误',
                   '乾', '坤']
    return random.choice(first_names) + random.choice(last_names) + random.choice(last_names)

# 生成电话号码（任选一个3位开头，后面8位随机生成）   
def gen_tel():
    prelist=["130","131","132","133","134","135","136","137","138","139","147","150","151","152","153","155","156","157","158","159","186","187","188", "177", "176"]
    return random.choice(prelist)+"".join(random.choice("0123456789") for i in range(8))

# 创建一个vcard（名字需要使用QUOTED-PRINTABLE编码）
def gen_vcard(name, tel):
    vcard = "BEGIN:VCARD" + '\n' + \
        "VERSION:2.1" + '\n' + \
        "N;CHARSET=UTF-8;ENCODING=QUOTED-PRINTABLE:;" + name + ";;;" + '\n' + \
        "FN;CHARSET=UTF-8;ENCODING=QUOTED-PRINTABLE:" + name + '\n' + \
        "TEL;CELL:" + tel + '\n' + \
        "TEL;HOME:" + tel + '\n' + \
        "EMAIL;HOME:123@abc.com" + '\n' + \
        "ADR;HOME;CHARSET=UTF-8;ENCODING=QUOTED-PRINTABLE:;;=E5=9C=B0=E5=9D=80;;;;" + '\n' + \
        "END:VCARD" + '\n'
    return vcard

def get_vcardfile(numb):
    path = work_path+'\\temp\\_vcard_temp\\'
    if int(numb) > 0:
        try:
            f = open(path+'contacts.vcf', 'w')
            counts = int(numb)
            for x in range(1, counts + 1):
                name = gen_name().encode('utf8')
                name = str(quopri.encodestring(name))[2:-1]
                f.write(gen_vcard(name, gen_tel()))
            f.close()
        except:
            logging.info('生成失败')
    else:
        logging.info('生成数量不正确')
```


__getphone_mod.py__：获取已连接设备的列表
```python
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
```
__logger_mod.py__：日志模块

```python
# -*- coding: utf-8 -*-
"""
Created on Wed Jul  3 09:21:06 2019

@author: REXLEE
"""

import logging
import datetime
from .bin_mod import bin_mod

work_path = bin_mod().work_path

def logger_mod(loglevel=logging.DEBUG):
    logpath = work_path+'\\temp\\_run_log\\'
    logging.basicConfig(
            level = loglevel,
            filename = logpath+"%s.log" % (datetime.datetime.now().strftime('%Y-%m-%d')), #文件名称
            datefmt = '%m-%d %H:%M:%S',#日期格式
            format = '%(asctime)-4s File \'%(pathname)s\', line %(lineno)d, in %(funcName)s(), %(levelname)s -> %(message)s', #格式
            filemode = 'w')#文件模式
    # 将日志输出到控制台
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('in %(filename)s, line %(lineno)d, %(levelname)s -> %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)

if __name__=="__main__":
    print('不支持单独运行文件，请运行run.py')
```
__thread_mod.py__：线程模块
```python
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  2 15:05:29 2019

@author: REXLEE
"""

from threading import Thread
import logging
import datetime
import importlib


class ThreadClass:

    def thread_start(self, equipment, toollist, config):#线程执行方法
        self.threads = []
        #运行开始，记录开始时间
        self.starttime = datetime.datetime.now()
        logging.info('运行开始时间：%s' % self.starttime.strftime('%H:%M:%S'))
        for phone in equipment:
            thread = Thread(target=Plan().myplan, args=(phone, toollist, config,))
            thread.start()
            # self.threads.append(thread)
        # for thread in self.threads:
        #     thread.join()


class Plan:

    def myplan(self, phone, toollist, config):
        for num in toollist:
            tempimport = importlib.import_module('tools.'+'_'+num+'_tool')
            temp = tempimport.toolclass(phone, config[int(num)]())
            temp.start()

```

__page__：用于存放整个工具的页面代码，以及页面逻辑等文档
__png__：用于存放整个工具页面中 所用到的一些图标文件

![在这里插入图片描述](https://img-blog.csdnimg.cn/20190926150740991.png)

类似与下方中的run图标

![在这里插入图片描述](https://img-blog.csdnimg.cn/20190926150816330.png)

__main.py__：主要为整个工具的界面相关的代码，生成界面的样式
PS：更新后，主要对这部分内容进行了更新，将其中的功能代码完全剥离出来，放到了后面的 main_fun.py 的文件中，此文件中，完全为静态的界面代码

```python
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

```
__main_fun.py__：整个工具的页面交互逻辑方法文件
```python
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

```
~~__run_fun.py__：工具中的Start按钮的功能，用于启动任务的执行按钮，我单独给他写一个文件，是因为它需要给任务开启多线程，<font color=red>内容我暂时没有写，后续添加进去。</font>~~

<font color=red>PS：run_fun.py的内容，已经完全写到了，main_fun.py中的
run_fun()方法
</font>

__toolpg__：存放每个小工具的配置页面，比如通讯录小工具，我们需要进行生成数量的设置，那么这个页面就负责与用户交互
![在这里插入图片描述](https://img-blog.csdnimg.cn/20190926151554560.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L1ZJUDUxODYwMA==,size_16,color_FFFFFF,t_70)
~~\__init.py__: 这里的py文件为 __toolpg__ 目录中的__ init __.py文件，目的是使得当前目录变为python package目录，其中我添加了一些代码，使得当前的目录中的所有py文件，自动导包 __mainpg.py__ 中，以至于，我每次添加新的工具时，不用在 __mainpg.py__ 中进行import的操作~~

PS：目前\__init__.py文件内容为空，我已经在*main.py*中使用了动态导
包模块‘importlib’

___1_软件安装_.py__： 此类文件为小工具前端页面文件，生成工具的配置页面，我这里约定以此方式命名，便于我对小工具进行排序，小工具在页面上的名称。
```python
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
        self.filename = tkinter.filedialog.askopenfilename(title=u"选择文件",filetypes=[("apk格式", "apk")])
        self.entry_apk_package.delete(0, END)
        self.entry_apk_package.insert(0, self.filename)

    def _Bn_search_F2(self):
        self.filename = tkinter.filedialog.askdirectory(title=u"选择文件夹")
        self.entry_apk_path.insert(0, self.filename)
      
    def getconfig(self):
        if self.entry_apk_package.get()=='' and self.entry_apk_path.get()=='':
            return None
        else:
            return (self.entry_apk_package.get(), self.entry_apk_path.get())
```
___2_卸载安装_.py__： 卸载软件的页面
```python
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

```
___3_通讯录_.py__： 生成通讯录的页面
```python
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
```
__tools__：前面的toolpg目录中的类似与‘___3_通讯录_.py’这种文件，主要是前端界面文件，作用是生成一个配置的页面，但页面的功能，是由tools目录中的对应工具实现
___1_tool.py__:此文件与“___1_安装软件_.py”对应，此文件为执行文件，真正去做软件安装的操作，而“___1_安装软件_.py”只是去渲染出一个配置页面，供用户去做配置，比如安装哪一个软件，需要用户在这个页面上去选择apk文件，“_1_tool.py”文件读取到配置文件中的所选apk然后进行安装
```python
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
```
___2_tool.py__:此文件与“___2_卸载软件_.py”对应，此文件为执行文件，真正去做软件卸载的操作，而“___2_卸载软件_.py”只是去渲染出一个配置页面，供用户去做配置，比如卸载哪一个软件，需要用户在这个页面上去选择apk文件（选择apk后，程序会读取出apk对应的包名，如果手机上存在此包名，就进行卸载），或者直接输入包名，“_2_tool.py”文件读取到配置文件中的包名后，进行卸载
```python
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
```
___2_tool.py__:此文件与“___3_通讯录_.py”对应。
```python
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
```

__run.py__：执行此文件即可启动程序，我写的比较简单，当然你可以在此文件中添加logging功能，进行一些其他初始化的工作
```python
# -- coding: utf-8 --

from mods import logger_mod
from page.mainpg_fun import *

logger_mod.logger_mod()
root = Tk()
Mainpg_fun(root)
root.mainloop()

```

__run.bat__:双击执行run.py
```
@echo off
python run.py
```
当程序完成后，并且可以正常运行，即可对软件进行打包，最后生成“.exe”文件。
打包方式


但以上程序代码，已经可以完整的加载出一个正常的程序页面，并且页面中的一些交互功能都是正常可用的，后续将不再更新，其中的工具，可以自由扩展，界面可以自动识别并加载。
https://blog.csdn.net/VIP518600/article/details/100074420

本文适合想学习tk\ttk模块的朋友，再完全不了解的情况下，按照上方的结构进行编写，并且可以成功运行。
```
仅供学习，禁止商用，转载请注明出处。
```
