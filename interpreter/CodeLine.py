# coding: utf8
"""
Строка исполняемого кода
"""

class CodeLine ():

	def __init__ (self):
	    self.id = 0
	    self.concept_id = 0
	    self.prev_line_id = 0
	    self.text = ""
	    self.field_id = 0
	    self.tree = None
	    self.priority = 1