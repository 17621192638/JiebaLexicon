import binascii
import os

class BdictParser():
    def __init__(self):
        pass

    def hex2chars(self, hex_data):
        words = []
        for i in range(0, len(hex_data), 4):
            word = bytes([int(hex_data[i:i+2], 16), int(hex_data[i+2:i+4], 16)]).decode('utf-16')
            if u'\u4e00' <= word <= u'\u9fa5':
                words.append(word)
            else:
                words = []
                break
        return words

    def parse(self, content):
        words = set([])
        hex_data = binascii.hexlify(content)
        hex_data = str(hex_data, encoding='utf-8')
        hex_data = hex_data[1696:]

        while True:
            wordCount = hex_data[0:2]
            wordCount = int(wordCount, 16)
            hex_data_part = hex_data[8+wordCount*4:8+wordCount*8]
            chars = self.hex2chars(hex_data_part)
            if len(chars) < 1:
                break
            word = ''.join(chars)
            words.add(word)
            hex_data = hex_data[8+wordCount*8:]
            if len(hex_data) < 1:
                break
        return list(words)

    def parse_file(self, fileName):
        with open(fileName, "rb") as f:
            content = f.read()
        words = self.parse(content)
        return words

    def start(self,source_path,target_dir):
        if os.path.isdir(source_path):
            for source_name in os.listdir(source_path):
                self.start(source_path= source_path +"\\"+source_name,target_dir=target_dir)
        elif os.path.isfile(source_path):
            if str(source_path).lower().endswith(".bdict"):
                try:
                    words = self.parse_file(fileName=source_path)
                    with open(target_dir + "\\" + os.path.basename(source_path).split(".bdict")[0] + ".txt", 'w',
                              encoding='utf-8') as f:
                        f.writelines([str(word) + "\n" for word in words])
                    print("{0}..解析完毕".format(source_path))
                except:
                    print("{0}..解析出错".format(source_path))





if __name__ == '__main__':
    bdict_parser = BdictParser()
    # Bdict文件或者包含文件的文件夹路径
    source_path=r"E:\baidu_pinyin_ciku"
    # 目标存储文件夹路径
    target_dir =r"E:\baidu_pinyin_ciku_txt"
    res = bdict_parser.start(source_path=source_path,target_dir=target_dir)
