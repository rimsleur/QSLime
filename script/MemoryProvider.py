# coding: utf8
"""
Данные в оперативной памяти
"""

class MemoryProvider ():

	@classmethod
	def __init__ (cls):
		cls.__fields = []
		cls.__fields.append (None)
		cls.__last_field_index = 0
		cls.__name_dict = {}

	@classmethod
	def create_field (cls, name):
		id = cls.get_field_id (name)
		if id != None:
			return id
		else:
			cls.__fields.append (None)
			cls.__last_field_index += 1
			cls.__name_dict[name] = cls.__last_field_index
			return cls.__last_field_index

	@classmethod
	def get_field_id (cls, name):
		return cls.__name_dict.get (name)

	@classmethod
	def get_field_value (cls, id):
		return cls.__fields[id]

	@classmethod
	def set_field_value (cls, id, value):
		cls.__fields[id] = value

	@classmethod
	def print_all (cls):
		print cls.__name_dict.items ()