# coding: utf8
"""
Данные для отладчика
"""

import json

class DebugDataProvider ():

	@classmethod
	def __init__ (cls, main_window):
		cls.main_window = main_window
		cls.debug_data = None

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