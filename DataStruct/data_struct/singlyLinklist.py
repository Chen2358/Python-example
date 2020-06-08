#coding: utf-8

class Node:
	'''Node节点'''
	def __init__(self, data, next_node=None):

		#节点中存储的数据
		self.__data = data

		#下个节点中引用地址 						
		self.__next = next_node

	@property
	def data(self):
		'''
		获取节点数据
		'''
		return self.__data

	@data.setter
	def data(self, data):
		'''
		设置节点数据
		'''
		self.__data = data

	@property
	def next_node(self):
		'''
		获取节点的next指针值
		'''
		return self.__next


	@next_node.setter
	def next_node(self, next_node):
		'''
		修改next指针
		'''
		self.__next = next_node


class SinglyLinkedList(object):
	'''
	单向链表
	'''
	def __init__(self):
		'''
		初始化
		'''
		self.__head = None

	def find_by_value(self, value):
		'''
		按值查找  
		'''
		node = self.__head
		while (node is not None) and (node.data != value):
			node = node.next_node
		return None

	def find_by_index(self, index):
		'''
		按索引查找
		'''
		node = self.__head
		pos = 0

		while (node is not None) and (pos != index):
			node = node.next_node
			pos += 1
		return node

	def insert_to_head(self, value):
		'''
		在头部插入node
		'''
		node = Node(value)

		#把node的next指向head
		node.next_node = self.__head
		#把head指向node
		self.__head = node

	def insert_after(self, node, value):
		'''
		在指定节点后插入一个node
		'''
		#如果指定的节点为空，则不插入node
		if node is None:						
			return

		new_node = Node(value)

		#把新节点的next指向指定的节点的next防止丢失
		new_node.next_node = node.next

		#把指定节点的next指向新节点
		node.next = new_node

	def insert_before(self, node, value):
		'''
		在指定节点前插入一个node
		'''
		#如果指定的节点为空，则不插入node
		if node is None:
			return

		#如果指定的节点是头节点，直接插入
		if node == self.__head:
			self.insert_to_head(value)
			return

		new_node = Node(value)
		pro = self.__head

		#如果在整个链表中都没有找到指定插入的节点，则该标记量设置为True
		not_found = False

		#寻找指定node之前的node
		while pro.next_node != node:
			#如果已经到了链表的最后一个节点，则表明改链表中没有找到指定插入的node节点
			if pro.next_node is None:
				not_found = True
				break
			else:
				pro = pro.next_node
		if not not_found:
			pro.next_node = new_node
			new_node.next_node = node

	def delete_by_node(self, node):
		'''
		在链表中删除指定的节点
		'''
		if self.__head is None:
			return

		#删除的节点是头节点
		if node == self.__head:
			self.__head = node.next_node
			return

		pro = self.__head

		#如果在整个链表中都没有找到指定插入的节点，则该标记量设置为True
		not_found = False

		while pror.next_node != node:
			#如果已经到了链表的最后一个节点，则表明改链表中没有找到指定删除的node节点
			if pro.next_node is None:
				not_found = True
				break
			else:
				pro = pro.next_node
		if not not_found:
			pro.next_node = node.next_node

	def delete_by_value(self, value):
		'''
		按值删除
		'''
		if self.__head is None:
			return

		if self.__head.data == value:
			self.__head = self.__head.next_node

		pro = self.__head
		node = self.__head.next_node
		not_found = False
		while node.data != value:
			if node.next_node is None:
				not_found = True
				break
			else:
				pro = node
				node = node.next.node
		if not_found is False:
			pro.next_node = node.next_node

	def delete_last_n_node(self, n):
		'''
		删除链表中倒数第n个节点

		思路：
			设置快、慢两个指针，慢指针不动；当快指针跨了n步后，快慢指针同时向链表尾部移动，
			当快指针到达链表尾部时，慢指针所指向的就是链表倒数第n个节点
		'''
		fast = self.__head
		slow = self.__head
		step = 0

		while step <= n:
			fast = fast.next_node
			step += 1

		while fast.next_node is not None:
			tmp = slow
			fast = fast.next_node
			slow = slow.next_node

		tmp.next_node = slow.next_node

	def find_mid_node(self):
		'''
		查找链表中的中间节点
		思路：
			设置快 、慢指针：快指针每次跨两步，慢指针每次跨一步，当快指针到达链表尾部时，慢指针指向链表的中间节点
		'''
		fast = self.__head
		slow = self.__head

		while fast.next_node is not None:
			fast = fast.next_node.next_node
			slow = slow.next_node
		return slow

	def cread_node(self, value):
		return Node(value)

	def print_all(self):
		pos = self.__head
		if pos is None:
			print('no data')
			return

		while pos.next_node is not None:
			print(str(pos.data) + "--->", end="")
			pos = pos.next_node
		print(str(pos.data))

	def reversed_self(self):
		'''链表翻转'''
		if self.__head is None or self.__head.next is None:
			return

		pre = self.__head
		node = self.__head.next
		while node is not None:
			pre, node = self.__reversed_with_two_node(pre, node)

		self.__head.next = None
		self.__head = pre

	def __reversed_with_two_node(self, pre, node):
		'''
		翻转相邻的两个节点
		pre：前一个节点
		node：当前节点	
		'''
		tmp = node.next_node
		node.next_node = pre
		pre = node
		node = tmp
		return pre, node

	def has_ring(self):
		'''
		检查链表是否有环

		思路：
			设置快、慢指针：快指针每次跨两步，慢指针每次跨一步，如果快指针没有与慢指针相遇而到达 链表尾部，则说明没有环；否则，有环
		'''
		fast = self.__head
		slow = self.__head

		while (fast.next_node is not None) and (fast is not None):
			fast = fast.next_node
			slow = slow.next_node
			if fast == slow:
				return True
		return False

if __name__ == '__main__':
	N = SinglyLinkedList()
	for i in range(15):
		N.insert_to_head(i)

	N.print_all()