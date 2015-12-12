# coding: utf8
"""
Информация о строке исполняемого кода для отладчика
"""

class DebuggerCodeLine ():

	def __init__ (self):
		self.internal_id = 0
		self.external_id = 0
		self.text = ""