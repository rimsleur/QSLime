# coding: utf8
"""
Стек программных инструкций для выполнения
"""

class CodeStack ():

	@classmethod
	def __init__ (cls):
		cls.__code_stack = []
		cls.__stack_index = 0
		cls.inside_procedure = False

	@classmethod
	def push (cls, line):
		cls.__code_stack.append (line)
		cls.__stack_index += 1
		#print "->", line.text

	@classmethod
	def pop (cls):
		if cls.__stack_index > 0:
			cls.__stack_index -= 1
			return cls.__code_stack.pop ()
		else:
			return None

	@classmethod
	def is_empty (cls):
		if cls.__stack_index == 0:
			return True
		else:
			return False

	@classmethod
	def sort (cls):
		for line in cls.__code_stack:
			#print "->", line.text
			pass
		r = len (cls.__code_stack) - 1
		i = 0
		while i < r:
			j = r
			while j > i:
				if cls.__code_stack[j-1].priority < cls.__code_stack[j].priority:
					e = cls.__code_stack[j-1]
					cls.__code_stack[j-1] = cls.__code_stack[j]
					cls.__code_stack[j] = e
				j -= 1
			i += 1
		for line in cls.__code_stack:
			#print "->", line.text
			pass
		#stop = stop