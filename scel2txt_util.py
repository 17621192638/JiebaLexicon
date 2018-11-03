#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Author  : jzy
@Contact :  : 905414225@qq.com
@Software: PyCharm
@File    : scel2txt_util.py
@Time    : 2018/11/2 11:20
@Desc    :
"""
import struct
import os

# 由于原代码不适用python3且有大量bug
# 以及有函数没有必要使用且一些代码书写不太规范或冗余
# 所以本人在原有的大框架基本不动的情况下作了大量的细节更改。
# 使得没有乱码出现，文件夹导入更方便等等。
# Author：Ling Yue, Taiyuan U of Tech
# Blog: http://blog.yueling.me


# 原作者：
# 搜狗的scel词库就是保存的文本的unicode编码，每两个字节一个字符（中文汉字或者英文字母）
# 找出其每部分的偏移位置即可
# 主要两部分
# 1.全局拼音表，貌似是所有的拼音组合，字典序
#       格式为(index,len,pinyin)的列表
#       index: 两个字节的整数 代表这个拼音的索引
#       len: 两个字节的整数 拼音的字节长度
#       pinyin: 当前的拼音，每个字符两个字节，总长len
#
# 2.汉语词组表
#       格式为(same,py_table_len,py_table,{word_len,word,ext_len,ext})的一个列表
#       same: 两个字节 整数 同音词数量
#       py_table_len:  两个字节 整数
#       py_table: 整数列表，每个整数两个字节,每个整数代表一个拼音的索引
#
#       word_len:两个字节 整数 代表中文词组字节数长度
#       word: 中文词组,每个中文汉字两个字节，总长度word_len
#       ext_len: 两个字节 整数 代表扩展信息的长度，好像都是10
#       ext: 扩展信息 前两个字节是一个整数(不知道是不是词频) 后八个字节全是0
#
#      {word_len,word,ext_len,ext} 一共重复same次 同音词 相同拼音表


# 拼音表偏移，
startPy = 0x1540;

# 汉语词组表偏移
startChinese = 0x2628;

# 全局拼音表
GPy_Table = {}

# 解析结果
# 元组(词频,拼音,中文词组)的列表
GTable = []

# 原始字节码转为字符串
def byte2str(data):
    pos = 0
    str = ''
    while pos < len(data):
        c = chr(struct.unpack('H', bytes([data[pos], data[pos + 1]]))[0])
        if c != chr(0):
            str += c
        pos += 2
    return str

# 获取拼音表
def getPyTable(data):
    data = data[4:]
    pos = 0
    while pos < len(data):
        index = struct.unpack('H', bytes([data[pos],data[pos + 1]]))[0]
        pos += 2
        lenPy = struct.unpack('H', bytes([data[pos], data[pos + 1]]))[0]
        pos += 2
        py = byte2str(data[pos:pos + lenPy])

        GPy_Table[index] = py
        pos += lenPy

# 获取一个词组的拼音
def getWordPy(data):
    pos = 0
    ret = ''
    while pos < len(data):
        index = struct.unpack('H', bytes([data[pos], data[pos + 1]]))[0]
        ret += GPy_Table[index]
        pos += 2
    return ret

# 读取中文表
def getChinese(data):
    pos = 0
    while pos < len(data):
        # 同音词数量
        same = struct.unpack('H', bytes([data[pos], data[pos + 1]]))[0]

        # 拼音索引表长度
        pos += 2
        py_table_len = struct.unpack('H', bytes([data[pos], data[pos + 1]]))[0]

        # 拼音索引表
        pos += 2
        py = getWordPy(data[pos: pos + py_table_len])

        # 中文词组
        pos += py_table_len
        for i in range(same):
            # 中文词组长度
            c_len = struct.unpack('H', bytes([data[pos], data[pos + 1]]))[0]
            # 中文词组
            pos += 2
            word = byte2str(data[pos: pos + c_len])
            # 扩展数据长度
            pos += c_len
            ext_len = struct.unpack('H', bytes([data[pos], data[pos + 1]]))[0]
            # 词频
            pos += 2
            count = struct.unpack('H', bytes([data[pos], data[pos + 1]]))[0]

            # 保存
            GTable.append((count, py, word))

            # 到下个词的偏移位置
            pos += ext_len


def scel2txt(file_name):
    print('-' * 60)
    with open(file_name, 'rb') as f:
        data = f.read()

    print("词库名：", byte2str(data[0x130:0x338])) # .encode('GB18030')
    print("词库类型：", byte2str(data[0x338:0x540]))
    print("描述信息：", byte2str(data[0x540:0xd40]))
    print("词库示例：", byte2str(data[0xd40:startPy]))

    getPyTable(data[startPy:startChinese])
    getChinese(data[startChinese:])

if __name__ == '__main__':

    # scel所在文件夹路径
    in_path = r"C:\Users\90541\Desktop\text"
    # 输出词典所在文件夹路径
    out_path = r"C:\Users\90541\Desktop\text\text.txt"

    fin = [fname for fname in os.listdir(in_path) if fname[-5:] == ".scel"]
    for f in fin:
        f = os.path.join(in_path, f)
        scel2txt(f)


    # 保存结果
    with open(out_path, 'w', encoding='utf8') as f:
        f.writelines([word+'\n' for count, py, word in GTable])