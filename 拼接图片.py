#!/usr/bin/python3
# -*- coding: utf-8 -*-
import math
from PIL import Image
import random
 
"""
合并图片
"""


def combineImgFromSourse(raw, col, list):
    """
    根据源图片合并新图
    """
    ## Todo
    return
    
def combineImg(list, dst_size):
    """
    根据新图要求合并源图片
    """
    target = Image.new('RGB', dst_size)
    imgs = [Image.open(i) for i in list]
    for raw in range(12):
        for col in range(6):
            target.paste(imgs[random.randint(0,len(list)-1)], (200*col, 200*raw))
    #target.show()
    target.save('reading__reading_themes_vine_yellow.jpg')

size = (1080, 2400)
list_im = [r'reading__reading_themes_vine_yellow1.jpg', r'reading__reading_themes_vine_yellow2.jpg',
            r'reading__reading_themes_vine_yellow3.jpg']
combineImg(list_im, size)