#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import json

__all__ = ['password']

#规定特征
NUMBER = re.compile(r'[0-9]')
LOWER_CASE = re.compile(r'[a-z]')
UPPER_CASE = re.compile(r'[A-Z]')
OTHERS = re.compile(r'[^0-9a-zA-Z]')

#检测常用密码
def load_common_password():
	words = []
	with open('10k_most_common.txt', 'rb') as f:
		for word in f.readlines():
			words.append(word.strip().decode(encoding="utf-8"))
	return words

COMMON_WORDS = load_common_password()


class Strength:
	#定义密码强度
	def __init__(self, valid, strength, message):
		self.valid = valid
		self.strength = strength
		self.message = message

	def __repr__(self):
		return self.strength

	def __str__(self):
		return self.message

	def __bool__(self):
		return self.valid


class Password:

	TERRIBLE = 0
	SIMPLE = 1
	MEDIUM = 2
	STRONG = 3

	@staticmethod
	def is_regular(input):
		reverse = input[::-1]
		regular = ''.join(['qwertyuiop', 'asdfghjkl', 'zxcvbnm'])
		return input in regular or reverse in regular

	@staticmethod
	def is_by_step(input):
		delta = ord(input[1]) - ord(input[0])

		for i in range(2, len(input)):
			if ord(input[i]) - ord(input[i-1]) != delta:
				return False
		return True

	@staticmethod
	def is_common(self):
		return input in COMMON_WORDS


	def __call__(self, input, min_length=6, min_types=3, level=STRONG):
		if len(input) < min_length:
			return Strength(False, 'Terrible', 'mimataiduanle')

		if self.is_regular(input) or self.is_by_step(input):
			return Strength(False, 'simple', 'mimayouguize')

		if self.is_common(input):
			return Strength(False, 'simple', 'mimahenchangjian')

		types = 0

		if NUMBER.search(input):
			types += 1

		if LOWER_CASE.search(input):
			types += 1

		if UPPER_CASE.search(input):
			types += 1

		if OTHERS.search(input):
			types += 1

		if types < 2:
			return Strength(level <= self.SIMPLE, 'simple', 'mimataijiandanle')

		if types < min_types:
			return Strength(level <= self.MEDIUM, 'medium', 'mimabugouqiang')

		return Strength(True, 'strong', 'wanmei')



class Email:

	#
	def __init__(self, email):
		self.email = email

	#
	def isValidEmail(self):
		if re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", self.email) != None:
			return True
		return False

	#
	def getEmailType(self):
		type = 'qq' or '163' or 'gmail' or '126' or 'sina'
		emailtype = re.search('@\w+', self.email).group()[1:]
		if emailtype in type:
			return emailtype
		return 'your email is wrong!'

		
password = Password()

