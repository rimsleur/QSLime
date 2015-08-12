# coding: utf8
"""
Древовидное представление суждения
"""

class CodeStack ():

	def __init__ (self):
		self.__code_stack = []
		self.__stack_index = 0

	def push (self, line):
		self.__code_stack.append (line)
		self.__stack_index += 1

	def pop (self):
		if self.__stack_index > 0:
			self.__stack_index -= 1
			return self.__code_stack.pop ()
		else:
			return None