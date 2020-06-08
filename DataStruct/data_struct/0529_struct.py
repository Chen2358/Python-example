#coding: utf-8

'''
#堆

class Stack:

	def __init__(self):
		self.__list = []

	def push(self, item):
		self.__list.append(item)

	def pop(self):
		return self.__list.pop()


#链表实现堆

class Node:

	def __init__(self, data):
		self._data = data
		self._next = None

class LinkedStack:

	def __init__(self):
		self._top = None

	def push(self, value):
		new_node = Node(value)
		new_node._next = self._top
		self._top = new_node

	def pop(self):
		if self._top:
			value = self._top._data
			self._top = self._top._next
			return value

	def __repr__(self):
		cur = self._top
		nums = []

		while cur:
			nums.append(cur._data)
			cur = cur._next
		return " ".join(f"{num}]" for num in nums)

if __name__ == '__main__':
	s = Stack()
	for i in range(10):
		s.push(i)
	print(s.pop())

	s1 =  LinkedStack()
	for i in range(10):
		s1.push(i)
	print(s1)

	for _ in range(3):
		s1.pop()
	print(s1)
'''
'''
#队列

class Queue:

	def __init__(self):
		self.__list = []

	def enqueue(self, value):
		self.__list.append(value)

	def dequeue(self):
		return self.__list.pop(0)

#双端队列

class Dqueue:

	def __init__(self):
		self.__list  =  []

	def add_front(self, value):
		self.__list.insert(0, value)

	def add_rear(self, value):
		self.__list.append(value)

	def pop_front(self):
		return self.__list.pop(0)

	def pop_rear(self):
		return  self.__list.pop()

if __name__ == '__main__':
	q = Queue()
	dq = Dqueue()

	q.enqueue(1)
	q.enqueue(2)
	q.enqueue(3)

	print(q.dequeue())

	dq.add_front(1)
	dq.add_front(2)
	dq.add_rear(4)
	dq.add_rear(3)	#2,1,4,3

	print(dq.pop_front())
	print(dq.pop_rear())
'''

#二叉树

class Node:

	def __init__(self, value):
		self.elem = value
		self.lchild = None
		self.rchild = None

class Tree:

	def __init__(self):
		self.root = None

	def add(self, item):
		node = Node(item)

		if self.root is None:
			self.root = node
			return

		queue = [self.root]
		while queue:
			cur = queue.pop(0)
			if cur.lchild is None:
				cur.lchild = node
				return
			queue.append(cur.lchild)
			if cur.rchild is None:
				cur.rchild = node
				return
			queue.append(cur.rchild)

	def breave_trave(self):
		if self.root is None:
			return

		queue = [self.root]
		while queue:
			cur = queue.pop(0)
			print(cur.elem, end=" ")
			if cur.lchild is not None:
				queue.append(cur.lchild)
			if cur.rchild is not None:
				queue.append(cur.rchild)

	def preorder(self, node):
		if node is None:
			return

		print(node.elem, end=" ")
		self.preorder(node.lchild)
		self.preorder(node.rchild)

	def inorder(self, node):
		if node is None:
			return

		self.inorder(node.lchild)
		print(node.elem,  end=" ")
		self.inorder(node.rchild)

	def postorder(self, node):
		if node is None:
			return

		self.postorder(node.lchild)
		self.postorder(node.rchild)
		print(node.elem, end=" ")

if __name__ == '__main__':
	tree = Tree()
	for i in range(10):
		tree.add(i)

	tree.breave_trave()
	print()
	tree.preorder(tree.root)
	print()

	tree.inorder(tree.root)
	print()
	tree.postorder(tree.root)




































