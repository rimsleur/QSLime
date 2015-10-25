#!/usr/bin/python
# coding: utf8
"""
Отладчик
Точка входа
"""

import sys
from PyQt4 import QtGui
from MainWindow import MainWindow

def main ():
	#exit = False
	#pipein = open ("/tmp/qlp-dbg-out", "r")
	#pipeout = open ("/tmp/qlp-dbg-in", "w")

	app = QtGui.QApplication (sys.argv)
	main_window = MainWindow ()
	main_window.show ()
	sys.exit (app.exec_ ())

	#pipein.close ()
	#pipeout.close ()

main ()