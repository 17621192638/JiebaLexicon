#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@Author  : jzy
@Contact :  : 905414225@qq.com
@Software: PyCharm
@File    : get_baiduciku.py
@Time    : 2018/11/2 15:36
@Desc    : 爬取 百度输入法 词库 https://shurufa.baidu.com/dict
"""
import urllib.request
from bs4 import BeautifulSoup

def get_web_url(cid,page_num):
    return "https://shurufa.baidu.com/dict_list?cid={0}&page={1}#page".format(cid,page_num)
def file_download_url(file_id):
    return "https://shurufa.baidu.com/dict_innerid_download?innerid={0}".format(file_id)
def get_files(file_path,ids):   # 获取所有文件的链接地址
    for cid in ids:
        for i in range(1,1000):
            print("{0}..当前页{1}开始".format(cid["name"],str(i)))
            web_url = get_web_url(cid=cid["id"],page_num=i)
            res = urllib.request.urlopen(url=web_url)
            soup = BeautifulSoup(res.read(),"lxml")
            file_url_list = soup.find_all("a",{"class":"dict-down dictClick","dict-innerid":True})
            if file_url_list:
                for file_url in file_url_list:
                    file_name = file_url.get("dict-name")
                    file_id = file_url.get("dict-innerid")
                    print("正在下载文件...{0}".format(file_name))
                    try:
                        urllib.request.urlretrieve(url=file_download_url(file_id=file_id),filename=file_path+"/{0}_{1}_{2}.bdict".format(cid["name"],file_name,file_id))
                        print("文件下载到本地成功...{0}".format(file_name))
                    except:
                        continue
            else:
                print("{0}...当前类别的词库已经爬取完毕".format(cid["name"]))
                break
    print("词库全部爬取完毕")

if __name__ == '__main__':
    # 下载.bdict文件的保存路径
    file_save_path = "E:/baidu_pinyin_ciku"
    # 百度拼音词库内的所有种类ID  https://shurufa.baidu.com/dict
    ids = [{"id": 157, "name": "城市规划"}, {"id": 158, "name": "理工行业"}, {"id": 317, "name": "人文社科"},
           {"id": 162, "name": "电子游戏"}, {"id": 159, "name": "生活百科"}, {"id": 163, "name": "娱乐休闲"},
           {"id": 165, "name": "人名专区"}, {"id": 160, "name": "文化艺术"}, {"id": 161, "name": "体育运动"},
           ]
    get_files(file_path=file_save_path,ids=ids)