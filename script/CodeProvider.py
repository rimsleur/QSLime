# coding: utf8
"""
Операции с исполнимым кодом
"""
from CodeLine import CodeLine
from CodeStack import CodeStack
from SyntaxAnalyzer import SyntaxAnalyzer
from HandlerVariables import HandlerVariables
from PropositionTreeNodeType import PropositionTreeNodeType
from TreeNodeConceptType import TreeNodeConceptType
from PropositionTree import PropositionTree
from MemoryProvider import MemoryProvider
from TriggerProvider import TriggerProvider
from ConditionProvider import ConditionProvider

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
		cls.__handler_variables = []
		cls.__priorities_assigned = False

		#Переделать
		cls.TEMPL1 = "увеличивать_?что_значение_?чего"
		cls.TEMPL2 = "преобразовывать_?во-что"
		cls.TEMPL3 = "устанавливать_?что_значение_?чего"
		cls.TEMPL4 = "увеличивать_?что_значение_?чего_элемент_?чего"
		cls.TEMPL5 = "устанавливать_?что_значение_?чего_элемент_?чего"

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
	def load_procedure (cls, concept_id, list_id, handler_variables):
		cls.__procedures.append ([])
		index = len (cls.__procedures)-1
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
			#PropositionTree.print_tree (code_line.tree)
			cls.__procedures[index].append (code_line)
			cls.__procedures_keys[concept_id] = index
			
			# Раскрытие вложенных суждений
			node = code_line.tree.root_node
			if 1!=1: #node.text == "создавать":
				node.child_index = 0
				side = None
				error_text = ""
				k = 0
				while node != None:
					if node.child_index == 0:
						if node.type == PropositionTreeNodeType.concept:
							if node.concept.subroot == True:
								child, error_text = PropositionTree.replace_subtree (node, side, True, cls.__cursor)
								if child != None:
									parent.children[0] = child
						else:
							side = node.side
					if node.child_index < len (node.children):
						idx = node.child_index
						node.child_index += 1
						code_line.tree.push_node (node)
						parent = node
						node = node.children[idx]
						node.child_index = 0
						k += 1
					else:
						node = code_line.tree.pop_node ()
						k -= 1

			#PropositionTree.print_tree (code_line.tree)
			#continue

			#Поиск всех переменных в коде
			node = code_line.tree.root_node
			node.child_index = 0
			field_id = None
			list1_id = None
			element1_id = None
			k = 0
			parent = None
			while node != None:
				if node.child_index == 0:
					if node.type == PropositionTreeNodeType.concept:
						if node.concept.type == TreeNodeConceptType.field or \
						   node.concept.type == TreeNodeConceptType.element:
						   pass
						elif node.concept.type == TreeNodeConceptType.definition:
							field_id = MemoryProvider.get_field_id (node.concept.name)
							s = ""
							if field_id != None:
								#print parent.text, node.concept.name, field_id
								node1 = node.parent 
								while node1 != None:
									if s != "":
										s = node1.text + '_' + s
									else:
										s = node1.text
									node1 = node1.parent
							else:
								list1_id = MemoryProvider.get_list_id (node.concept.name)
								if list1_id != None:
									#print parent.text, node.concept.name, list1_id
									node1 = node.parent 
									while node1 != None:
										#print node1.text
										if node1.text == "элемент":
											i = 0
											node2 = node1.children[i]
											while node2 != None and node2.text != "?какой":
												node2 = node1.children[i]
												i += 1
											if node2 != None and node2.text == "?какой":
												node2 = node2.children[0]
												if node2.type == PropositionTreeNodeType.number:
													element1_id = int (node2.text)
										if s != "":
											s = node1.text + '_' + s
										else:
											s = node1.text
										node1 = node1.parent	
							if s != "":
								i = None
								vi = 0
								for v in handler_variables.variables:
									if field_id != None:
										if v[:1] == 'F':
											if int (v[1:]) == field_id:
												i = vi
												break
									elif list1_id != None:
										if v[:1] == 'L':
											n = v.find ('.')
											if n != 0:
												if int (v[1:n]) == list1_id:
													i = vi
													break
									vi += 1
								if i == None:
									if field_id != None:
										object_key = 'F' + str (field_id)
										handler_variables.variables.append (object_key)
									elif list1_id != None:
										object_key = 'L' + str (list1_id) + '.' + str (element1_id)
										handler_variables.variables.append (object_key)
									if s == cls.TEMPL1 or s == cls.TEMPL2 or s == cls.TEMPL3 \
									or s == cls.TEMPL4 or s == cls.TEMPL5:
										#print s
										handler_variables.changeable.append (True)
									else:
										#print s
										handler_variables.changeable.append (False)
								else:
									if s == cls.TEMPL1 or s == cls.TEMPL2 or s == cls.TEMPL3 \
									or s == cls.TEMPL4 or s == cls.TEMPL5:
										#print s
										if handler_variables.changeable[i] == False:
											handler_variables.changeable[i] = True

				if node.child_index < len (node.children):
					idx = node.child_index
					node.child_index += 1
					code_line.tree.push_node (node)
					parent = node
					node = node.children[idx]
					node.child_index = 0
					k += 1
				else:
					node = code_line.tree.pop_node ()
					k -= 1

		cls.__handler_variables.append (handler_variables)

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

	@classmethod
	def is_priorities_assigned (cls):
		return cls.__priorities_assigned

	@classmethod
	def assign_priorities (cls):
		variables = []
		variables.append (None)
		variables_ids = {}
		var_procs_read = []
		var_procs_read.append (None)
		var_procs_write = []
		var_procs_write.append (None)
		preproc = []
		postproc = []
		postproc_ids = {}

		for hv in cls.__handler_variables:
			#print "hv", hv.id
			vi = 0
			for v in hv.variables:
				#print "v", v, hv.changeable[vi]
				id = variables_ids.get (v)
				#print "id", id
				if id == None:
					i = len (variables)
					#print "i", i
					variables.append (v)
					variables_ids[v] = i
					var_procs_read.append ([])
					var_procs_write.append ([])
					if hv.changeable[vi] == False:
						var_procs_read[i].append (hv.id)
					else:
						var_procs_write[i].append (hv.id)
				else:
					found = False
					if hv.changeable[vi] == False:
						for vp in var_procs_read[id]:
							if vp == hv.id:
								found = True
						if found == False:
							var_procs_read[id].append (hv.id)
					else:
						for vp in var_procs_write[id]:
							if vp == hv.id:
								found = True
						if found == False:
							var_procs_write[id].append (hv.id)

				vi += 1

		"""print "----"
		vi = 0
		for v in variables:
			if v != None:
				print "v", v
				for w in var_procs_write[vi]:
					print "w", w
				for r in var_procs_read[vi]:
					print "r", r
			vi += 1
		print "----"""

		vi = 0
		for v in variables:
			if v != None:
				for w in var_procs_write[vi]:
					for r in var_procs_read[vi]:
						#print r , "->", w
						preproc.append (r)
						postproc_ids[w] = len (postproc)
						postproc.append (w)
			vi += 1
		return
		l = len (preproc)
		i = 0
		while i < l:
			if postproc_ids.get (preproc[i]):
				print "found"
			else:
				t = preproc[i][:1]
				id = int (preproc[i][1:])
				priority = 1
				#print t + str (id), priority
				if t == 'T':
					TriggerProvider.set_priority (id, priority)
				elif t == 'C':
					ConditionProvider.set_priority (id, priority)
				t = postproc[i][:1]
				id = int (postproc[i][1:])
				priority += 1
				#print t + str (id), priority
				if t == 'T':
					TriggerProvider.set_priority (id, priority)
				elif t == 'C':
					ConditionProvider.set_priority (id, priority)
			i += 1

		cls.__priorities_assigned = True