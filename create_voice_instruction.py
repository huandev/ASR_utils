# -*- coding: utf-8 -*-
#python2.7
from aliyun_voice.voice import Voice
from arab2chn import ChnNumber
import sys
import os
#from pypinyin import lazy_pinyin
import shutil
import re


#reload(sys)
#sys.setdefaultencoding('utf-8')

dir_save_voices = sys.argv[1]
is_rename = True

if os.path.exists(dir_save_voices):
    shutil.rmtree(dir_save_voices)    #递归删除文件夹
os.mkdir(dir_save_voices)

#auth = Voice("ALIYUNACCESSID", "ALIYUNACCESSKEY")
with open("api_key", "r") as f_key:
    for line in f_key.readlines():
        ID, KEY = line.strip().split(",")
ID = ID.strip()
KEY = KEY.strip()
auth = Voice(ID, KEY)
encode_type = "wav" # default: pcm
voice_name = "xiaogang" # default: xiaoyun
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
                       "暂停": "暂停测试",
                       "运行": "开始运行",
                       "停止": "停止运行",
                       "退出": "退出测试",
                       "打开I方C工具": "打开二次方工具",
                       "打开MIIM工具": "打开物理层管理工具",
                       "打开SPI工具": "打开串行外设工具",
                       "打开DDR工具": "打开数据方向工具",
                       "打开flash工具": "打开闪存工具",
                       "打开localbus工具": "打开本地总线工具"}


def create_nonum_instructions():
    for instruction in instructions:
        # text = instruction
        # pinyin_text = lazy_pinyin(text.decode("utf-8"))
        # filename = "".join(pinyin_text) +"_standardTTS.wav"
        if is_rename and (instruction in rename_instructions.keys()):
            text = rename_instructions[instruction]
        else:
            text = instruction
        filename = text +"_standardTTS.wav"
        auth.save_voice(text, os.path.join(dir_save_voices, filename), encode_type=encode_type, voice_name=voice_name)

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
        auth.save_voice(text, os.path.join(dir_save_voices, filename), encode_type=encode_type, voice_name=voice_name)
        #auth.save_voice(text, filename, encode_type="wav")


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
        #auth.save_voice(text, filename, encode_type="wav")
        auth.save_voice(text, os.path.join(dir_save_voices, filename), encode_type=encode_type, voice_name=voice_name)


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
        #auth.save_voice(text, filename, encode_type="wav")
        auth.save_voice(text, os.path.join(dir_save_voices, filename), encode_type=encode_type, voice_name=voice_name)

def create_some_instructions(path_instructions):
    pattern = re.compile(r"第[零一二三四五六七八九十百千两]+行")
    with open(path_instructions, "r") as f_ins:
        for i,line in enumerate(f_ins.readlines()):
            line_clean = line.strip()
            text = line_clean
            filename = "".join(text) + "_standardTTS.wav"
            if "二百" in text or "二千" in text:
                print(text)
                text = text.replace("二百", "两百")
                text = text.replace("二千", "两千")
                filename = "".join(text) + "_standardTTS.wav"
            res = re.findall(pattern, text)
            #print(res[0])
            #new_num = re.sub("", "|", res[0])
            #new_num = res[0].encode("utf-8").replace(u"", u",") #.encode("utf-8")

            if res:
                # decode:str-->unicode    encode: str-->decode
                new_num = res[0].decode("utf-8").replace("",",")[:-1]
                new_num = new_num.encode("utf-8")
                text = "选择" + new_num
		#print(type(text))
                print(text)
           
            auth.save_voice(text, os.path.join(dir_save_voices, filename), encode_type=encode_type, voice_name=voice_name)
    print("------{} records-------".format(i+1))


def create_voice():
    print("ok")
    while 1:
        text = raw_input("Text: ")
        filename = raw_input("filename: ")
        #filename = "".join(text) + "_TTS.wav"
        auth.save_voice(text, os.path.join(dir_save_voices, filename), encode_type=encode_type, voice_name=voice_name)

if __name__ == "__main__":
    #create_nonum_instructions()
    #create_num_instructions_normal()
    #create_num_instructions_single()
    #create_num_instructions_special()
    path_instructions = "data/errors_TTS_man"
    create_some_instructions(path_instructions)
    #create_voice()
