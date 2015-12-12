# coding: utf8
"""
Данные записи списка из базы данных
"""

class DatabaseList ():

	def __init__ (self):
	    self.id = 0
	    self.concept_id = 0
	    self.prev_line_id = 0
	    self.text = ""

	@classmethod
	def read_single (cls, cursor, concept_id, prev_line_id):
		query = "SELECT id, concept_id, prev_line_id, text FROM qsl_list WHERE"
		if concept_id != 0:
			query += " concept_id = " + str (concept_id)
			if prev_line_id != 0:
				query += " AND"
		if prev_line_id != 0:
			query += " prev_line_id = " + str (prev_line_id)
		query += ";"
		cursor.execute (query)
		row = cursor.fetchone ()
		if row != None:
			list = DatabaseList ()
			list.id = row[0]
			list.concept_id = row[1]
			list.prev_line_id = row[2]
			list.text = row[3]
			return list
		else:
			return None

	@classmethod
	def read (cls, cursor, concept_id):
		query = "SELECT id, concept_id, prev_line_id, text FROM qsl_list WHERE"
		if concept_id != 0:
			query += " concept_id = " + str (concept_id) + ";"
		cursor.execute (query)
		row = cursor.fetchone ()
		rows = []
		while (row != None):
			rows.append (row)
			row = cursor.fetchone ()
		arr = []
		for row in rows:
			list = DatabaseList ()
			list.id = row[0]
			list.concept_id = row[1]
			list.prev_line_id = row[2]
			list.text = row[3]
			arr.append (list)
		if len (arr) > 0:
			return arr
		else:
			return None