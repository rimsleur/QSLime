# coding: utf8
"""
Данные триггеров
"""

from Trigger import Trigger
from CodeStack import CodeStack
from CodeLine import CodeLine
from ConditionProvider import ConditionProvider

class TriggerProvider ():

	@classmethod
	def __init__ (cls):
		cls.__triggers = []
		cls.__trigger_keys = {}
		cls.__triggers.append (None)
		cls.__activated_triggers = []
		cls.__activated_trigger_keys = {}
		cls.__last_activated_key = ""

	@classmethod
	def register_trigger (cls, field_id, key):
		trigger = Trigger ()
		trigger.field_id = field_id
		trigger.key = key
		cls.__triggers.append (trigger)
		id = len (cls.__triggers) - 1
		cls.__trigger_keys[key] = id
		return id

	@classmethod
	def delete_trigger (cls, key):
		id = cls.__trigger_keys.get (key)
		#id = cls.__event_keys[key]
		if id != None:
			#cls.__events.pop (id)
			del (cls.__trigger_keys[key])

	@classmethod
	def set_handler (cls, id, handler):
		cls.__triggers[id].handler = handler
		#print cls.__events[id].key
		#Проработать
		#if cls.__events[id].key == "2":
		#	cls.__events[id].priority = 2

	@classmethod
	def get_handler (cls, id):
		return cls.__triggers[id].handler

	@classmethod
	def get_trigger_id (cls, key):
		return cls.__trigger_keys.get (key)

	@classmethod
	def activate_trigger (cls, key):
		id = cls.get_trigger_id (key)
		if id != None:
			if cls.__activated_trigger_keys.get (key) == None:
				#if key == cls.__last_fired_key:
				cls.__activated_triggers.append (cls.__triggers[id])
				#else:
					#cls.__fired_events.insert (0, cls.__events[id])
				cls.__activated_trigger_keys[key] = id
				cls.__last_activated_key = key
				#print "^", key
			ConditionProvider.activate_trigger (id)

	@classmethod
	def dispatch_triggers (cls):
		triggers = []
		trigger = None
		if len (cls.__activated_triggers) > 0:
			trigger = cls.__activated_triggers.pop ()
		while trigger != None:
			if trigger.handler != "":
				triggers.append (trigger)	
			trigger = None
			if len (cls.__activated_triggers) > 0:
				trigger = cls.__activated_triggers.pop ()
		cls.__activated_trigger_keys.clear ()
		cls.__sort_triggers (triggers)
		for trigger in triggers:
			code_line = CodeLine ()
			code_line.field_id = trigger.field_id
			code_line.text = trigger.handler
			CodeStack.push (code_line)

	@classmethod
	def __sort_triggers (cls, triggers):
		#for event in events:
		#	print event.key, event.priority
		r = len (triggers) - 1
		i = 0
		while i < r:
			j = r
			while j > i:
				if triggers[j-1].priority < triggers[j].priority:
					e = triggers[j-1]
					triggers[j-1] = triggers[j]
					triggers[j] = e
				j -= 1
			i += 1