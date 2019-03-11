#-*- coding: utf-8 -*-
#!/usr/bin/env python3

from sudoku import *

def is_full(challange, m=3):
	for i, j in itertools.product(range(m**2), repeat=2):
		if challange[i][j] is None:
			return False
	return True

def cal_candidate(challenge, x, y, m=3):
	candidate = list(range(1, m**2 + 1))
	for i in range(m**2):
		#
		if challange[x][i] in candidate:
			candidate.remove(challange[x][i])
		#
		if challange[i][y] in candidate:
			candidate.remove(challange[i][y])
	#
	for i, j in itertools.product(range(m), repeat=2):
		#
		x0, y0 = x - x % m, y - y % m
		if challange[x0+i][y0+j] in candidate:
			candidate.remove(challange[x0+i][y0+j])
	return candidate


def least_candidate(challange, m=3):
	least, x, y = m ** 2, -1, -1
	for i, j in itertools.product(range(m**2), repeat=2):
		if not challange[i][j]:
			num = len(cal_candidate(challange, i, j))
			if num < least:
				least = num
				x, y = i, j
	return x, y

def solving_sudoku(challange, m=3):
	#
	if is_full(challange):
		return challange

	#
	x, y = least_candidate(challange)

	#
	id = x * (m**2) + y

	#
	result = try_candidate(challange, id)
	return result

def try_candidate(challange, id, m=3):
	#
	if is_full(challange):
		return challange

	#
	x = id // (m**2)
	y = id % (m**2)

	#
	while challange[x][y]:
		id = (id + 1) % m**4
		x = id // (m**2)
		y = id % (m**2)
	candidate = cal_candidate(challange, x, y)

	#
	if len(candidate) == 0:
		return False

	#
	for i in range(len(candidate)):
		challange[x][y] = candidate[i]

		#
		result_r = try_candidate(challange, (id + 1) % m ** 4)
		if not result_r:
			#
			pass
		else:
			return challange
	challange[x][y] = None
	return False

if __name__ == '__main__':
	Board = make_board()
	challange = print_board(Board)

	wait = input("PRESS ENTER TO SHOW THE ANSWER")
	print("RAW ANSWER")
	print_answer(Board)
	print('Calculated from your program: ')
	result = solving_sudoku(challange)
	print_answer(result)