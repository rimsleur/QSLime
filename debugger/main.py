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
	app = QtGui.QApplication (sys.argv)
	main_window = MainWindow (app)
	main_window.show ()
	sys.exit (app.exec_ ())

main ()