#!/usr/bin/env /python3
# encodig: utf-8

'''
文本块生成器：把纯文本分成一个个文本块
'''
def lines(file):
	for line in file: yield line
	yield '\n'

def blocks(file):
	block = []
	for line in lines(file):
		if line.strip():
			block.append(line)
		elif block:
			yield ''.join(block).strip()
			block = []
