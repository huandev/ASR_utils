# -*- coding:utf-8 -*-
import Levenshtein

while 1:
    str1 = input("str1:")
    str2 = input("str2:")

    dist = Levenshtein.distance(str1, str2)
    print(dist)
