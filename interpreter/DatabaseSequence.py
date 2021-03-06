# coding: utf8
"""
Данные последовательность триад из базы данных
"""

class DatabaseSequence ():

	def __init__ (self):
	    self.id = 0
	    self.proposition_id = 0
	    self.left_triad_id = 0
	    self.right_triad_id = 0

	@classmethod
	def read (cls, cursor, proposition_id, left_triad_id, right_triad_id):
		query = "SELECT id, proposition_id, left_triad_id, right_triad_id FROM qsl_sequence WHERE"
		if proposition_id != 0:
			query += " proposition_id = " + str (proposition_id)
			if right_triad_id != 0 or left_triad_id !=0:
				query += " AND"
		if right_triad_id != 0:
			query += " right_triad_id = " + str (right_triad_id)
			if left_triad_id !=0:
				query += " AND"
		if left_triad_id != 0:
			query += " left_triad_id = " + str (left_triad_id)
		query += ";"
		cursor.execute (query)
		row = cursor.fetchone ()
		if row != None:
			sequence = DatabaseSequence ()
			sequence.id = row[0]
			sequence.proposition_id = row[1]
			sequence.left_triad_id = row[2]
			sequence.right_triad_id = row[3]
			return sequence
		else:
			return None