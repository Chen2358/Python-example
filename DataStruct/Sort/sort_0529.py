#coding: utf-8


#冒泡：O(n**2)，稳定，原地
def bubble_sort(origin_items, cmp=lambda x, y: x > y):
	items = origin_items[:]
	if len(items) == 0 or len(items) == 1:
		return items

	for i in range(1, len(items)):
		for j in range(0, len(items)-i):
			if cmp(items[j], items[j+1]):
				items[j], items[j+1] = items[j+1], items[j]
	return items

#插入：O(n**2)，稳定，原地
def insert_sort(origin_items):
	items = origin_items[:]
	if len(items) == 0 or len(items) == 1:
		return items

	for i in range(1, len(items)):
		while i > 0 and items[i-1] > items[i]:
			items[i-1], items[i] = items[i], items[i-1]
			i -= 1
	return items

#插入：O(n**2)，不稳定，原地
def select_sort(origin_items, cmp=lambda x, y: x < y):
	items = origin_items[:]
	if len(items) == 0 or len(items) == 1:
		return items

	for i in range(0, len(items)-1):
		min_index = i
		for j in range(i+1, len(items)):
			if cmp(items[j], items[min_index]):
				min_index = j
		items[i], items[min_index] = items[min_index], items[i]
	return items

#希尔：
def shell_sort(alist):
	n = len(alist)
	gap = n // 2
	i = 1

	while gap > 0:
		for j in range(gap, n):
			i = j
			while i > 0:
				if alist[i-gap] > alist[i]:
					alist[i-gap], alist[i] = alist[i], alist[i-gap]
					i -= gap
				else:
					break
		gap //= 2
	return alist

#快排：O(n*log2n), 不稳定，原地
def quick_sort(alist, first, last):
	if first >= last:
		return

	mid = alist[first]
	low = first
	high = last

	while low < high:
		while low < high and alist[high] >= mid:
			high -= 1
		alist[low] = alist[high]
		while low < high and alist[low] < mid:
			low  += 1
		alist[high] = alist[low]

	alist[low] = mid
	quick_sort(alist, first, mid-1)
	quick_sort(alist, mid+1, last)

#二分查找
def bsearch(alist, item):
	first, last = 0, len(alist)-1

	while first <= last:
		mid = (first  +  last) // 2
		if item  > alist[mid]:
			first = mid + 1
		elif item < alist[mid]:
			last = mid - 1
		else:
			return mid
	return -1

#递归实现二分查找
def b_search(alist, first, last, item):
	return binsearch(alist, first, last, item)

def binsearch(alist, first, last, item):
	if first > last:
		return 

	mid = (first + last) // 2
	if item > alist[mid]:
		return binsearch(alist, mid+1, last, item)
	elif item < alist[mid]:
		return binsearch(alist, first, mid-1, item)
	else:
		return mid

#二分查找第一个等于给定值的元素
def bsearch_left(alist, item):
	first, last = 0, len(alist)-1

	while first <= last:
		mid = (first + last) // 2
		if item > alist[mid]:
			first = mid + 1
		else:
			last = mid - 1
	if first < len(alist) and alist[first] == item:
		return first
	else:
		return -1

#二分查找最后一个等于给定值的元素
def bsearch_right(alist, item):
	first, last = 0, len(alist)-1

	while first  <= last:
		mid = (first + last) // 2
		if item >= alist[mid]:
			first = mid + 1
		else:
			last = mid - 1
	if last >= 0 and alist[last]  == item:
		return last
	else:
		return -1

def fact(n):
	return 1 if (n==0) or (n==1) else n * fact(n-1)

known = {0:1, 1: 1}
def fib(n):
	if n in known:
		return known[n]
	res = fib(n-1) + fib(n-2)
	known[n] = res
	return res


if __name__ == '__main__':
	import random

	L = list(range(10))

	random.shuffle(L)
	print("L:   ", L)
	L_B = bubble_sort(L)
	print("L_B: ", L_B)

	random.shuffle(L)
	print("L:   ", L)
	L_I = insert_sort(L)
	print("L_I: ", L_I)

	random.shuffle(L)
	print("L:   ", L)
	L_S = select_sort(L)
	print("L_S: ", L_S)

	random.shuffle(L)
	print("L:   ", L)
	L_shell = shell_sort(L)
	print("L_shell: ", L_shell)

	random.shuffle(L)
	print("L:   ", L)
	quick_sort(L, 0, len(L)-1)
	print("L_Q: ", L)

	L1 = [1, 1, 2, 3, 4, 6, 7, 7, 7, 7, 10, 22]
	print(bsearch(L1, 3))
	print(b_search(L1, 0, len(L1)-1, 3))

	print(bsearch_left(L1, 7))
	print(bsearch_right(L1, 7))

	print([fact(x) for x in range(10)])
	print([fib(x) for x in range(10)])






