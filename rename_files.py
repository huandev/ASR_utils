import os
import sys
import re

script, path = sys.argv

for filename in os.listdir(path):
    os.rename(os.path.join(path, filename), os.path.join(path, filename.replace(" ","")))

for filename in os.listdir(path):
    os.rename(os.path.join(path, filename), os.path.join(path, filename.replace("，","")))
"""
for filename in os.listdir(path):
    os.rename(os.path.join(path, filename), os.path.join(path, re.sub(u"[\u4e00-\u9fa5]1.wav","_1.wav")))

for filename in os.listdir(path):
    os.rename(os.path.join(path, filename), os.path.join(path, filename.replace("2.wav","_2.wav")))

for filename in os.listdir(path):
    os.rename(os.path.join(path, filename), os.path.join(path, filename.replace("3.wav","_4.wav")))

for filename in os.listdir(path):
    os.rename(os.path.join(path, filename), os.path.join(path, filename.replace("4.wav","_4.wav")))
"""
