# coding: utf8
"""
Узел дерева
"""

class PropositionTreeNode ():

	def __init__ (self):
		self.type = 0
		self.side = None
		self.parent = None
		self.children = []
		self.child_index = 0
		self.text = ""
		self.concept = None
		self.linkage = None