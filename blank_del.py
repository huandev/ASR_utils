import os
import sys

script, path = sys.argv

for filename in os.listdir(path):
    os.rename(os.path.join(path, filename), os.path.join(path, filename.replace(" ","")))
