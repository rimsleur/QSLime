# coding: utf8
"""
Стэк программных инструкций для выполнения
"""

class CodeStack ():

	@classmethod
	def __init__ (cls):
		cls.__code_stack = []
		cls.__stack_index = 0

	@classmethod
	def push (self, line):
		self.__code_stack.append (line)
		self.__stack_index += 1

	@classmethod
	def pop (self):
		if self.__stack_index > 0:
			self.__stack_index -= 1
			return self.__code_stack.pop ()
		else:
			return None