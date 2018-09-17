#!/usr/bin/env python3
#-*-coding: utf-8 -*-

from MyQR import myqr 

# myqr.run('https://www.baidu.com')

myqr.run(
	words = 'https://www.baidu.com',
	picture = 'Sources/gakki.gif',
	colorized = True,
	save_name = 's.gif')