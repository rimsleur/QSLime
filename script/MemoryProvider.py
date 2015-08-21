# coding: utf8
"""
Данные в оперативной памяти
"""

from ListElement import ListElement
from ListElementType import ListElementType

class MemoryProvider ():

	@classmethod
	def __init__ (cls):
		cls.__fields = []
		cls.__fields.append (None)
		cls.__last_field_index = 0
		cls.__field_name_dict = {}
		cls.__lists = []
		cls.__lists.append (None)
		cls.__last_list_index = 0
		cls.__list_name_dict = {}

	@classmethod
	def create_field (cls, name):
		id = cls.get_field_id (name)
		if id != None:
			return id
		else:
			cls.__fields.append (None)
			cls.__last_field_index += 1
			cls.__field_name_dict[name] = cls.__last_field_index
			return cls.__last_field_index

	@classmethod
	def get_field_id (cls, name):
		return cls.__field_name_dict.get (name)

	@classmethod
	def get_field_value (cls, id):
		return cls.__fields[id]

	@classmethod
	def set_field_value (cls, id, value):
		cls.__fields[id] = value

	@classmethod
	def print_all_fields (cls):
		print cls.__field_name_dict.items ()

	@classmethod
	def create_list (cls, name):
		id = None
		if name != "":
			id = cls.get_list_id (name)
		if id != None:
			return id
		else:
			cls.__lists.append ([None])
			cls.__last_list_index += 1
			if name != "":
				cls.__list_name_dict[name] = cls.__last_list_index
			return cls.__last_list_index

	@classmethod
	def get_list_id (cls, name):
		return cls.__list_name_dict.get (name)

	@classmethod
	def add_list_element (cls, list_id):
		element = ListElement()
		cls.__lists[list_id].append (element)
		return len (cls.__lists[list_id]) - 1

	@classmethod
	def get_list_element_value (cls, list_id, element_id):
		list = cls.__lists[list_id]
		if list[element_id].type == ListElementType.field:
			return list[element_id].value
		else:
			return None

	@classmethod
	def set_list_element_value (cls, list_id, element_id, value):
		list = cls.__lists[list_id]
		list[element_id].type = ListElementType.field
		list[element_id].value = value

	@classmethod
	def set_list_element_ref_list (cls, list_id, element_id, ref_list_id):
		list = cls.__lists[list_id]
		list[element_id].type = ListElementType.list
		list[element_id].reference = ref_list_id

	@classmethod
	def get_list_element_ref_list (cls, list_id, element_id):
		list = cls.__lists[list_id]
		if list[element_id].type == ListElementType.list:
			return list[element_id].reference
		else:
			return 0