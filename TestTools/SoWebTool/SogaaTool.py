#-*- coding: UTF-8 -*-

from PageOptions import *
import tkinter as tk
from tkinter import *


class App(object):

	def __init__(self, master):
		self.master = master
		self.initWidgets()

	def initWidgets(self):
		self.entry = Entry(relief=SUNKEN, font=('Courier New', 24), width=25)
		self.entry.pack(side=TOP, pady=10)
		p = Frame(self.master)
		p.pack(side=TOP)
		self.intVar = IntVar()

		li = ('搜询价', '搜订单', '搜采购', '搜仓库', '搜客户',  '搜供应商')

		i = 1
		for name in li:
			# b = Radiobutton(self.master,
			# 				text=li[i], 
			# 				variable = self.font=('Verdana', 10), width=6)
			# b.grid(row=i // 4, column= i % 4)
			tk.Radiobutton(self.master,
						   text=name,
						   variable=self.intVar,
						   # command=self.search,
						   value=i).pack(side=LEFT, fill=X, expand=YES)
			i += 1
		b = Button(self.master, text='查询', width=6, height=4, command=self.search).pack(side=TOP, fill=Y, expand=NO)

	def search(self):
		# from tkinter import messagebox
		# messagebox.showinfo(title=None, message=self.intVar.get())
		# print(self.intVar.get())	#1,2,3,4,5,6
		SoWeb = WebOptions()
		SoWeb.login()
		loc = self.intVar.get()
		text = self.entry.get()
		if loc == 1:
			SoWeb.search_sq(text)
			# print('Done')
			# print(text)
		elif loc == 2:
			SoWeb.search_so(text)
		elif loc == 3:
			SoWeb.search_sp(text)
		elif loc == 4:
			SoWeb.search_ck(text)
		elif loc == 5:
			SoWeb.search_user(text)
		else:
			SoWeb.search_supplier(text)
	

if __name__ == '__main__':

	window = Tk()
	window.title('SogaaTool')
	App(window)
	window.mainloop()