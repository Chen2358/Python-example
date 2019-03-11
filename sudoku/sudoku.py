#-*- coding: utf-8 -*-
#!/usr/bin/env python3

import random
import itertools
from copy import deepcopy

def make_board(m=3):
	#
	numbers = list(range(1, m**2 +1))
	#
	board = None

	while board is None:
		board = attempt_board(m, numbers)
	return board

#
def attempt_board(m, numbers):
	n = m ** 2

	board = [[None for _ in range(n)] for _ in range(n)]

	for i, j in itertools.product(range(n), repeat=2):
		#
		#
		i0, j0 = i - i %m, j - j %m
		random.shuffle(numbers)
		for x in numbers:
			#
			if (x not in board[i]
				and all(row[j] != x for row in board)
				and all(x not in row[j0:j0+m]
						for row in board[i0:i])):
				#
				board[i][j] = x
				break
		else:
			return  None
	return board

#
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

#
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















