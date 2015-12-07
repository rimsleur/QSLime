# coding: utf8
"""
Данные отладчика
"""
import json

class DebuggerProvider ():

	@classmethod
	def __init__ (cls):
		cls.dbgin = None
		cls.dbgout = None
		cls.current_procedure = ""
		cls.current_line_id = None
		cls.code_lines = []

	@classmethod
	def reset (cls):
		cls.current_procedure = ""
		cls.current_line_id = None
		#cls.code_lines.clear ()

	@classmethod
	def append_code_line (cls, text):
		if cls.current_line_id == None:
			cls.current_line_id = 0
		else:
			cls.current_line_id += 1
		cls.code_lines.append (text)

	@classmethod
	def build_debug_data (cls):
		d = {
			"current_procedure": cls.current_procedure,
			"current_line": cls.current_line_id + 1,
			"code_lines": cls.code_lines,
		}
		data = json.dumps (d, ensure_ascii = False)
		return data