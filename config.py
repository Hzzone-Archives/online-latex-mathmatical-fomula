import utils

IMAGE_DIR = '/home/ubuntu/tuchuang/expression'

generate_way = "dvisvgm"


# 生成的方式
generate_ways = {
    "codecogs": utils.codecogs,
    "tex2svg": utils.tex2svg,
    "dvisvgm": utils.dvisvgm
}

