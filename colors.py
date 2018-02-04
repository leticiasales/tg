# -*- coding: utf-8 -*-

import sys
from urllib2 import urlopen
import io
from colorthief import ColorThief
from colour import Color

# fd = urlopen('http://lokeshdhakar.com/projects/color-thief/img/photo1.jpg')
fd = open('../../Downloads/luleti.jpg')
f = io.BytesIO(fd.read())
color_thief = ColorThief(f)
# r,g,b = color_thief.get_color(quality=1)
# r = float(r) /255
# g = float(g) /255
# b = float(b) /255
# c = Color(rgb = (r,g,b))
# print(c.hex)
p = color_thief.get_palette(quality=1)
for i in p:
	r, g, b = i
	# print (r, g, b)
	r = float(r) /255
	g = float(g) /255
	b = float(b) /255
	c = Color(rgb = (r,g,b))
	print(c.hex)
