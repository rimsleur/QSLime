# coding: utf8
"""
Данные событий
"""

from Event import Event
from CodeStack import CodeStack
from CodeLine import CodeLine
from ConditionProvider import ConditionProvider

class EventProvider ():

	@classmethod
	def __init__ (cls):
		cls.__events = []
		cls.__event_keys = {}
		cls.__events.append (None)
		cls.__fired_events = []
		cls.__fired_event_keys = {}
		cls.__last_fired_key = ""

	@classmethod
	def register_event (cls, field_id, key):
		event = Event ()
		event.field_id = field_id
		event.key = key
		cls.__events.append (event)
		id = len (cls.__events) - 1
		cls.__event_keys[key] = id
		return id

	@classmethod
	def delete_event (cls, key):
		id = cls.__event_keys[key]
		cls.__events.pop (id)
		del (cls.__event_keys[key])

	@classmethod
	def set_handler (cls, id, handler):
		cls.__events[id].handler = handler

	@classmethod
	def get_handler (cls, id):
		return cls.__events[id].handler

	@classmethod
	def get_event_id (cls, key):
		return cls.__event_keys.get (key)

	@classmethod
	def fire_event (cls, key):
		id = cls.get_event_id (key)
		if id != None:
			if cls.__fired_event_keys.get (key) == None:
				#if key == cls.__last_fired_key:
				cls.__fired_events.append (cls.__events[id])
				#else:
					#cls.__fired_events.insert (0, cls.__events[id])
				cls.__fired_event_keys[key] = id
				cls.__last_fired_key = key
				#print "^", key
			ConditionProvider.set_event (id)

	@classmethod
	def dispatch_events (cls):
		event = None
		if len (cls.__fired_events) > 0:
			event = cls.__fired_events.pop ()
		while event != None:
			if event.handler != "":
				code_line = CodeLine ()
				code_line.field_id = event.field_id
				code_line.text = event.handler
				CodeStack.push (code_line)
			event = None
			if len (cls.__fired_events) > 0:
				event = cls.__fired_events.pop ()
		cls.__fired_event_keys.clear ()