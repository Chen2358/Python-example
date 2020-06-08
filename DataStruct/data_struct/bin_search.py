#coding: utf-8
'''
二分查找及变体
'''

def bsearch(alist, item):
	first, last = 0, len(alist) - 1
	while first <= last:
		mid = (first + last) // 2
		if item > alist[mid]:
			first = mid + 1
		elif item < alist[mid]:
			last = mid - 1
		else:
			return mid
	return -1


#递归实现
def b_search(alist, first, last, item):
    return bin_search(alist, first, last, item)

def bin_search(alist, low, high, item):
    if low > high:
        return -1
    
    mid = (low + high) // 2
    if item > alist[mid]:
        return bin_search(alist, mid+1, high, item)
    elif item < alist[mid]:
        return  bin_search(alist, low, mid-1, item)
    else:
        return mid


#第一个等于给定值的元素
def bsearch_left(alist, item):
	first, last = 0, len(alist) - 1
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

#最后一个等于给定值的元素
def bsearch_right(alist, item):
	first, last = 0, len(alist) - 1
	while first <= last:
		mid = (first + last) // 2
		if item >= alist[mid]:
			first = mid + 1
		else:
			last = mid - 1
	if last > 0 and alist[last] == item:
		return last
	else:
		return -1

if __name__ == '__main__':
	L = [1, 1, 2, 3, 4, 6, 7, 7, 7, 7, 10, 22]

	print(bsearch(L, 2))
	print(b_search(L, 0, len(L)-1, 2))

	print(bsearch_left(L, 7))
	print(bsearch_right(L, 7))
