# coding: utf8
"""
Узел дерева
"""

class PropositionTreeNode ():

	def __init__ (self):
		self.type = 0
		self.parent = None
		self.children = []
		self.child_index = 0
		self.text = ""