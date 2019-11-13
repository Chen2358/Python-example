#-*- coding: utf-8 -*-

from reportlab.graphics.shapes import Drawing, String
from reportlab.graphics import renderPDF

#创建指定尺寸的Drawing对象
d = Drawing(100, 100)
#创建指定属性的图形元素
s = String(50, 50, 'Hello World!', textAnchor='middle')


#将图形元素添加到Drawing对象
d.add(s)

#以PDF渲染Drawing对象，并保存
renderPDF.drawToFile(d, 'hello.pdf', 'A simple PDF file')