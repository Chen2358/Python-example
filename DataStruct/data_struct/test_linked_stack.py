#coding: utf-8

class Node:

	def __init__(self, value):
		self._data = value
		self._next = None


class Stack:

	def __init__(self):
		self._top = None


	def push(self, value):
		new_node = Node(value)
		new_node.next = self._top
		self._top = new_node

	def pop(self):
		if self._top:
			value = self._top._data
			self._top =  self._top.next
			return value

	def __repr__(self):
		cur = self._top
		nums = []
		while cur:
			nums.append(cur._data)
			cur = cur.next
		return " ". join(f"{num}]" for num in nums)

if __name__ == '__main__':
	s = Stack()
	for i in range(10):
		s.push(i)
	print(s)

	for _ in range(3):
		s.pop()
	print(s)