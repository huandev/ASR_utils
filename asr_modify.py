# -*- coding:utf-8 -*-
"""
python2
需安装 pypinyin Levenshtein
pip install pypinyin
pip install Levenshtein
"""
from pypinyin import lazy_pinyin
import os
import Levenshtein
import sys
import re
import copy
import time

threshold_dist = 10
default_instruction = "DEFAULT"
# pinyin_table =  "pinyin_table_TTS_man" #"standard_pinyin_table"  #"pinyin_table_audio_AI"


# get pinyin of instructions from file "pinyin_instructions"
def load_pinyin_table(_pinyin_table):
    pinyin_instruction = dict()
    with open(_pinyin_table, "r") as f:
        for line in f.readlines():
            instruction, pinyin = line.strip().split(",")
            # python2 转码 str --> unicode
            if type(pinyin).__name__ == 'str':
                pinyin = pinyin.decode("utf-8")
            if type(instruction).__name__ == 'str':
                pinyin = pinyin.decode("utf-8")
        
            if pinyin in pinyin_instruction.keys() and (instruction != pinyin_instruction[pinyin]):
                print("Pinyin conflict:"+ instruction + "|" + pinyin_instruction[pinyin])
        
            pinyin_instruction[pinyin] = instruction
    return pinyin_instruction
# calculate Levenshtein distance

#pinyin_instruction = load_pinyin_table(pinyin_table)

def get_predicted_instruction(_text, pinyin_instruction) :
    tic = time.time()
    _pinyin_text = lazy_pinyin(_text)
    _pinyin_raw = copy.deepcopy(_pinyin_text)
    # 首字母大写
    for i,p in enumerate(_pinyin_text):
        _pinyin_text[i] = p.capitalize() #把第一个字母转化为大写，其余小写
    #pinyin_text = "".join(pinyin_text)
    #pred_pinyin[utt_id]['pinyin'] = pinyin_text

    pattern0 = re.compile(r"[地第的定][零一二两三四五六七八九十百千]+[行航]")
    pattern1 = re.compile(r"[一二两三四五六七八九][千][零一二两三四五六七八九十百]+[行航]")
    pattern2 = re.compile(r"[地第的定].+[行航]")
        
    res0 = re.findall(pattern0, _text)
    res1 = re.findall(pattern1, _text)
    res2 = re.search(pattern2, _text)

    if res0:
        #part_ins = res[0].replace("的", "第")
        part_ins = re.sub(r"[的定地]+", "第", res0[0])
        part_ins = re.sub(r"[行航]", "行", part_ins)

        if "二百" or "二千" in part_ins:
            part_ins = part_ins.replace("二百", "两百")
            part_ins = part_ins.replace("二千", "两千")
        #sim_instruction = "选择" + part_ins 
        text_new = "选择" + part_ins
        _pinyin_text = lazy_pinyin(text_new)
        for i in range(len(_pinyin_text)):
            _pinyin_text[i] = _pinyin_text[i].capitalize()
        # "运行"等不该转换
        if text_new[-1] == "行":
            _pinyin_text[-1] = "Hang"
    elif res1:
        text_new = "选择第" + res1[0]
        if "二百" or "二千" in text:
            text = text.replace("二百", "两百")
            text = text.replace("二千", "两千")
        text_new = "选择第" + res1[0]
        for i in range(len(_pinyin_text)):
            _pinyin_text[i] = _pinyin_text[i].capitalize()
        # "运行"等不该转换
        if text_new[-1] == "行":
            _pinyin_text[-1] = "Hang"
    elif res2:
        # "运行"等不该转换
        if _text[-1] == "行":
            _pinyin_text[-1] = "Hang"
        s, e = res2.span()
        for i in range(s, e):
            if _pinyin_text[i] == "De":
                _pinyin_text[i] = "Di"
            if _pinyin_text[i] in ["Ai", "Wan", "Tai", "An"]:
                _pinyin_text[i] = "Er"
            if _pinyin_text[i] in ["Lun","Luo", "Lu"]:
                _pinyin_text[i] = "Liu"
            if (_pinyin_text[i] == "Qin") and (i+1 < e) and (_pinyin_text[i+1] == "Ai"):
                _pinyin_text[i] = "Qian"
                _pinyin_text[i+1] = "Er"
            if _pinyin_text[i] == "Ci":
                _pinyin_text[i] = "Si"
            if _pinyin_text[i] == "Qiu":
                _pinyin_text[i] = "Jiu"

    _pinyin_text = "".join(_pinyin_text)
    if "DiDi" in _pinyin_text:
        _pinyin_text = _pinyin_text.replace("DiDi", "Di")


    min_dist = 1000
    sim_instruction = None
    sim_pinyin = None
    for pinyin, instruction in pinyin_instruction.items():
        dist_tmp = Levenshtein.distance(_pinyin_text, pinyin)
        if dist_tmp < min_dist:
            min_dist = dist_tmp
            sim_instruction = instruction
            sim_pinyin = pinyin
    if min_dist > threshold_dist or len(_pinyin_text) < 3:
        sim_instruction = default_instruction

    result = {
             "min_dist": min_dist,
             "sim_instruction": sim_instruction,
             "sim_pinyin": sim_pinyin,
             "pinyin_text": _pinyin_text,
             "pinyin_raw": _pinyin_raw}
    toc = time.time()
    print("Time cost: {} s".format(toc - tic))
    return result["sim_instruction"]

if __name__ == "__main__":
    # load指令拼音表
    pinyin_table =  "./pinyin_table_TTS_man"  
    pinyin_instruction = load_pinyin_table(pinyin_table)
    
    # 修正
    text = u"选择第一百衣十行"
    instruction = get_predicted_instruction(text,  pinyin_instruction)
    print(instruction)
