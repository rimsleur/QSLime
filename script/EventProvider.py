# coding: utf8
"""
Данные событий
"""

from Event import Event
from CodeStack import CodeStack
from CodeLine import CodeLine

class EventProvider ():

	@classmethod
	def __init__ (cls):
		cls.__events = []
		cls.__event_keys = {}
		cls.__events.append (None)
		cls.__fired_events1 = []
		cls.__fired_event_keys1 = {}
		cls.__fired_events2 = []
		cls.__fired_event_keys2 = {}
		cls.__halfcycle = 1

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
	def set_event_handler (cls, id, handler):
		cls.__events[id].handler = handler

	@classmethod
	def get_event_handler (cls, id):
		return cls.__events[id].handler

	@classmethod
	def get_event_id (cls, key):
		return cls.__event_keys.get (key)

	@classmethod
	def fire_event (cls, key):
		id = cls.get_event_id (key)
		if id != None:
			if cls.__halfcycle == 1:
				if cls.__fired_event_keys1.get (key) == None:
					cls.__fired_events1.append (cls.__events[id])
					cls.__fired_event_keys1[key] = id
				else:
					cls.__fired_events2.append (cls.__events[id])
					cls.__fired_event_keys2[key] = id
			if cls.__halfcycle == 2:
				if cls.__fired_event_keys2.get (key) == None:
					cls.__fired_events2.append (cls.__events[id])
					cls.__fired_event_keys2[key] = id
				else:
					cls.__fired_events1.append (cls.__events[id])
					cls.__fired_event_keys1[key] = id

	@classmethod
	def dispatch_events (cls):
		event = None
		if cls.__halfcycle == 1 and len (cls.__fired_events1) == 0:
			cls.__halfcycle = 2
		elif cls.__halfcycle == 2 and len (cls.__fired_events2) == 0:
			cls.__halfcycle = 1
		if cls.__halfcycle == 1:
			fired_events = cls.__fired_events1
			cls.__halfcycle = 2
		elif cls.__halfcycle == 2:
			fired_events = cls.__fired_events2
			cls.__halfcycle = 1
		if len (fired_events) > 0:
			event = fired_events.pop ()
		while event != None:
			if event.handler != "":
				code_line = CodeLine ()
				code_line.field_id = event.field_id
				code_line.text = event.handler
				CodeStack.push (code_line)
			event = None
			if len (fired_events) > 0:
				event = fired_events.pop ()