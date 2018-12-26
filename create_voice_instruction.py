# -*- coding: utf-8 -*-
from aliyun_voice.voice import Voice
from arab2chn import ChnNumber
import sys
#from pypinyin import lazy_pinyin


is_rename = True


auth = Voice("ALIYUNACCESSID", "ALIYUNACCESSKEY")
"""
text = "爸爸，我不回家吃饭了"
#filename="test1"
if len(sys.argv) > 1:
   text = sys.argv[1]
filename=text+".wav"
if len(sys.argv) > 2:
   filename = sys.argv[2]

auth.save_voice(text, filename, encode_type="wav")
"""
instructions = ["开始测试","暂停","退出","运行","停止","单次触发","正常模式","放大水平时基","放大垂直分辨率","放大采样间隔","放大存储深度","缩小水平时基","缩小垂直分辨率","缩小采样间隔","缩小存储深度","打开时钟工具","打开电源工具","打开通用信号工具","打开I方C工具","打开MIIM工具","打开SPI工具","打开localbus工具","打开DDR工具","打开flash工具","打开时序工具"]
num_table_special = {"0":"洞", "1":"幺", "2":"两", "3": "三", "4":"四", "5":"五", "6":"六", "7":"拐", "8":"八", "9": "勾"}
num_table_single = {"0":"零", "1":"一", "2":"二", "3": "三", "4":"四", "5":"五", "6":"六", "7":"七", "8":"八", "9": "九"}
rename_instructions = {
                       "暂停": "请暂停",
                       "运行": "开始运行",
                       "停止": "全部停止",
                       "退出": "退出操作",
                       "打开I方C工具": "打开二次方工具",
                       "打开MIIM工具": "打开物理层管理工具",
                       "打开SPI工具": "打开串行外设工具",
                       "打开DDR工具": "打开数据方向工具",
                       "打开flash工具": "打开闪存工具"}


for instruction in instructions:
    # text = instruction
    # pinyin_text = lazy_pinyin(text.decode("utf-8"))
    # filename = "".join(pinyin_text) +"_standardTTS.wav"
    if is_rename and (instruction in rename_instructions.keys()):
        text = rename_instructions[instruction]
    else:
        text = instruction
    filename = text +"_standardTTS.wav"
    auth.save_voice(text, filename, encode_type="wav")

def create_num_instructions_normal():
    # 正常读法：比如 1234 ---> 一千两百三十四
    for x in range(1,10000):
    #for x in [1234, 234]:
        x_chn = ChnNumber(str(x))
        text = "选择第" + x_chn.encode("utf-8") + "行"
        if text.startswith("选择第一十"):
            text = text.replace("选择第一十", "选择第十")
        #pinyin_text = lazy_pinyin(text.decode("utf-8"))
        filename = "".join(text) + "_standardTTS.wav"
        #auth.save_voice(text, filename, encode_type="wav")
        if "二百" in text or "二千" in text:
            print(text)
            text = text.replace("二百", "两百")
            text = text.replace("二千", "两千")
            filename = "".join(text) + "_standardTTS.wav"
        auth.save_voice(text, filename, encode_type="wav")


def create_num_instructions_single():

    # 分开读法：比如 1234 --->一二三四
    for x in range(1,10000):
    #for x in [1234, 234]:
        x = str(x)
        #text = "选择第" + x_chn.encode("utf-8") + "行"
       
        for char in x:
            x = x.replace(char, num_table_single[char])
        text = "选择第" + x + "行"
        if text.startswith("选择第一十"):
            text = text.replace("选择第一十", "选择第十")
        filename = "".join(text) + "_standardTTS.wav"
        auth.save_voice(text, filename, encode_type="wav")


def create_num_instructions_special():

    # 正常读法：比如 1234 --->一千两百三十四
    for x in range(1,10000):
    #for x in [1234, 234]:
        x = str(x)
        #text = "选择第" + x_chn.encode("utf-8") + "行"
       
        for char in x:
            x = x.replace(char, num_table_special[char])
        text = "选择第" + x + "行"
        if text.startswith("选择第一十"):
            text = text.replace("选择第一十", "十")
        filename = "".join(text) + "_standardTTS.wav"
        auth.save_voice(text, filename, encode_type="wav")


create_num_instructions_normal()
#create_num_instructions_single()
#create_num_instructions_special()

