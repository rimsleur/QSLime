# coding: utf8
"""
Древовидное представление суждения
"""

from PropositionTreeNode import PropositionTreeNode
from PropositionTreeNodeType import PropositionTreeNodeType
from PropositionTreeNodeSide import PropositionTreeNodeSide
from LanguageHelper import LanguageHelper
from ContextProvider import ContextProvider
from TreeNodeConcept import TreeNodeConcept
from DatabaseTriad import DatabaseTriad
from DatabaseSequence import DatabaseSequence
from DatabaseConcept import DatabaseConcept
from MemoryProvider import MemoryProvider
from TreeNodeConceptType import TreeNodeConceptType

class PropositionTree ():

	def __init__ (self):
		self.root_node = None
		self.__node_stack = []
		self.__stack_index = 0
		self.is_totally_parsed = False

	def push_node (self, node):
		self.__node_stack.append (node)
		self.__stack_index += 1

	def pop_node (self):
		if self.__stack_index > 0:
			self.__stack_index -= 1
			return self.__node_stack.pop ()
		else:
			return None

	@classmethod
	def print_tree (cls, tree):
		node = tree.root_node
		node.child_index = 0
		k = 0
		print "<Печать древовидной структуры суждения>"
		while node != None:
			if node.child_index == 0:
				if node.type == PropositionTreeNodeType.concept:
					if node.concept.subroot == True:
						print "    "*k + "+" + node.text
					elif node.concept.sublink == True:
						print "    "*k + "=" + node.text
					else:
						print "    "*k + node.text
				else:
					print "    "*k + node.text

			if node.child_index < len (node.children):
				idx = node.child_index
				node.child_index += 1
				tree.push_node (node)
				node = node.children[idx]
				node.child_index = 0
				k += 1
			else:
				node = tree.pop_node ()
				k -= 1
		print "</Печать древовидной структуры суждения>"

	@classmethod
	def get_actor_and_actant (cls, root_node):
		idx = 0
		actor = None
		actant = None
		while idx < len (root_node.children):
			child = root_node.children[idx]
			if child.type == PropositionTreeNodeType.linkage:
				if child.linkage.name == LanguageHelper.translate ("who") or child.linkage.name == LanguageHelper.translate ("what"):
					parent = child
					child = child.children[0]
					if child.type == PropositionTreeNodeType.concept:
						if child.side == PropositionTreeNodeSide.left:
							actor = child
							if root_node.concept.subroot != True:
								ContextProvider.set_actor_node (actor)
						elif child.side == PropositionTreeNodeSide.right:
							actant = child
			if actor != None and actant != None:
				break
			idx += 1
		if actor == None:
			actor = ContextProvider.get_actor_node ()
		return actor, actant

	@classmethod
	def replace_subtree (cls, root_node, side, is_new, cursor):
		actor, actant = PropositionTree.get_actor_and_actant (root_node)
		result_node = PropositionTreeNode ()
		result_node.type = PropositionTreeNodeType.concept
		result_node.side = side
		result_node.concept = TreeNodeConcept ()
		is_memobject = False
		error_text = ""

		if root_node.concept.name == LanguageHelper.translate ("to-have"):
			if actant.concept.name == LanguageHelper.translate ("name"):
				if actor.concept.name == LanguageHelper.translate ("field"):
					child1 = actant.children[0]
					if child1.type == PropositionTreeNodeType.linkage:
						if child1.linkage.name == LanguageHelper.translate ("which"):
							child2 = child1.children[0]
							if child2.type == PropositionTreeNodeType.concept:
								if is_new == True:
									result_node.concept.id = MemoryProvider.create_field (child2.concept.name)
									is_memobject = True
									result_node.concept.type = TreeNodeConceptType.field
									result_node.concept.name = "$" + str (result_node.concept.id)
									result_node.text = result_node.concept.name
									ContextProvider.set_field_node (result_node)
								else:
									result_node.concept.id = MemoryProvider.get_field_id (child2.concept.name)
									is_memobject = True
									result_node.concept.type = TreeNodeConceptType.field
									result_node.concept.name = "$" + str (result_node.concept.id)
									result_node.text = result_node.concept.name
				elif actor.concept.name == LanguageHelper.translate ("list"):
					child1 = actant.children[0]
					if child1.type == PropositionTreeNodeType.linkage:
						if child1.linkage.name == LanguageHelper.translate ("which"):
							child2 = child1.children[0]
							if child2.type == PropositionTreeNodeType.concept:
								if is_new == True:
									result_node.concept.id = MemoryProvider.create_list (child2.concept.name)
									is_memobject = True
									result_node.concept.type = TreeNodeConceptType.memlist
									result_node.concept.name = "$" + str (result_node.concept.id)
									result_node.text = result_node.concept.name
									ContextProvider.set_list_node (result_node)
								else:
									result_node.concept.id = MemoryProvider.get_list_id (child2.concept.name)
									is_memobject = True
									result_node.concept.type = TreeNodeConceptType.memlist
									result_node.concept.name = "$" + str (result_node.concept.id)
									result_node.text = result_node.concept.name
				elif actor.concept.name == LanguageHelper.translate ("procedure"):
					child1 = actant.children[0]
					if child1.type == PropositionTreeNodeType.linkage:
						if child1.linkage.name == LanguageHelper.translate ("which"):
							child2 = child1.children[0]
							if child2.type == PropositionTreeNodeType.concept:
								database_triad = DatabaseTriad.read (cursor, actant.concept.id, child1.linkage.id, child2.concept.id)
								if database_triad == None:
									error_text = ErrorHelper.get_text (105)
									return None, error_text
								database_sequense1 = DatabaseSequence.read (cursor, 0, 0, database_triad.id)
								if database_sequense1 == None:
									error_text = ErrorHelper.get_text (105)
									return None, error_text
								database_triad = DatabaseTriad.read_by_id (cursor, database_sequense1.left_triad_id)
								if database_triad == None:
									error_text = ErrorHelper.get_text (105)
									return None, error_text
								if database_triad.left_concept_id == root_node.concept.id:
									database_sequense2 = DatabaseSequence.read (cursor, database_sequense1.proposition_id, 0, database_triad.id)
									if database_sequense2 == None:
										error_text = ErrorHelper.get_text (105)
										return None, error_text
									database_triad = DatabaseTriad.read_by_id (cursor, database_sequense2.left_triad_id)
									if database_triad == None:
										error_text = ErrorHelper.get_text (105)
										return None, error_text
									result_node.concept.id = database_triad.left_concept_id
									database_concept = DatabaseConcept.read_by_name (cursor, LanguageHelper.translate ("to-be"))
									if database_concept == None:
										error_text = ErrorHelper.get_text (104)
										return None, error_text
									database_triad1 = DatabaseTriad.read (cursor, result_node.concept.id, 0, database_concept.id)
									if database_triad1 == None:
										error_text = ErrorHelper.get_text (104)
										return None, error_text
									database_triad2 = DatabaseTriad.read (cursor, database_concept.id, 0, actor.concept.id)
									if database_triad2 == None:
										error_text = ErrorHelper.get_text (104)
										return None, error_text
									database_sequense3 = DatabaseSequence.read (cursor, 0, database_triad1.id, database_triad2.id)
									if database_sequense3 == None:
										error_text = ErrorHelper.get_text (104)
										return None, error_text
								else:
									error_text = ErrorHelper.get_text (105)
									return None, error_text
		if is_memobject != True:
			if result_node.concept.id != 0:
				database_concept = DatabaseConcept.read_by_id (cursor, result_node.concept.id)
				result_node.concept.type = database_concept.type
				result_node.concept.name = database_concept.name
				result_node.text = result_node.concept.name
			else:
				return None, error_text

		return result_node, error_text