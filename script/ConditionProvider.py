# coding: utf8
"""
Данные условий
"""
from Condition import Condition
from CodeStack import CodeStack
from CodeLine import CodeLine

class ConditionProvider ():

	@classmethod
	def __init__ (cls):
		cls.__conditions = []
		cls.__conditions.append (None)
		cls.__is_activated_triggers = {}
		cls.__attach_lists = {}
		cls.__activated_conditions = []

	@classmethod
	def create_condition (cls):
		condition = Condition ()
		cls.__conditions.append (condition)
		return len (cls.__conditions) - 1

	@classmethod
	def set_handler (cls, id, handler):
		cls.__conditions[id].handler = handler
		cls.__conditions[id].priority = 4

	@classmethod
	def get_handler (cls, id):
		return cls.__conditions[id].handler

	@classmethod
	def attach_trigger (cls, condition_id, trigger_id):
		cls.__conditions[condition_id].attached_triggers += 1
		cls.__is_activated_triggers[trigger_id] = False
		list = cls.__attach_lists.get (trigger_id)
		if list == None:
			cls.__attach_lists[trigger_id] = []
			cls.__attach_lists[trigger_id].append (condition_id)
		else:
			cls.__attach_lists[trigger_id].append (condition_id)

	@classmethod
	def activate_trigger (cls, trigger_id):
		#print trigger_id
		is_set = cls.__is_activated_triggers.get (trigger_id)
		if is_set == False:
			cls.__is_activated_triggers[trigger_id] = True
			list = cls.__attach_lists[trigger_id]
			for id in list:
				cls.__conditions[id].activated_triggers += 1
				if cls.__conditions[id].activated_triggers == cls.__conditions[id].attached_triggers:
					cls.fire_condition (id)

	@classmethod
	def deactivate_trigger (cls, trigger_id):
		is_set = cls.__is_activated_triggers.get (trigger_id)
		if is_set == True:
			cls.__is_activated_triggers[trigger_id] = False
			list = cls.__attach_lists[trigger_id]
			for id in list:
				cls.__conditions[id].activated_triggers -= 1

	@classmethod
	def fire_condition (cls, id):
		cls.__activated_conditions.append (cls.__conditions[id])

	@classmethod
	def dispatch_conditions (cls):
		condition = None
		if len (cls.__activated_conditions) > 0:
			condition = cls.__activated_conditions.pop ()
		while condition != None:
			if condition.handler != "":
				code_line = CodeLine ()
				code_line.text = condition.handler
				code_line.priority = condition.priority
				CodeStack.push (code_line)
			condition = None
			if len (cls.__activated_conditions) > 0:
				condition = cls.__activated_conditions.pop ()