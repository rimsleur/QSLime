# coding: utf8
"""
Данные триады из базы данных
"""

class DatabaseTriad ():

	def __init__ (self):
	    self.id = 0
	    self.left_concept_id = 0
	    self.linkage_id = 0
	    self.right_concept_id = 0

	@classmethod
	def read (cls, cursor, left_concept_id, linkage_id, right_concept_id):
		query = "SELECT id, left_concept_id, linkage_id, right_concept_id FROM qsl_triad WHERE"
		if left_concept_id != 0:
			query += " left_concept_id = " + str (left_concept_id)
			if linkage_id != 0 or right_concept_id !=0:
				query += " AND"
		if linkage_id != 0:
			query += " linkage_id = " + str (linkage_id)
			if right_concept_id !=0:
				query += " AND"
		if right_concept_id !=0:
			query += " right_concept_id = " + str (right_concept_id)
		query += ";"

		cursor.execute (query)
		row = cursor.fetchone ()
		if row != None:
			triad = DatabaseTriad ()
			triad.id = row[0]
			triad.left_concept_id = row[1]
			triad.linkage_id = row[2]
			triad.right_concept_id = row[3]
			return triad
		else:
			return None

	@classmethod
	def read_by_id (cls, cursor, id):
		query = "SELECT id, left_concept_id, linkage_id, right_concept_id FROM qsl_triad WHERE id = "
		query += str (id) + ";"
		cursor.execute (query)
		row = cursor.fetchone ()
		if row != None:
			triad = DatabaseTriad ()
			triad.id = row[0]
			triad.left_concept_id = row[1]
			triad.linkage_id = row[2]
			triad.right_concept_id = row[3]
			return triad
		else:
			return None