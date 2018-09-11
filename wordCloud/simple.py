#!/usr/bin/env python3
# coding: utf-8

import os
from os import path
from wordcloud import WordCloud

d = path.dirname(__file__)
font= os.path.join(os.path.dirname(__file__), "DroidSansFallbackFull.ttf")

#text = open(path.join(d, 'constitution.txt')).read()
text = open('santi.txt', 'r', encoding='gbk').read()

wordcloud = WordCloud(font_path=font).generate(text)

import matplotlib.pyplot as plt


plt.imshow(wordcloud)
plt.axis("off")

wordcloud = WordCloud(font_path=font, max_font_size=40).generate(text)
plt.figure()
plt.imshow(wordcloud)
plt.axis("off")
plt.show()