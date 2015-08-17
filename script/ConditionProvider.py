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
		cls.__is_set_events = {}
		cls.__attach_lists = {}
		cls.__fired_conditions = []

	@classmethod
	def create_condition (cls):
		condition = Condition ()
		cls.__conditions.append (condition)
		return len (cls.__conditions) - 1

	@classmethod
	def set_handler (cls, id, handler):
		cls.__conditions[id].handler = handler

	@classmethod
	def get_handler (cls, id):
		return cls.__conditions[id].handler

	@classmethod
	def attach_event (cls, condition_id, event_id):
		cls.__conditions[condition_id].attached_events += 1
		cls.__is_set_events[event_id] = False
		list = cls.__attach_lists.get (event_id)
		if list == None:
			cls.__attach_lists[event_id] = []
			cls.__attach_lists[event_id].append (condition_id)
		else:
			cls.__attach_lists[event_id].append (condition_id)

	@classmethod
	def set_event (cls, event_id):
		is_set = cls.__is_set_events.get (event_id)
		if is_set == False:
			cls.__is_set_events[event_id] = True
			list = cls.__attach_lists[event_id]
			for id in list:
				cls.__conditions[id].fired_events += 1
				if cls.__conditions[id].fired_events == cls.__conditions[id].attached_events:
					cls.fire_condition (id)

	@classmethod
	def unset_event (cls, event_id):
		is_set = cls.__is_set_events.get (event_id)
		if is_set == True:
			cls.__is_set_events[event_id] = False
			list = cls.__attach_lists[event_id]
			for id in list:
				cls.__conditions[id].fired_events -= 1

	@classmethod
	def fire_condition (cls, id):
		cls.__fired_conditions.append (cls.__conditions[id])

	@classmethod
	def dispatch_conditions (cls):
		condition = None
		if len (cls.__fired_conditions) > 0:
			condition = cls.__fired_conditions.pop ()
		while condition != None:
			if condition.handler != "":
				code_line = CodeLine ()
				code_line.text = condition.handler
				CodeStack.push (code_line)
			condition = None
			if len (cls.__fired_conditions) > 0:
				condition = cls.__fired_conditions.pop ()