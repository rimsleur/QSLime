# coding: utf8
"""
Данные отладчика
"""
import os
import json

class DebuggerProvider ():

	@classmethod
	def __init__ (cls):
		cls.STEP_TYPE_STEP_OVER = 1
		cls.STEP_TYPE_STEP_INTO_PROCEDURE = 2
		cls.STEP_TYPE_STEP_INTO_MODULE = 3
		cls.STEP_TYPE_STEP_OUT_PROCEDURE = 4
		cls.STEP_TYPE_STEP_OUT_MODULE = 5
		cls.STEP_TYPE_RUN = 6
		cls.STEP_TYPE_STOP = 7

		cls.dbgin = None
		cls.dbgout = None
		cls.current_procedure = ""
		cls.current_line_id = None
		cls.code_lines = []
		cls.data = ""
		cls.step_type = 0

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
		cls.data = json.dumps (d, ensure_ascii = False)

	@classmethod
	def send_data (cls):
		os.write (cls.dbgout, (cls.data + u'\n').encode ("utf-8"))

	@classmethod
	def receive_data (cls):
		data = cls.dbgin.readline ()
		d = json.loads (data)
		cls.step_type = d.get ('step_type')
		print "cls.step_type=", cls.step_type