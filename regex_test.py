# coding: utf-8
import re

pattern = re.compile(r"[第的][零一二两三四五六七八九十百千]+行")
pattern = re.compile(r"[第的地].+行")
"""
while 1:
    s = input("input string: ")
    #m = pattern.match(s)
    res = re.findall(pattern, s)
    #print(m.group())
    print(res)
    r = re.search(pattern,s)
    print(r)
    if r:
        print(r.span())
        print(r.group())
"""
s = input("input string: ")
s_new = re.sub(r"[的定]+", "第", s)
print(s_new)
