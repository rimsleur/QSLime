#!/usr/bin/python
# coding: utf8
"""
Контроллер
Точка входа
"""

import sys
from PyQt4 import QtGui
from MainWindow import MainWindow

def main ():
	application = QtGui.QApplication (sys.argv)
	main_window = MainWindow (application)
	main_window.show ()
	sys.exit (application.exec_ ())

main ()