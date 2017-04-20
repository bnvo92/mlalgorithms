from os import path
import numpy as np
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import heapq
from PIL import Image
import random


def grey_color_func(word, font_size, position, orientation, random_state=None,
                    **kwargs):
    return "hsl(0, 0%%, %d%%)" % random.randint(60, 100)

text = open('avengers_script.txt','r', encoding='utf-8').read()

stopwords = set(STOPWORDS)
stopwords.add('INT')
stopwords.add('EXT')

mask = np.array(Image.open('avengers-logo-stencil.jpg'))

wc = WordCloud(max_words=1000, stopwords=stopwords, mask=mask,
               margin = 10).generate(text)

default_colors = wc.to_array()
plt.figure(figsize=(10,8),facecolor='k')
plt.imshow(wc.recolor(color_func=grey_color_func, random_state=3),
           interpolation="bilinear")
plt.axis('off')
plt.figure()
plt.imshow(default_colors, interpolation="bilinear")
plt.axis('off')
plt.show()



def ulti(w_cloud,text, n):
    d = w_cloud.process_text(text)
    maximums = {k: d[k] for k in heapq.nlargest(n, d, key = lambda k:d[k])}
    X = np.arange(len(maximums))
    Y = maximums.values()
    plt.figure()
    plt.bar(X,Y, align='center')
    plt.xticks(X, maximums.keys(), rotation='vertical')
    plt.ylabel('Frequency')
    plt.title('%r Most Frequent Words' %n)
    plt.show()
    return maximums

