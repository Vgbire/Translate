import threading
import time
import tkinter
import hashlib
import random
from tkinter.filedialog import *
import pyperclip
import requests
import json
import shutil

path = ''


def openFolder():
    os.system('explorer.exe /n,%s' % path)


def changeFolder(pat):
    pt.delete(0, tkinter.END)
    filepath = askdirectory(title="修改存放日志文件夹", initialdir=pat)
    global path
    path = filepath.replace('/', '\\')
    pt.insert(10, path)
    if (os.path.exists(pat + "\\translate.log")):
        if (os.path.exists(filepath + "\\translate.log")):
            os.remove(filepath + "\\translate.log")
        shutil.move(pat + "\\translate.log", filepath + "\\translate.log")


def openFile():
    os.system('cmd /c %s' % (path + "\\translate.log"))


def baiduInterface(q):
    appid = "20190808000325167"
    orilan = "auto"
    to = ""
    if (65 <= ord(q[0].upper()) <= 90):
        to = "zh"
    else:
        to = "en"
    salt = str(random.randint(1235467890, 9087654321))
    secretKey = "msPayCcPEK0QRwRYwXRt"
    com = appid + q + salt + secretKey
    sign = hashlib.md5(com.encode(encoding='UTF-8')).hexdigest()
    url = "http://api.fanyi.baidu.com/api/trans/vip/translate?q=" + q + "&from=" + orilan + "&to=" + to + "&appid=" + appid + "&salt=" + salt + "&sign=" + sign
    html = requests.get(url)
    try:
        src = json.loads(html.text)["trans_result"][0]["src"]
        dst = json.loads(html.text)["trans_result"][0]["dst"]
        result.delete(0, tkinter.END)
        result.insert(10, dst)
        if (path != ''):
            with open(path + "/translate.log", "at+") as file:
                file.write(src + "\t\t\t" + dst + '\n')
    except Exception as msg:
        result.delete(0, tkinter.END)
        if ("error_code" in json.loads(html.text)):
            if (path != ""):
                with open(path + "/translate.log", "at+") as file:
                    file.write(json.loads(html.text)["error_code"] + "\t\t\t" + json.loads(html.text)["error_msg"])
            if json.loads(html.text)["error_code"] == "54003":
                result.insert(10, "别那么快！！")
            else:
                result.insert(10, "原文不能包含+号")


def fanyi(*event):
    q = txt.get()
    if (q == ""):
        result.insert(10, "请输入。。。")
    else:
        baiduInterface(q)


def run():
    curValue = ""
    lastValue = ""
    while True:
        curValue = pyperclip.paste()
        try:
            if curValue != lastValue:
                lastValue = curValue
                q = curValue
                baiduInterface(q)
            time.sleep(0.1)
        except KeyboardInterrupt:
            break


window = tkinter.Tk()
window.title("翻译")
window.iconbitmap('C:\\Users\\rookie\\PycharmProjects\\python\\Reptile\\翻译\\favicon.ico')

width = 200
height = 120
screenHeight = window.winfo_screenheight()
screenWidth = window.winfo_screenwidth()
align = '%dx%d+%d+%d' % (width, height, screenWidth - 1.1 * width, screenHeight - 2.1 * height)
window.geometry(align)

window.resizable(width=False, height=False)

txt = tkinter.Entry(window)
txt.grid(row=0, column=0, sticky=tkinter.W + tkinter.E + tkinter.N + tkinter.S, padx=5, pady=5)
txt.bind("<Return>", fanyi)

result = tkinter.Entry(window)
result.grid(row=1, column=0, sticky=tkinter.W + tkinter.E + tkinter.N + tkinter.S, padx=5, pady=5)

var = tkinter.StringVar()
var.set(path)
pt = tkinter.Entry(window, textvariable=var)
pt.grid(row=2, column=0, sticky=tkinter.W + tkinter.E + tkinter.N + tkinter.S, padx=5, pady=5)

btn = tkinter.Button(window, text="翻译", command=fanyi)
btn.grid(row=0, column=1, sticky=tkinter.W + tkinter.E + tkinter.N + tkinter.S, padx=5, pady=5)

folder = tkinter.Button(window, text='目录', command=openFolder)
folder.grid(row=1, column=1, sticky=tkinter.W, padx=5, pady=5)

change = tkinter.Button(window, text='修改', command=lambda: changeFolder(pat=path))
change.grid(row=2, column=1, sticky=tkinter.W, padx=5, pady=5)

threading.Thread(target=run).start()
window.mainloop()
