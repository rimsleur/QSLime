#!/usr/bin/python
# coding: utf8
"""
Программа-терминал для взаимодействия с QLP
Точка входа
"""

import os
import sys
import time
import curses

reload (sys)

def main ():
	exit = False
	pipein = open("/tmp/qlpterm-tube", "r")

	screen = curses.initscr()
	screen.clear ()
	curses.curs_set(0)

	while (exit != True):
		line = pipein.readline ()
		if line == "":
			break
		line = line.replace ("\n", "")
		#print line
		pos_lbr = line.find ("[")
		cmd = line[:pos_lbr]
		if cmd == "INIT":
			pos_div = line.find (":")
			xs = line [pos_lbr+1:pos_div]
			pos_rbr = line.find ("]")
			ys = line [pos_div+1:pos_rbr]
			x = int (xs) + 2
			y = int (ys) + 2
			if x != 0 and y != 0:
				window = curses.newwin (y, x, 0, 0)
				window.border (0)
			else:
				return
		elif cmd == "SET":
			pos_rbr = line.find ("]")
			coord = line [pos_lbr+1:pos_rbr]
			xs = coord[:1]
			ys = coord[1:]
			x = ord (xs) - 64
			y = int (ys)
			if x != 0 and y != 0:
				window.addstr (y, x, "*")
		elif cmd == "REFR":
			window.refresh ()
			time.sleep (1)
		elif cmd == "MOVE":
			pos_div = line.find (":")
			xs = line [pos_lbr+1:pos_div]
			pos_rbr = line.find ("]")
			ys = line [pos_div+1:pos_rbr]
	curses.endwin ()
        
main ()