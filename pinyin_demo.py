# -*- coding:utf-8 -*-
#from __future__ import input
#python3
from pypinyin import lazy_pinyin,load_phrases_dict
import sys

while 1:
    s = input("Input string:  ")
    pinyin = lazy_pinyin(s)
    for i in range(0, len(pinyin)):
        pinyin[i] =  pinyin[i].capitalize() #首字母大写
    
    print(pinyin)
    print("".join(pinyin))
