# coding: utf8
"""
Данные контекста
"""

class ContextProvider ():

	@classmethod
	def __init__ (cls):
		cls.__field_node = None
		cls.__actor_node = None

	@classmethod
	def set_field_node (cls, node):
		cls.__field_node = node

	@classmethod
	def get_field_node (cls):
		return cls.__field_node

	@classmethod
	def set_actor_node (cls, node):
		cls.__actor_node = node

	@classmethod
	def get_actor_node (cls):
		return cls.__actor_node