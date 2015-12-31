#!/usr/bin/python
# coding: utf8
"""
Программа выгрузки программного модуля из QLP в файл .qslm
"""

import sys
import os
import MySQLdb

reload (sys)

def main ():
	if len (sys.argv) < 2:
		print "Недостаточное количество аргументов"
		return
	modulename = sys.argv[1]
	if modulename == None:
		print "Имя модуля не определено"
		return
	path = sys.argv[2]
	if path == None:
		print "Путь к файлу не определен"
		return
	filename = path + modulename + '.qslm'
	qslmfile = open (filename, "w")
	if qslmfile == None:
		print "Не удалось открыть файл для записи"
		return

	db = MySQLdb.connect (host="localhost", user="qslbase", passwd="qslbase", db="qslbase", charset="utf8")
	cursor = db.cursor ()
	sys.setdefaultencoding ("utf8")

	qslmfile.write ('модуль ' + modulename + '\n\n')
	
	row = None
	linkage_id = 0
	left_concept_id = 0
	right_concept_id = 0
	triad_id = 0
	module_id = 0
	procedures = []

	query = "SELECT id FROM qsl_linkage WHERE name = 'какой';"
	cursor.execute (query)
	row = cursor.fetchone ()
	if row != None:
		linkage_id = row[0]

	query = "SELECT id FROM qsl_concept WHERE type = 2 AND name = 'имя';"
	cursor.execute (query)
	row = cursor.fetchone ()
	if row != None:
		left_concept_id = row[0]

	query = "SELECT id FROM qsl_concept WHERE type = 2 AND name = '" + modulename + "';"
	cursor.execute (query)
	row = cursor.fetchone ()
	if row != None:
		right_concept_id = row[0]

	if left_concept_id != 0 and linkage_id != 0 and right_concept_id !=0:
		query = "SELECT id FROM qsl_triad WHERE left_concept_id = " + str (left_concept_id)
		query += " AND linkage_id = " + str (linkage_id)
		query += " AND right_concept_id = " + str (right_concept_id) + ";"
		cursor.execute (query)
		row = cursor.fetchone ()
		if row != None:
			triad_id = row[0]

	if triad_id != 0:
		query = "SELECT id, proposition_id FROM qsl_sequence WHERE right_triad_id = " + str (triad_id) + ";"
		cursor.execute (query)
		row = cursor.fetchone ()
		if row != None:
			query = "SELECT left_triad_id FROM qsl_sequence WHERE proposition_id = " + str (row[1])
			query += " AND id <> " + str (row[0]) + ";"
			cursor.execute (query)
			row = cursor.fetchone ()
			if row != None:
				query = "SELECT left_concept_id FROM qsl_triad WHERE id = " + str (row[0]) + ";"
				cursor.execute (query)
				row = cursor.fetchone ()
				if row != None:
					module_id = row[0]

	if module_id != 0:
		linkage_id = 0
		left_concept_id = 0
		right_concept_id = 0
		triad_id = 0
		arr = []
		module_list_id = 0

		query = "SELECT id FROM qsl_linkage WHERE name = 'что';"
		cursor.execute (query)
		row = cursor.fetchone ()
		if row != None:
			linkage_id = row[0]

		left_concept_id = module_id

		query = "SELECT id FROM qsl_concept WHERE type = 1 AND name = 'быть';"
		cursor.execute (query)
		row = cursor.fetchone ()
		if row != None:
			right_concept_id = row[0]

		if left_concept_id != 0 and linkage_id != 0 and right_concept_id !=0:
			query = "SELECT id FROM qsl_triad WHERE left_concept_id = " + str (left_concept_id)
			query += " AND linkage_id = " + str (linkage_id)
			query += " AND right_concept_id = " + str (right_concept_id) + ";"
			cursor.execute (query)
			row = cursor.fetchone ()
			if row != None:
				triad_id = row[0]

		if triad_id != 0:
			query = "SELECT right_triad_id FROM qsl_sequence WHERE left_triad_id = " + str (triad_id) + ";"
			cursor.execute (query)
			row = cursor.fetchone ()
			while row != None:
				arr.append (row[0])
				row = cursor.fetchone ()

			for a in arr:
				query = "SELECT right_concept_id FROM qsl_triad WHERE id = " + str (a) + ";"
				cursor.execute (query)
				row = cursor.fetchone ()
				if row != None:
					query = "SELECT id FROM qsl_concept WHERE type = 7 AND id = " + str (row[0]) + ";"
					cursor.execute (query)
					row = cursor.fetchone ()
					if row != None:
						module_list_id = row[0]

		if module_list_id != 0:
			query = "SELECT text FROM qsl_list WHERE concept_id = " + str (module_list_id) + ";"
			cursor.execute (query)
			row = cursor.fetchone ()
			while row != None:
				procedures.append (row[0])
				row = cursor.fetchone ()

	for procedure in procedures:
		m = modulename + '.'
		s = procedure.replace (m, '')
		qslmfile.write ('\tпроцедура ' + s + '\n')

		row = None
		linkage_id = 0
		left_concept_id = 0
		right_concept_id = 0
		triad_id = 0
		procedure_id = 0

		query = "SELECT id FROM qsl_linkage WHERE name = 'какой';"
		cursor.execute (query)
		row = cursor.fetchone ()
		if row != None:
			linkage_id = row[0]

		query = "SELECT id FROM qsl_concept WHERE type = 2 AND name = 'имя';"
		cursor.execute (query)
		row = cursor.fetchone ()
		if row != None:
			left_concept_id = row[0]

		query = "SELECT id FROM qsl_concept WHERE type = 2 AND name = '" + procedure + "';"
		cursor.execute (query)
		row = cursor.fetchone ()
		if row != None:
			right_concept_id = row[0]

		if left_concept_id != 0 and linkage_id != 0 and right_concept_id !=0:
			query = "SELECT id FROM qsl_triad WHERE left_concept_id = " + str (left_concept_id)
			query += " AND linkage_id = " + str (linkage_id)
			query += " AND right_concept_id = " + str (right_concept_id) + ";"
			cursor.execute (query)
			row = cursor.fetchone ()
			if row != None:
				triad_id = row[0]

		if triad_id != 0:
			query = "SELECT id, proposition_id FROM qsl_sequence WHERE right_triad_id = " + str (triad_id) + ";"
			cursor.execute (query)
			row = cursor.fetchone ()
			if row != None:
				query = "SELECT left_triad_id FROM qsl_sequence WHERE proposition_id = " + str (row[1])
				query += " AND id <> " + str (row[0]) + ";"
				cursor.execute (query)
				row = cursor.fetchone ()
				if row != None:
					query = "SELECT left_concept_id FROM qsl_triad WHERE id = " + str (row[0]) + ";"
					cursor.execute (query)
					row = cursor.fetchone ()
					if row != None:
						procedure_id = row[0]

		if procedure_id != 0:
			linkage_id = 0
			left_concept_id = 0
			right_concept_id = 0
			triad_id = 0
			arr = []
			procedure_list_id = 0

			query = "SELECT id FROM qsl_linkage WHERE name = 'что';"
			cursor.execute (query)
			row = cursor.fetchone ()
			if row != None:
				linkage_id = row[0]

			left_concept_id = procedure_id

			query = "SELECT id FROM qsl_concept WHERE type = 1 AND name = 'быть';"
			cursor.execute (query)
			row = cursor.fetchone ()
			if row != None:
				right_concept_id = row[0]

			if left_concept_id != 0 and linkage_id != 0 and right_concept_id !=0:
				query = "SELECT id FROM qsl_triad WHERE left_concept_id = " + str (left_concept_id)
				query += " AND linkage_id = " + str (linkage_id)
				query += " AND right_concept_id = " + str (right_concept_id) + ";"
				cursor.execute (query)
				row = cursor.fetchone ()
				if row != None:
					triad_id = row[0]

			if triad_id != 0:
				query = "SELECT right_triad_id FROM qsl_sequence WHERE left_triad_id = " + str (triad_id) + ";"
				cursor.execute (query)
				row = cursor.fetchone ()
				while row != None:
					arr.append (row[0])
					row = cursor.fetchone ()

				for a in arr:
					query = "SELECT right_concept_id FROM qsl_triad WHERE id = " + str (a) + ";"
					cursor.execute (query)
					row = cursor.fetchone ()
					if row != None:
						query = "SELECT id FROM qsl_concept WHERE type = 7 AND id = " + str (row[0]) + ";"
						cursor.execute (query)
						row = cursor.fetchone ()
						if row != None:
							procedure_list_id = row[0]

		if procedure_list_id != 0:
			query = "SELECT text FROM qsl_list WHERE concept_id = " + str (procedure_list_id) + ";"
			cursor.execute (query)
			row = cursor.fetchone ()
			while row != None:
				s = row[0].replace ('\n', '\\n')
				qslmfile.write ('\t\t' + s + '\n')
				row = cursor.fetchone ()

		qslmfile.write ('\n')

	qslmfile.close

main ()