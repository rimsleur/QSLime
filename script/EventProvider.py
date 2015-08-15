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
		cls.__events.append (None)
		cls.__last_event_index = 0
		cls.__event_dict = {}
		cls.__fired_events = []

	@classmethod
	def register_event (cls, field_id, key):
		event = Event ()
		event.field_id = field_id
		cls.__events.append (event)
		cls.__last_event_index += 1
		cls.__event_dict[key] = cls.__last_event_index
		return cls.__last_event_index

	@classmethod
	def set_event_handler (cls, id, handler):
		cls.__events[id].handler = handler

	@classmethod
	def get_event_handler (cls, id):
		return cls.__events[id].handler

	@classmethod
	def get_event_id (cls, key):
		return cls.__event_dict.get (key)

	@classmethod
	def fire_event (cls, key):
		id = cls.get_event_id (key)
		if id != None:
			cls.__fired_events.append (cls.__events[id])

	@classmethod
	def dispatch_events (cls):
		event = None
		if len (cls.__fired_events) > 0:
			event = cls.__fired_events.pop ()
		while event != None:
			code_line = CodeLine ()
			code_line.field_id = event.field_id
			code_line.text = event.handler
			CodeStack.push (code_line)
			event = None
			if len (cls.__fired_events) > 0:
				event = cls.__fired_events.pop ()