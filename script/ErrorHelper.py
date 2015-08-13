# coding: utf8
"""
Формирователь текста ошибок
"""

class ErrorHelper ():

	@classmethod
	def get_text (cls, cursor, number, *var):
		query = "SELECT text FROM qsl_error WHERE number = " + str (number) + ";"
		cursor.execute (query)
		row = cursor.fetchone ()
		if row != None:
			text = row[0]
			i = 0
			while i < len (var):
				text = text.replace ("&", var[i], 1)
				i += 1
			return "#" + str (number) + ":" + text
		else:
			return "#100:Ошибка с номером " + str (number) + " отсутствует в базе данных"