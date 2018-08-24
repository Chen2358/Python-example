#!/usr/bin/env /python3
# encodig: utf-8

'''
文本块生成器：把纯文本分成一个个文本块
'''
def lines(file):
	#生成器，在文本最后加一空行
	for line in file: yield line
	yield '\n'

def blocks(file):
	#生成器，生成单独的文本块
	block = []
	for line in lines(file):
		if line.strip():
			block.append(line)
		elif block:
			yield ''.join(block).strip()
			block = []
