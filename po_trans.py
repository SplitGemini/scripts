#!/usr/bin/python3  
# -*- coding: utf-8 -*-  
from deep_translator import GoogleTranslator
import os

def append(line):
    of.write(line+'\n')


def extend(t):
    for line in t:
        append(line)


def translate_text(text, dest, src):
    print("translate:{}".format(text), end='')
    result = GoogleTranslator(source=src, target=dest).translate(text)
    print(" to:{}".format(result))
    #print(u"Detected source language: {}".format(result["detectedSourceLanguage"]))
    count += 1
    return result
    

def avsplit(s, n):
    """
    按n长度分割s字符串，返回字符串数组
    """
    fn = len(s)//n
    if fn == 0:
        return [s]

    sr = []
    for i in range(fn):
        sr.append(s[i*n:i*n+n])
        if i == fn - 1:
            sr.append(s[i*n+n:])
    return sr


def translate(src):
    if src.isspace():
        append(src)
        return True
    # 太短，不翻译
    if len(src) <= 3:
        return False
    # 先逆转义换行符和双引号，翻译完成后按换行分割
    result = translate_text(text=src.replace('\\n','\n').replace('\\"','"'), dest='zh-cn', src='en').split('\n')
    n = 50
    if len(result) == 0:
        print("translate failed.")
        return False
    if len(result) == 1 and len(result[0]) < n:
        append("msgstr \"{}\"".format(result[0].replace('"', '\\"').replace('％','%')))
        return True
    append("msgstr \"\"")
    for i in range(len(result)):
        if i != len(result) - 1:
            # result按原文换行分割，每行再添加转义换行符
            result[i] += "\\n"
        # 重新转义双引号
        result[i] = result[i].replace('"', '\\"').replace('％','%')
        # 按长度切割
        for j in avsplit(result[i], n):
            append('"'+j+'"')

    return True
 
count = 0
msgid = ""
msgstr = ""
msgstr_reserved = []
msg_type = 0

in_name = 'cheatengine-x86_64.po'
out_name = 'result.po'
if os.path.exists(out_name):
    os.remove(out_name)
of = open(out_name, 'a+', encoding='utf-8')

with open(in_name, 'r', encoding='utf-8') as file:
    for line in file:
        line = line.replace('\n','')
        if line.startswith("msgid "):
            shouldTrans = True
            msgid = ""
            msg_type = 0
            if len(line) > 8:
                msgid += line[7:-1]
            append(line)
        elif line.startswith("msgstr "):
            msgstr = ""
            msg_type = 1
            if len(line) > 9:
                msgstr += line[8:-1]
            msgstr_reserved.append(line)
        elif line.startswith("msgctxt "):
            msg_type = 2
            append(line)
        elif line.startswith("\""):
            if msg_type == 0:
                msgid += line[1:-1]
                append(line)
            elif msg_type == 1:
                msgstr += line[1:-1]
                msgstr_reserved.append(line)
            else:
                append(line)
        else:
            if msgid and (msgid == msgstr or not msgstr):
                if not translate(msgid):
                    extend(msgstr_reserved)
                msgid = ""
                msgstr = ""
                msgstr_reserved.clear()
            elif len(msgstr_reserved) > 0:
                msgid = ""
                msgstr = ""
                extend(msgstr_reserved)
                msgstr_reserved.clear()
            append(line)

of.close()
print("Finished. Translate {} items.".format(count))