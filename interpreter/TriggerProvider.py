# coding: utf8
"""
Данные триггеров
"""

from Trigger import Trigger
from CodeStack import CodeStack
from CodeLine import CodeLine
from ConditionProvider import ConditionProvider
from TriggerType import TriggerType

class TriggerProvider ():

	@classmethod
	def __init__ (cls):
		cls.__triggers = []
		cls.__triggers.append (None)
		cls.__trigger_name_dict = {}
		cls.__object_triggers = {}
		
		cls.__activated_triggers = []
		#cls.__activated_trigger_keys = {}
		#cls.__last_activated_key = ""

	@classmethod
	def create_trigger (cls, name):
		trigger = Trigger ()
		cls.__triggers.append (trigger)
		id = len (cls.__triggers) - 1
		if name != None:
			cls.__trigger_name_dict[name] = id
		return id

	@classmethod
	def register_trigger (cls, trigger_id, object_key, trigger_type, trigger_condition, field_value):
		trigger = cls.__triggers[trigger_id]
		#trigger.field_id = field_id
		trigger.object_key = object_key
		trigger.type = trigger_type
		trigger.condition = trigger_condition
		trigger.value = field_value

		#print "trigger_id=", trigger_id, " object_key=", object_key, " condition=", trigger_condition, " value", field_value

		object_triggers = cls.get_object_triggers (object_key)
		if object_triggers == None:
			triggers = []
			triggers.append (trigger_id)
			cls.__object_triggers [object_key] = triggers
		else:
			object_triggers.append (trigger_id)

	@classmethod
	def delete_trigger (cls, object_key, trigger_condition, field_value):
		object_triggers = cls.get_object_triggers (object_key)
		if object_triggers != None:
			idx = None
			for id in object_triggers:
				if cls.__triggers[id].condition == trigger_condition:
					idx = id

			if idx != None:
				ConditionProvider.deactivate_trigger (idx)
				cls.__triggers.pop (idx)
				del (cls.__object_triggers[object_key])

	@classmethod
	def set_handler (cls, id, concept_id):
		cls.__triggers[id].handler = concept_id

	@classmethod
	def get_handler (cls, id):
		return cls.__triggers[id].handler

	@classmethod
	def set_priority (cls, id, priority):
		#print id, priority
		cls.__triggers[id].priority = priority

	@classmethod
	def set_class (cls, id, classtxt):
		#print id, classtxt
		cls.__triggers[id].classtxt = classtxt

	@classmethod
	def get_id_by_class (cls, classtxt):
		#print classtxt
		i = 0
		for trigger in cls.__triggers:
			if	trigger != None and trigger.classtxt == classtxt:
				return i
			i += 1

	#@classmethod
	#def get_trigger_id (cls, key):
	#	return cls.__trigger_keys.get (key)

	@classmethod
	def get_object_triggers (cls, object_key):
		return cls.__object_triggers.get (object_key)

	@classmethod
	def process_object_triggers (cls, object_key, object_value):
		deferred_activation = []
		object_triggers = cls.get_object_triggers (object_key)
		if object_triggers != None:
			for id in object_triggers:
				activate = False

				if cls.__triggers[id].condition == "":
					activate = True
				elif cls.__triggers[id].condition == "==":
					if str (object_value) == str (cls.__triggers[id].value):
						activate = True
				elif cls.__triggers[id].condition == "!=":
					if str (object_value) != str (cls.__triggers[id].value):
						activate = True
				elif cls.__triggers[id].condition == ">=":
					if object_value >= cls.__triggers[id].value:
						activate = True
				elif cls.__triggers[id].condition == "<=":
					if object_value <= cls.__triggers[id].value:
						activate = True
				elif cls.__triggers[id].condition == ">":
					if object_value > cls.__triggers[id].value:
						activate = True
				elif cls.__triggers[id].condition == "<":
					if object_value < cls.__triggers[id].value:
						activate = True
		
				if activate == True:
					if cls.__triggers[id].type == TriggerType.on_change:
						if cls.__triggers[id].active == True:
							cls.__triggers[id].active = False
							#print "D", cls.__triggers[id].condition, cls.__triggers[id].value
							ConditionProvider.deactivate_trigger (id)
					deferred_activation.append (id)
				else:
					#print "deact", object_key, cls.__triggers[id].condition, cls.__triggers[id].value, object_value
					if cls.__triggers[id].active == True:
						#print "D", cls.__triggers[id].condition, cls.__triggers[id].value
						cls.__triggers[id].active = False
						n = cls.__activated_triggers.count (id)
						if n != 0:
							cls.__activated_triggers.remove (id)
						ConditionProvider.deactivate_trigger (id)

			for id in deferred_activation:
				#print "act", object_key, cls.__triggers[id].condition, cls.__triggers[id].value, object_value
				if cls.__triggers[id].active == False:
					cls.__triggers[id].active = True
					cls.__activated_triggers.append (id)
					ConditionProvider.activate_trigger (id)

	@classmethod
	def dispatch_triggers (cls):
		triggers = []
		trigger = None
		if len (cls.__activated_triggers) > 0:
			trigger = cls.__triggers[cls.__activated_triggers.pop ()]
		while trigger != None:
			#trigger.active = False
			if trigger.handler != "":
				triggers.append (trigger)
			trigger = None
			if len (cls.__activated_triggers) > 0:
				trigger = cls.__triggers[cls.__activated_triggers.pop ()]
		for trigger in triggers:
			code_line = CodeLine ()
			code_line.field_id = trigger.object_key
			code_line.concept_id = trigger.handler
			code_line.prev_line_id = -1
			code_line.priority = trigger.priority
			CodeStack.push (code_line)