# coding: utf8
"""
Данные отладчика
"""
import os
import json

class DebuggerProvider ():

	@classmethod
	def __init__ (cls, use):
		cls.STEP_TYPE_STEP_OVER = 1
		cls.STEP_TYPE_STEP_INTO_PROCEDURE = 2
		cls.STEP_TYPE_STEP_INTO_MODULE = 3
		cls.STEP_TYPE_STEP_OUT_PROCEDURE = 4
		cls.STEP_TYPE_STEP_OUT_MODULE = 5
		cls.STEP_TYPE_RUN = 6
		cls.STEP_TYPE_STOP = 7

		cls.use = use
		cls.dbgin = None
		cls.dbgout = None
		cls.previous_procedure_id = None
		cls.current_procedure_id = 0
		cls.current_line_id = 0
		cls.data = ""
		cls.step_type = 0
		cls.registered_procedures = {}

	@classmethod
	def reset (cls):
		cls.previous_procedure_id = None
		cls.current_procedure_id = 0
		cls.current_line_id = 0
		cls.single_code_line = ""

	@classmethod
	def set_single_code_line (cls, text):
		cls.current_line_id = 1
		cls.single_code_line = text

	@classmethod
	def build_debug_data (cls):
		d = {
			"current_procedure_id": cls.current_procedure_id,
			"current_line_id": cls.current_line_id,
		}
		if cls.current_procedure_id != cls.previous_procedure_id:
			l = []
			if cls.current_procedure_id == 0:
				l.append (cls.single_code_line)
			else:
				procedure = cls.registered_procedures.get (cls.current_procedure_id)
				for line in procedure.code_lines:
					l.append (line.text)
			d["code_lines"] = l
			#print d["code_lines"]
		cls.data = json.dumps (d, ensure_ascii = False)

	@classmethod
	def send_data (cls):
		os.write (cls.dbgout, (cls.data + u'\n').encode ("utf-8"))

	@classmethod
	def receive_data (cls):
		data = cls.dbgin.readline ()
		d = json.loads (data)
		cls.step_type = d.get ('step_type')

	@classmethod
	def register_procedure (cls, dbg_procedure):
		cls.registered_procedures[dbg_procedure.id] = dbg_procedure

	@classmethod
	def set_procedure_id (cls, procedure_id):
		cls.previous_procedure_id = cls.current_procedure_id
		cls.current_procedure_id = procedure_id

	@classmethod
	def set_line_id (cls, line_id):
		if cls.current_procedure_id != 0:
			procedure = cls.registered_procedures.get (cls.current_procedure_id)
			if procedure != None:
				cls.current_line_id = procedure.get_internal_line_id (line_id)