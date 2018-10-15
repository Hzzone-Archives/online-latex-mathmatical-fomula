import utils
import config
from tqdm import tqdm
import os
import shutil

# 测试命令行生成svg的速度

with open('Corpus_part4_2016.txt') as f:
    lines = f.readlines()
    lines = [line.strip('\n') for line in lines]
    lines = [line.strip('$') for line in lines]


# ~70k 的数学公式，来源于 [crohme](https://www.isical.ac.in/~crohme/) 提供的数据集
# 在 13' mbp 15 early 测试，大概不到 2s 一个公式，有点慢了...

# test_count = len(lines)
test_count = 10

shutil.rmtree(config.IMAGE_DIR)
os.mkdir(config.IMAGE_DIR)

for line in tqdm(lines[:test_count]):
    utils.tex2svg(line, 'svg', config.IMAGE_DIR)

shutil.rmtree(config.IMAGE_DIR)
os.mkdir(config.IMAGE_DIR)

for line in tqdm(lines[:test_count]):
    utils.codecogs(line, 'svg', config.IMAGE_DIR)

shutil.rmtree(config.IMAGE_DIR)
os.mkdir(config.IMAGE_DIR)

for line in tqdm(lines[:test_count]):
    utils.dvisvgm(line, 'svg', config.IMAGE_DIR)
