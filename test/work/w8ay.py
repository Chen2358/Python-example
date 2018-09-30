#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from lib.core.Spider import SpiderMain
from lib.core import webcms

reload(sys)
sys.setdefaultencoding('utf-8')

def main():
	root = "https://blog.yesfree.pw/"
	threadNum = 10

	#webcms
	ww = webcms.webcms(root, threadNum)
	ww.run()
	#spider
	w8 = SpiderMain(root, threadNum)
	w8.craw()

if __name__ == '__main__':
	main()