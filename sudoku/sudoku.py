#-*- coding: utf-8 -*-
#!/usr/bin/env python3

import random
import itertools
from copy import deepcopy

#初始化数独二位列表
def make_board(m=3):
	#默认数独的每一个区块是3*3的
	numbers = list(range(1, m**2 +1))
	#创建一个含有所有可能的列表
	board = None

	while board is None:
		board = attempt_board(m, numbers)
	return board

#向列表中填充数字
def attempt_board(m, numbers):
	n = m ** 2

	board = [[None for _ in range(n)] for _ in range(n)]

	for i, j in itertools.product(range(n), repeat=2):
		#i,j代表行和列
		#i0和j0代表的是board[i][j]所在的区块的起始位置
		i0, j0 = i - i %m, j - j %m
		random.shuffle(numbers)
		for x in numbers:
			#分布检查行、列、区块
			if (x not in board[i]
				and all(row[j] != x for row in board)
				and all(x not in row[j0:j0+m]
						for row in board[i0:i])):
				#检查没问题就赋值
				board[i][j] = x
				break
		else:
			return  None
	return board

#打印
def print_board(board, m=3):
	numbers = list(range(1, m**2 + 1))

	#
	omit = 5
	challange = deepcopy(board)
	for i, j in itertools.product(range(omit), range(m ** 2)):
		x = random.choice(numbers) -1
		challange[x][j] =  None

	#
	spacer = "++-----+-----+-----++-----+-----+-----++-----+-----+-----++"
	print(spacer.replace('-', '='))
	for i, line in enumerate(challange):
		print("||  {}  |  {}  |  {}  ||  {}  |  {}  |  {}||  {}  |  {}  |  {}  ||"
			.format(*(cell or ' ' for cell in line)))
		if (i + 1) % 3 == 0: print(spacer.replace('-', '='))
		else: print(spacer)
	return challange

#打印答案
def print_answer(board):
	spacer = "++-----+-----+-----++-----+-----+-----++-----+-----+-----++"
	print(spacer.replace('-', '='))
	for i, line in enumerate(board):
		print("||  {}  |  {}  |  {}  ||  {}  |  {}  |  {}||  {}  |  {}  |  {}  ||"
			.format(*(cell or ' ' for cell in line)))
		if (i + 1) % 3 == 0: print(spacer.replace('-', '='))
		else: print(spacer)

if __name__ == '__main__':
	Board = make_board()
	print_board(Board)















