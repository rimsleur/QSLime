#!/usr/bin/python
# coding: utf8
import MySQLdb
import sys
reload(sys)

def main (text):

	class Concept:
		id = 0
		name = 0
		type = 0

	class Triad:
		linkage_id = 0
		linkage_name = ""
		left_concept = Concept ()
		right_concept = Concept ()

	word = []
	tokens = []
	triads = []
	major_linkage_id = 0
	left_concept = Concept ()

	db = MySQLdb.connect (host="localhost", user="qslbase", passwd="1q2w3e", db="qslbase", charset="utf8")
	cursor = db.cursor()

	after_space = False
	after_linkage = False

	#print "Python-скрипт, функция main()"
	
	sys.setdefaultencoding("utf8")

# Разбор суждения на токены
	for letter in text:
		if letter == "?" and after_space == True:
			token = ''.join (word)
			tokens.append (token)
			word = []
			after_linkage = True
		after_space = False
		if letter == " ":
			after_space = True
			if after_linkage == True:
				token = ''.join (word)
				tokens.append (token)
				word = []
			else:
				word.append (letter)
			after_linkage = False
		else:
			word.append (letter)

	token = ''.join (word)
	if token != "":
		token = token.replace ('?', '')
		tokens.append (token)

# Построение списка триад
	linkage_filled = False
	idx = 1

	for token in tokens:
		#print token
		if token.find ('?') == 0:
			triad = Triad ()
			s = token.replace ('?', '')
			query = "SELECT id FROM qsl_linkage WHERE name = \'" + s + "\';"
			cursor.execute (query)
			row = cursor.fetchone ()
			if row != None:
				triad.linkage_id = row[0]
			triad.linkage_name = token
			triad.left_concept = Concept ()
			triad.right_concept = Concept ()
			triad.left_concept.id = left_concept.id
			triad.left_concept.name = left_concept.name
			linkage_filled = True
		else:
			if linkage_filled == True:
				linkage_filled = False
				if token != "_":
					query = "SELECT id, type FROM qsl_concept WHERE name = \'" + token + "\';"
					cursor.execute (query)
					row = cursor.fetchone ()
					if row != None:
						triad.right_concept.id = row[0]
						triad.right_concept.type = row[1]
					if triad.right_concept.type == 1:
						major_linkage_id = idx
						idx += 1
				triad.right_concept.name = token
				left_concept.id = triad.right_concept.id
				left_concept.name = triad.right_concept.name
				triads.append (triad)
			else:
				if token != "_":
					query = "SELECT id, type FROM qsl_concept WHERE name = \'" + token + "\';"
					cursor.execute (query)
					row = cursor.fetchone ()
					if row != None:
						left_concept.id = row[0]
						left_concept.type = row[1]
				left_concept.name = token

# Прохождение по цепочке триад и поиск суждения
	#for triad in triads:
		#print str(triad.left_concept.id) + ", " + str(triad.linkage_id) + ", " + str(triad.right_concept.id)

	triad_count = len (triads);
	idx = major_linkage_id;
	triad1_id = 0
	triad2_id = 0
	proposition_id = 0

	while idx <= triad_count:
		query = "SELECT id FROM qsl_triad WHERE left_concept_id = " + str (triads[idx-1].left_concept.id)
		query += " AND linkage_id = " + str (triads[idx-1].linkage_id)
		query += " AND right_concept_id = " + str (triads[idx-1].right_concept.id) + ";"
		cursor.execute (query)
		row = cursor.fetchone ()
		if row != None:
			if triad1_id == 0:
				triad1_id = row[0]
			else:
				if triad2_id != 0:
					triad1_id = triad2_id
				triad2_id = row[0]
		else:
			if idx == major_linkage_id:
				break

		if triad1_id != 0 and triad2_id != 0:
			#print str (triad1_id) + ", " + str (triad2_id)
			query = "SELECT proposition_id FROM qsl_sequence WHERE"
			query += " left_triad_id = " + str (triad1_id)
			query += " AND right_triad_id = " + str (triad2_id)
			if proposition_id != 0:
				query += " AND proposition_id = " + str (proposition_id)
			query += ";"
			cursor.execute (query)
			row = cursor.fetchone ()
			if row != None:
				proposition_id = row[0]

		idx += 1

	res = ""

	if proposition_id != 0:
		query = "SELECT text FROM qsl_proposition WHERE id = " + str (proposition_id) + ";"
		cursor.execute (query)
		row = cursor.fetchone ()
		if row != None:
			res = row[0]

	if res != "":
		return res
	else:
		return "Информация отсутствует"

print main  ("шар ?что иметь ?что цвет ?какой _?")
