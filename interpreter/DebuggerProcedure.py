# coding: utf8
"""
Информация о процедуре исполняемого кода для отладчика
"""

class DebuggerProcedure ():

	def __init__ (self, id, name): 
		self.code_int_id = {}
		self.code_lines = []
		self.id = id
		self.name = name

	def append_line (self, dbg_code_line):
		self.code_lines.append (dbg_code_line)
		self.code_int_id [dbg_code_line.external_id] = dbg_code_line.internal_id

	def get_internal_line_id (self, external_line_id):
		return self.code_int_id.get (external_line_id)