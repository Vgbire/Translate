# 多线程
import threading
# 线程睡眠
import time
# GUI
import tkinter
# md5
import hashlib
# 随机数
import random
# 类似软件安装选择安装路径的模块
from tkinter.filedialog import *
# 读取剪切板内容模块
import pyperclip
# html请求模块
import requests
# 解析json格式的模块
import json
# 移动文件
import shutil

# 全局路径
path = ''


class Window(object):
    # 初始化
    window = tkinter.Tk()
    # 标题
    window.title("翻译")
    # 修改图标
    window.iconbitmap('favicon.ico')

    # 设置窗口大小，并设置窗口打开在桌面的初始位置
    width = 200
    height = 120
    # 获取桌面的尺寸
    screenHeight = window.winfo_screenheight()
    screenWidth = window.winfo_screenwidth()
    align = '%dx%d+%d+%d' % (width, height, screenWidth - 1.1 * width, screenHeight - 2.1 * height)
    # print(align)
    window.geometry(align)

    # 设置窗口是否可伸缩,True可变，False不可变
    window.resizable(width=False, height=False)

    # 输入框
    txt = tkinter.Entry(window)
    txt.grid(row=0, column=0, sticky=tkinter.W + tkinter.E + tkinter.N + tkinter.S, padx=5, pady=5)
    # 绑定事件
    txt.bind("<Return>", fanyi)
    # 输出框
    result = tkinter.Entry(window)
    result.grid(row=1, column=0, sticky=tkinter.W + tkinter.E + tkinter.N + tkinter.S, padx=5, pady=5)
    # 显示当前日志文件存放目录的输入框
    var = tkinter.StringVar()
    var.set(path)
    pt = tkinter.Entry(window, textvariable=var)
    pt.grid(row=2, column=0, sticky=tkinter.W + tkinter.E + tkinter.N + tkinter.S, padx=5, pady=5)

    # 翻译按钮
    btn = tkinter.Button(window, text="翻译", command=fanyi)
    btn.grid(row=0, column=1, sticky=tkinter.W + tkinter.E + tkinter.N + tkinter.S, padx=5, pady=5)
    # 打开读取日志文件
    folder = tkinter.Button(window, text='目录', command=openFolder)
    folder.grid(row=1, column=1, sticky=tkinter.W, padx=5, pady=5)
    # 修改日志存放目录
    change = tkinter.Button(window, text='修改', command=lambda: changeFolder(pat=path))
    change.grid(row=2, column=1, sticky=tkinter.W, padx=5, pady=5)


# 打开文件的路径
def openFolder():
    os.system('explorer.exe /n,%s' % path)


# 修改日志文件存放路径
def changeFolder(pat):
    # filepath = askopenfilename(title="修改存放日志文件夹",initialdir=path)
    pt.delete(0, tkinter.END)
    filepath = askdirectory(title="修改存放日志文件夹", initialdir=pat)
    # print(filepath)
    # 定义path是全局变量path
    global path
    # 默认的目录分割符/,我们需要将其转为\，但是\要转义\\
    path = filepath.replace('/', '\\')
    # 将当前日志路径显示在pt中
    pt.insert(10, path)
    # 移动之前的日志文件，如果该文件不存在，则认为是第一次创建该日志文件
    if (os.path.exists(pat + "\\translate.log")):
        # 如果目标目录有该同名文件，则删除
        if (os.path.exists(filepath + "\\translate.log")):
            os.remove(filepath + "\\translate.log")
        # 然后移动源目录的log文件
        shutil.move(pat + "\\translate.log", filepath + "\\translate.log")


# 打开日志文件查看日志
def openFile():
    os.system('cmd /c %s' % (path + "\\translate.log"))


# 百度接口
def baiduInterface(q):
    # 这是去百度官网申请开通之后提供的参数
    appid = "20190808000325167"
    orilan = "auto"
    to = ""
    # 判断原文语言，因为原文语言设置为auto，如果是英文就设置to值为zh，否则to就转换为en
    # ord用于将一个字母转换成ASCLL对应的数字
    if (65 <= ord(q[0].upper()) <= 90):
        to = "zh"
    else:
        to = "en"
    # 生成官方要求的一个随机数
    salt = str(random.randint(1235467890, 9087654321))
    # 官方提供的密钥
    secretKey = "msPayCcPEK0QRwRYwXRt"
    # combination组合的意思
    com = appid + q + salt + secretKey
    # md5转换
    sign = hashlib.md5(com.encode(encoding='UTF-8')).hexdigest()
    # 这是按照官方要求，拼接得到的完整链接
    url = "http://api.fanyi.baidu.com/api/trans/vip/translate?q=" + q + "&from=" + orilan + "&to=" + to + "&appid=" + appid + "&salt=" + salt + "&sign=" + sign
    html = requests.get(url)
    # 弹窗提示，并不友好
    # showinfo("翻译",json.loads(html.text)["trans_result"][0]["dst"])
    # 因为申请的是普通的入口，一秒钟限制翻译一次，但是是免费的，有认证版一秒钟内可翻译10次，但是一个月内超过200W次翻译，超过的部分收费
    # 所以点击太频繁时，会返回error_code，判断json是否存在该键，存在就给出提示内容，但是用异常处理更好
    # if ("error_code" in json.loads(html.text)):
    #     result.insert(10, "别那么快！！")
    # else:
    #     src = json.loads(html.text)["trans_result"][0]["src"]
    #     dst = json.loads(html.text)["trans_result"][0]["dst"]
    #     result.insert(10, dst)
    # 异常处理，避免超过使用频率
    # 弹窗提示用户的方式不够友好，决定提示在输出栏
    try:
        # 原文
        src = json.loads(html.text)["trans_result"][0]["src"]
        # 译文
        dst = json.loads(html.text)["trans_result"][0]["dst"]
        # 清空译文显示框
        result.delete(0, tkinter.END)
        # 写入译文
        result.insert(10, dst)
        # 追加写，文件不存在则创建,在文件后面追加内容
        if (path != ''):
            with open(path + "/translate.log", "at+") as file:
                file.write(src + "\t\t\t" + dst + '\n')
    # 查看异常信息
    except Exception as msg:
        result.delete(0, tkinter.END)
        # error_code是官方json文件请求失败返回的错误信息提示json里的数据
        if ("error_code" in json.loads(html.text)):
            # print(html.text)
            # python内置的捕获异常，打印异常提示
            # print(msg)
            if (path != ""):
                # 将error_msg打印到日志里
                with open(path + "/translate.log", "at+") as file:
                    file.write(json.loads(html.text)["error_code"] + "\t\t\t" + json.loads(html.text)["error_msg"])
            if json.loads(html.text)["error_code"] == "54003":
                # 提示内容，一秒钟请求超过两次
                result.insert(10, "别那么快！！")
            else:
                # 原文里有+号传参有BUG，不是我的代码BUG，是它们网页传参的BUG，应该是当成字符串拼接的符号
                result.insert(10, "原文不能包含+号")


# 可选参数event是为了用户键入回车键执行翻译绑定的事件对象，点击按钮翻译时，不需要传参
def fanyi(*event):
    # 获取原文输入框的内容
    q = txt.get()
    if (q == ""):
        result.insert(10, "请输入。。。")
    else:
        baiduInterface(q)


# 供创建的线程调用的函数，开启线程后监听剪切板内容是否改变，改变则执行输出翻译的内容，不改变则不执行
def run():
    # 当前剪切板的值
    curValue = ""
    # 上一次剪切板的值
    lastValue = ""
    while True:
        curValue = pyperclip.paste()  # 读取剪切板复制的内容
        try:
            if curValue != lastValue:  # 如果检测到剪切板内容有改动，那么就进入文本的修改
                lastValue = curValue
                q = curValue
                baiduInterface(q)
            # 这个sleep解决了一些BUG，我也不知道为什么，感觉多线程无限运行的好像都要加个sleep才能正常，谁能告诉我为什么
            # 不信可以注释运行试试
            time.sleep(0.1)
        except KeyboardInterrupt:  # 如果有ctrl+c，那么就退出这个程序。  （不过好像并没有用。无伤大雅）
            break




# 监听剪切板内容变化线程开启
threading.Thread(target=run).start()
# 进入消息循环
window.mainloop()