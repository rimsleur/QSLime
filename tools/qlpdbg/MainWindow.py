#!/usr/bin/python
# coding: utf8

"""
Главное окно
"""

import sys
from PyQt4 import QtGui
from MainHSplitter import MainHSplitter
from MainVSplitter import MainVSplitter

class MainWindow (QtGui.QMainWindow):

	def __init__ (self):
		QtGui.QMainWindow.__init__ (self)
		
		self.setWindowTitle (u'Отладчик')
		self.statusBar ().showMessage (u'Готов')

		central_widget = QtGui.QWidget ()
		self.main_vbox = MainHSplitter (self, central_widget)
		self.setCentralWidget (central_widget)

		self.resize (1000, 522)
		