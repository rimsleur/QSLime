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
	lines = []
	procs = []
	conds = []

	for line in sourse.readlines ():
		lines.append (line)

	for line in lines:
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

				for line in lines:
					tab_count = 0

					for char in line:
						if char == "\t":
							tab_count += 1
						else:
							break

					if tab_count == 1:
						n = tab_count
						m = line.find (' ')
						word = line[n:m]
						if word == "процедура":
							line = line[m+1:]
							m = line.find (' ')
							procedure = line[:m]
							if procedure != "":
								procs.append (procedure)
						elif word == "условие":
							line = line[m+1:]
							m = line.find (' ')
							condition = line[:m]
							if condition != "":
								conds.append (condition)

				script.write ('\n')
				script.write ('./qconcept -c 2 \'' + module + '\'\n')
				script.write ('./qconcept -c 5\n')
				script.write ('CONCEPT1=`./qconcept -m`\n')
				script.write ('./qsl2qsl -c "#$CONCEPT1 ?что быть ?чем модуль"\n')
				script.write ('./qsl2qsl -c "#$CONCEPT1 ?что иметь ?что имя ?какой ' + module + '"\n')

				if len (procs) > 0:
					script.write ('\n')
					script.write ('./qconcept -c 2 \'' + module + '.procs' + '\'\n')
					script.write ('./qconcept -c 5\n')
					script.write ('CONCEPT1=`./qconcept -m`\n')
					script.write ('./qsl2qsl -c "#$CONCEPT1 ?что быть ?чем процедуры"\n')
					script.write ('./qsl2qsl -c "#$CONCEPT1 ?что иметь ?что имя ?какой ' + module + '.procs' + '"\n')
					script.write ('./qconcept -c 7\n')
					script.write ('CONCEPT2=`./qconcept -m`\n')
					script.write ('./qsl2qsl -c "#$CONCEPT1 ?что быть ?чем #$CONCEPT2"\n')

					line_count = 1

					for proc in procs:
						if line_count == 1:
							script.write ('./qconcept -a $CONCEPT2 0 \'' + module + '.' + proc + '\'; PREVLINE=`./qconcept -g`\n')
						else:
							script.write ('./qconcept -a $CONCEPT2 $PREVLINE \'' + module + '.' + proc + '\'; PREVLINE=`echo "$PREVLINE + 1" | bc`\n')
						line_count += 1

				if len (conds) > 0:
					script.write ('\n')
					script.write ('./qconcept -c 2 \'' + module + '.conds' + '\'\n')
					script.write ('./qconcept -c 5\n')
					script.write ('CONCEPT1=`./qconcept -m`\n')
					script.write ('./qsl2qsl -c "#$CONCEPT1 ?что быть ?чем условия"\n')
					script.write ('./qsl2qsl -c "#$CONCEPT1 ?что иметь ?что имя ?какой ' + module + '.conds' + '"\n')
					script.write ('./qconcept -c 7\n')
					script.write ('CONCEPT2=`./qconcept -m`\n')
					script.write ('./qsl2qsl -c "#$CONCEPT1 ?что быть ?чем #$CONCEPT2"\n')

					line_count = 1

					for cond in conds:
						if line_count == 1:
							script.write ('./qconcept -a $CONCEPT2 0 \'' + module + '.' + cond + '\'; PREVLINE=`./qconcept -g`\n')
						else:
							script.write ('./qconcept -a $CONCEPT2 $PREVLINE \'' + module + '.' + cond + '\'; PREVLINE=`echo "$PREVLINE + 1" | bc`\n')
						line_count += 1

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

			elif word == "условие":
				line = line[m+1:]
				m = line.find (' ')
				condition = line[:m]

				script.write ('\n')
				script.write ('./qconcept -c 2 \'' + module + '.' + condition + '\'\n')
				script.write ('./qconcept -c 5\n')
				script.write ('CONCEPT1=`./qconcept -m`\n')
				script.write ('./qsl2qsl -c "#$CONCEPT1 ?что быть ?чем условие"\n')
				script.write ('./qsl2qsl -c "#$CONCEPT1 ?что иметь ?что имя ?какой ' + module + '.' + condition + '"\n')
				script.write ('./qconcept -c 7\n')
				script.write ('CONCEPT2=`./qconcept -m`\n')
				script.write ('./qsl2qsl -c "#$CONCEPT1 ?что быть ?чем #$CONCEPT2"\n')

				script.write ('./qconcept -c 2 \'' + module + '.' + condition + '.precs' + '\'\n')
				script.write ('./qconcept -c 5\n')
				script.write ('CONCEPT1=`./qconcept -m`\n')
				script.write ('./qsl2qsl -c "#$CONCEPT1 ?что быть ?чем предпосылки"\n')
				script.write ('./qsl2qsl -c "#$CONCEPT1 ?что иметь ?что имя ?какой ' + module + '.' + condition + '.precs' + '"\n')
				script.write ('./qconcept -c 7\n')
				script.write ('CONCEPT3=`./qconcept -m`\n')
				script.write ('./qsl2qsl -c "#$CONCEPT1 ?что быть ?чем #$CONCEPT3"\n')

				line_count = 0

		elif tab_count == 2:
			line = line [tab_count:]

			if line == "(\n" or line == ")\n":
				line_count = 0
				continue

			line_count += 1
			line = line.replace ('\n', '')

			if line_count == 1:
				script.write ('./qconcept -a $CONCEPT2 0 \'' + line + '\'; PREVLINE=`./qconcept -g`\n')
			else:
				script.write ('./qconcept -a $CONCEPT2 $PREVLINE \'' + line + '\'; PREVLINE=`echo "$PREVLINE + 1" | bc`\n')

		elif tab_count == 3:
			line = line [tab_count:]

			line_count += 1
			line = line.replace ('\n', '')

			if line_count == 1:
				script.write ('./qconcept -a $CONCEPT3 0 \'' + line + '\'; PREVLINE=`./qconcept -g`\n')
			else:
				script.write ('./qconcept -a $CONCEPT3 $PREVLINE \'' + line + '\'; PREVLINE=`echo "$PREVLINE + 1" | bc`\n')

	sourse.close
	script.close

main ()