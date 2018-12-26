# -*- coding:utf-8 -*-
# python3
from pypinyin import lazy_pinyin,load_phrases_dict
from arab2chn import ChnNumber
import sys
import os
import re
#instructions = ["开始测试","暂停","退出","运行","停止","单次触发","正常模式","放大水平时基","放大垂直分辨率","放大采样间隔","放大存储深度","缩小水平时基","缩小垂直分辨率","缩小采样间隔","缩小存储深度","打开时钟工具","打开电源工具","打开通用信号工具","打开I方C工具","打开MIIM工具","打开SPI工具","打开localbus工具","打开DDR工具","打开flash工具","打开时序工具"]

script, dir_wavs, name_pinyin_table = sys.argv

instructions = []
for wav_file in os.listdir(dir_wavs):
    if not wav_file.endswith(".wav"):
        print("Not wav file: {}".format(wav_file))
    else:
        instruction = wav_file.strip().split("_")[0]
        instructions.append(instruction)

# pinyin_instructions = dict()
#load_phrases_dict({'行':[['hang']]})

#with open("pinyin_instructions", "w") as f:
pattern = re.compile(r"[选择第][零一二三四五六七八九十百千两]+[行]")
with open(name_pinyin_table, "w") as f:
    for instruction in instructions:
        pinyin_tmp = lazy_pinyin(instruction)
        res = re.findall(pattern, instruction)
        #if instruction.endswith("行"):
        if res:
            pinyin_tmp[-1] = "Hang"
        for i,p in enumerate(pinyin_tmp):
            pinyin_tmp[i] = p.capitalize() #把第一个字母转化为大写，其余小写
        pinyin_tmp = "".join(pinyin_tmp)
        f.write(instruction + "," + pinyin_tmp)
        f.write("\n")
#    for x in range(1,10000):
#        x_chn = ChnNumber(str(x))
#        text = "选择第" + x_chn + "行"
#        if text.startswith("一十"):
#            text = text.replace("一十", "十")
#        #f.write(text + "," + pinyin_tmp)
#        #f.write("\n")
#        if "二百" in text or "二千" in text:
#            print(text)
#            text = text.replace("二百", "两百")
#            text = text.replace("二千", "两千")
#            #pinyin_tmp = lazy_pinyin(text)
#            #pinyin_tmp[-1] = "hang"
#            #pinyin_tmp = "".join(pinyin_tmp)
#        pinyin_tmp = lazy_pinyin(text)
#        pinyin_tmp[-1] = "hang"
#        pinyin_tmp = "".join(pinyin_tmp)
#        f.write(text + "," + pinyin_tmp)
#        f.write("\n")


