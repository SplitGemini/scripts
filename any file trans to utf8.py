#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import sys
import codecs
import chardet


def convert(file, in_enc="GBK", out_enc="UTF-8"):
    """
    该程序用于将目录下的文件从指定格式转换到指定格式，默认的是GBK转到utf-8
    :param file:    文件路径
    :param in_enc:  输入文件格式
    :param out_enc: 输出文件格式
    :return:
    """
    in_enc = in_enc.upper()
    out_enc = out_enc.upper()
    if in_enc == 'UTF-8':
        print("编码转换：" + file.split('\\')[-1] + " 已经是" + in_enc + "编码了")
        return
    try:
        print("编码转换：转换 \" " + file.split('\\')[-1] + " \" 从 " + in_enc + " --> " + out_enc)
        #GB18030兼容GB2312和GBK，避免它们出现不包含字符
        if in_enc == 'GB2312' or in_enc == 'GBK':
            in_enc = 'GB18030'
        with codecs.open(file, 'r', in_enc) as f:
            new_content = f.read()
            codecs.open(file, 'w', out_enc).write(new_content)
    # print (f.read())
    except IOError as err:
        print("I/O error: {0}".format(err))


def main(path):
    print("Path: " + path)
    i = 0
    for root, dirs, files in os.walk(sys.path[0]):  # 遍历当前文件夹
        for fileName in files:
            if '.lrc' in fileName:
                filePath = os.path.join(root,fileName)
                with open(filePath, "rb") as f:
                    data = f.read()
                    codeType = chardet.detect(data)['encoding']
                    convert(filePath, codeType, 'UTF-8')
                    i += 1
    print('有{}个{}文件被处理'.format(i, 'lrc'))


main(sys.path[0])
