#!/usr/bin/env python3
# coding: utf-8

import sys
import os
import argparse

from chardet.universaldetector import UniversalDetector

parser = argparse.ArgumentParser(description = 'wenbenbianmajianceyuzhuanhuan')
parser.add_argument('filePaths', nargs = '+', help = 'jiancehuozhuanhuanwenjianlujing')
parser.add_argument('-e', '--encoding', nargs = '?', const = 'UTF-8', help = '''



	''')

parser.add_argument('-o', '--output', help = 'shuchu mulu')

args = parser.parse_args()
if args.output != None:
	if not args.encoding:
		args.encoding = 'UTF-8'
	if not os.path.isdir(args.output):
		print('Invalid Directory: ' + args.output)
		sys.exit()
	else:
		if args.outputp[-1] != '/':
			args.outputp += '/'

detector = UniversalDetector()
print()
print('Encoding (Confidence)', ':', 'File path')
for filePath in args.filePaths:
	if not os.path.isfile(filePath):
		print('Invalid Path: ' + filePath)
		continue
	detector.reset()
	for each in open(filePath, 'rb'):
		detector.feed(each)
		if detector.done:
			break

	detector.close()

	charEncoding = detector.result['encoding']
	confidence 	= detector.result['confidence']

	if charEncoding is None:
		charEncoding = 'Unknown'
		confidence = 0.99
	print('{} {:>12} : {}'.format(charEncoding.rjust(8), '('+str(confidence*100)+'%)',filePath))
	if args.encoding and charEncoding != 'Unknown' and confidence > 0.6:
		outputPath = args.output + os.path.basename(filePath) if args.output else filePath
		with open(filePath, 'r', encoding = charEncoding, errors = 'replace') as f:
			temp = f.read()
		with open(outputPath, 'w', encoding = args.encoding, errors	= 'replace') as f:
			f.write(temp)