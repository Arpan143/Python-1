#!/usr/bin/python
# -*- coding: utf-8 -*-

import re,BeautifulSoup
from bs4 import BeautifulSoup

html_doc = """
<html>
<head>
<title>The Dormouse's story1</title>
</head>
<body>
<p class="title">
<b>The Dormouse's story2</b>
</p>

<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
</html>
"""

soup = BeautifulSoup(html_doc,'lxml') #创建BeautifulSoup对象 用lxml解析器解析
# soup = BeautifulSoup(open('index.html'),'lxml')
# print soup.prettify() #soup对象源码输出
# print soup.get_text() #soup对象文本形式输出
# print soup.a.attrs #soup对象中a标签的所有属性的字典
# print soup.a['href'] #soup对象中a标签的href属性的数值
# print soup.a.get #soup对象中a标签的所有属性 与attrs等价
# print soup.a.string #soup对象中a标签的文本 ,用来获取文件名等
# soup.a['href'] = "http://www.freebuf.com" #修改soup对象中a标签的href属性的数值
# del soup.a['href'] #删除soup对象中a标签的href属性
# print soup.head.contents #将soup对象中head标签的所有属性以列表存放
# for i in soup.find_all('a'):
    # print type(i.get('href'))
# print soup.title.string
# print soup.p.b.string
# print soup.a
# print soup.find_all('a')
# print soup.a.['href']
# print soup.find(id='link3')
# print soup.a.get_text() #将页面以文本形式获取
