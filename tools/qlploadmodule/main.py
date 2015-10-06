#!/usr/bin/python
# coding: utf8
"""
Программа формирования скрипта для загрузки программного модуля в QLP
"""

import sys

def main ():
	filename = sys.argv[1]
	if filename != None:
		sourse = open (filename, "r")
	filename = sys.argv[2]
	if filename != None:
		script = open (filename, "w")
	if sourse == None:
		print "Не удалось открыть файл-источник"
		return
	if script == None:
		print "Не удалось открыть файл-получатель"
		return

	script.write ('#! /bin/bash\n\n')
	script.write ('cd `cat ../path`\n')

	module = None
	line_count = 0

	for line in sourse.readlines ():
		if line == "\n":
			continue

		tab_count = 0

		for char in line:
			if char == "\t":
				tab_count += 1
			else:
				break

		if tab_count == 0:
			n = tab_count
			m = line.find (' ')
			word = line[n:m]
			if word == "модуль":
				line = line[m+1:]
				m = line.find (' ')
				module = line[:m]

		elif tab_count == 1:
			if module == None:
				print "Не удалось определить имя модуля"
				return

			n = tab_count
			m = line.find (' ')
			word = line[n:m]
			if word == "процедура":
				line = line[m+1:]
				m = line.find (' ')
				procedure = line[:m]

				script.write ('\n')
				script.write ('./qconcept -c 2 \'' + module + '.' + procedure + '\'\n')
				script.write ('./qconcept -c 5\n')
				script.write ('CONCEPT1=`./qconcept -m`\n')
				script.write ('./qsl2qsl -c "#$CONCEPT1 ?что быть ?чем процедура"\n')
				script.write ('./qsl2qsl -c "#$CONCEPT1 ?что иметь ?что имя ?какой ' + module + '.' + procedure + '"\n')
				script.write ('./qconcept -c 7\n')
				script.write ('CONCEPT2=`./qconcept -m`\n')
				script.write ('./qsl2qsl -c "#$CONCEPT1 ?что быть ?чем #$CONCEPT2"\n')

				line_count = 0

		elif tab_count == 2:
			line = line [tab_count:]

			if line [:1] == '#':
				script.write (line)
				continue

			line_count += 1
			line = line.replace ('\n', '')

			if line_count == 1:
				script.write ('./qconcept -a $CONCEPT2 0 \'' + line + '\'; PREVLINE=`./qconcept -g`\n')
			else:
				script.write ('./qconcept -a $CONCEPT2 $PREVLINE \'' + line + '\'; PREVLINE=`echo "$PREVLINE + 1" | bc`\n')

	sourse.close
	script.close

main ()