# coding: utf8
"""
Операции с исполнимым кодом
"""
from CodeLine import CodeLine
from CodeStack import CodeStack
from SyntaxAnalyzer import SyntaxAnalyzer

class CodeProvider ():

	@classmethod
	def __init__ (cls, cursor):
		cls.__initial_procedure = 0
		cls.__procedures = []
		cls.__procedures_keys = {}
		cls.__cursor = cursor
		cls.__current_procedure = None
		cls.__current_line = None
		cls.__current_procedures = []
		cls.__current_lines = []

	@classmethod
	def set_initial_procedure (cls, id):
		cls.__initial_procedure = id

	@classmethod
	def get_initial_procedure (cls):
		return cls.__initial_procedure

	@classmethod
	def is_procedure_already_loaded (cls, concept_id):
		id = cls.__procedures_keys.get(concept_id)
		if id != None:
			return True
		else:
			return False

	@classmethod
	def load_procedure (cls, concept_id, list_id):
		cls.__procedures.append ([])
		idx = len (cls.__procedures)-1
		query = "SELECT id, prev_line_id, text FROM qsl_list WHERE concept_id = " + str (list_id) + ";"
		cls.__cursor.execute (query)
		row = cls.__cursor.fetchone ()
		rows = []
		while (row != None):
			rows.append (row)
			row = cls.__cursor.fetchone ()
		for row in rows:
			code_line = CodeLine ()
			code_line.id = row[0]
			code_line.concept_id = list_id
			code_line.prev_line_id = row[1]
			code_line.text = row[2]
			SyntaxAnalyzer.analize (code_line.text)
			code_line.tree = SyntaxAnalyzer.proposition_tree
			#SyntaxAnalyzer.proposition_tree.print_tree ()
			cls.__procedures[idx].append (code_line)
			cls.__procedures_keys[concept_id] = idx

	@classmethod
	def execute_procedure (cls, concept_id):
		id = cls.__procedures_keys.get(concept_id)		
		if id != None:
			if cls.__current_procedure != None:
				cls.__current_procedures.append (cls.__current_procedure)
			cls.__current_procedure = id
			if cls.__current_line != None:
				cls.__current_lines.append (cls.__current_line)
			cls.__current_line = 0
			CodeStack.inside_procedure = True
			cls.prepare_next_line ()

	@classmethod
	def prepare_next_line (cls):
		if cls.__current_line < len (cls.__procedures[cls.__current_procedure]):
			CodeStack.push (cls.__procedures[cls.__current_procedure][cls.__current_line])
			cls.__current_line += 1
			return True
		else:
			if len (cls.__current_procedures) > 0:
				cls.__current_procedure = cls.__current_procedures.pop ()
			else:
				cls.__current_procedure = None
			if len (cls.__current_lines) > 0:
				cls.__current_line = cls.__current_lines.pop ()
			else:
				cls.__current_line = None
			if cls.__current_procedure == None:
				CodeStack.inside_procedure = False
			return False