#/usr/bin/env python3
#-*-coding: utf-8 -*-

import numpy as np
from PIL import Image
from os import path
import matplotlib.pyplot as plt
import random
import os

from wordcloud import WordCloud,STOPWORDS

font= os.path.join(os.path.dirname(__file__), "DroidSansFallbackFull.ttf")


def grey_color_func(word,font_size, position, orientation, random_state=None, **kwargs):
	return "hsl(0,0%%, %d%%)" % random.randint(60, 100)

d = path.dirname(__file__)

mask =np.array(Image.open(path.join(d, "stormtrooper_mask.png")))

text = open('santi.txt','r', encoding='gbk').read()

#
text = text.replace("chengxinshuo", "chengxin")
text = text.replace("chengxinhe","chengxin")
text = text.replace("chengxinwen","chengxin")

#
stopwords =set(STOPWORDS)
stopwords.add("int")
stopwords.add("ext")

wc = WordCloud(font_path=font, max_words=2000, mask=mask, stopwords=stopwords, margin=10, random_state=1).generate(text)

#
default_colors= wc.to_array()
plt.title("Custom colors")
plt.imshow(wc.recolor(color_func=grey_color_func, random_state=3))
wc.to_file("a_new_hope.png")
plt.axis("off")
plt.figure()
plt.title("santi-cipin tongji")
plt.imshow(default_colors)
plt.axis("off")
plt.show()