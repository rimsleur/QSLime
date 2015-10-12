# coding: utf8
"""
Переводчик аглийских терминов в коде на другие языки
"""

class LanguageHelper ():

	@classmethod
	def __init__ (cls, cursor, lang):
		cls.__cursor = cursor
		cls.__lang = lang

	@classmethod
	def translate (cls, word):
		query = "SELECT word FROM qsl_language WHERE en_word = '" + word + "' AND lang = '" + cls.__lang + "';"
		cls.__cursor.execute (query)
		row = cls.__cursor.fetchone ()
		if row != None:
			return row[0]
		else:
			return ""