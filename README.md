# JiebaLexicon
构建中国百科词库,作为jieba分词的自定义词库。爬取[百度输入法词库](https://shurufa.baidu.com/dict_list?cid=157),将.bdict文件解析为txt文件.
* [get_baiduciku.py](https://github.com/17621192638/JiebaLexicon/blob/master/get_baiduciku.py) 百度词库汇总代码
* [爬虫结果集 .bdict文件](https://github.com/17621192638/JiebaLexicon/tree/master/baidu_pinyin_ciku)  包含城市区划、理工行业、人文社会、电子游戏、生活百科、娱乐休闲、人名专区、文化艺术、体育运动9个大分类下的所有细分类词库
* [BdictParser.py](https://github.com/17621192638/JiebaLexicon/blob/master/BdictParser.py) 将.bdict后缀的文件解析成txt文件
* [txt解析结果集](https://github.com/17621192638/JiebaLexicon/tree/master/baidu_pinyin_ciku_txt)
* [baidu_nouns.txt](https://github.com/17621192638/JiebaLexicon/blob/master/baidu_nouns.txt)  词库汇总集合 `length 4,236,599`
