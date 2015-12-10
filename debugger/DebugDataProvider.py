# coding: utf8
"""
Данные для отладчика
"""

import json

class DebugDataProvider ():

	@classmethod
	def __init__ (cls, main_window):
		cls.STEP_TYPE_STEP_OVER = 1
		cls.STEP_TYPE_STEP_INTO_PROCEDURE = 2
		cls.STEP_TYPE_STEP_INTO_MODULE = 3
		cls.STEP_TYPE_STEP_OUT_PROCEDURE = 4
		cls.STEP_TYPE_STEP_OUT_MODULE = 5
		cls.STEP_TYPE_RUN = 6
		cls.STEP_TYPE_STOP = 7

		cls.main_window = main_window
		cls.debug_data = None
		cls.step_type = 0

	@classmethod
	def receive_data (cls):
		debug_data_str = cls.main_window.channel.receive ()
		cls.debug_data = json.loads (debug_data_str)
		if cls.debug_data != None:
			code_lines = cls.debug_data.get ('code_lines')
			if code_lines != None:
				cls.code_lines = code_lines
			cls.current_line = cls.debug_data.get ('current_line')

	@classmethod
	def send_data (cls):
		d = {
			"step_type": cls.step_type,
		}
		data = json.dumps (d, ensure_ascii = False)
		cls.main_window.channel.send (data)

	@classmethod
	def set_step_type (cls, step_type):
		cls.step_type = step_type

	@classmethod
	def update_code_text (cls):
		if cls.debug_data != None and cls.code_lines != None:
			cls.main_window.code_viewer.clear ()
			i = 1
			for code_line in cls.code_lines:
				if cls.current_line == i:
					cls.main_window.code_viewer.append ('<b>' + code_line + '</b>\n')
				else:
					cls.main_window.code_viewer.append (code_line + '\n')
				i += 1