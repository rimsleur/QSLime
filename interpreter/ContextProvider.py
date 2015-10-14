# coding: utf8
"""
Данные контекста
"""

class ContextProvider ():

	@classmethod
	def __init__ (cls):
		cls.__field_node = None
		cls.__constant_node = None
		cls.__actor_node = None
		cls.__trigger_node = None
		cls.__condition_node = None
		cls.__list_node = None
		cls.__element_node = None

	@classmethod
	def set_field_node (cls, node):
		cls.__field_node = node

	@classmethod
	def get_field_node (cls):
		return cls.__field_node

	@classmethod
	def set_constant_node (cls, node):
		cls.__constant_node = node

	@classmethod
	def get_constant_node (cls):
		return cls.__constant_node

	@classmethod
	def set_actor_node (cls, node):
		cls.__actor_node = node

	@classmethod
	def get_actor_node (cls):
		return cls.__actor_node

	@classmethod
	def set_trigger_node (cls, node):
		cls.__trigger_node = node

	@classmethod
	def get_trigger_node (cls):
		return cls.__trigger_node

	@classmethod
	def set_condition_node (cls, node):
		cls.__condition_node = node

	@classmethod
	def get_condition_node (cls):
		return cls.__condition_node

	@classmethod
	def set_list_node (cls, node):
		cls.__list_node = node

	@classmethod
	def get_list_node (cls):
		return cls.__list_node

	@classmethod
	def set_element_node (cls, node):
		cls.__element_node = node

	@classmethod
	def get_element_node (cls):
		return cls.__element_node