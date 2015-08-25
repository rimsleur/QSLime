# coding: utf8
"""
Древовидное представление суждения
"""

from PropositionTreeNodeType import PropositionTreeNodeType

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

	def print_tree (self):
		node = self.root_node
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
				self.push_node (node)
				node = node.children[idx]
				node.child_index = 0
				k += 1
			else:
				node = self.pop_node ()
				k -= 1
		print "</Печать древовидной структуры суждения>"