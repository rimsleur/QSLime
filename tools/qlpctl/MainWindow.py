#!/usr/bin/python
# coding: utf8

"""
Главное окно
"""

import sys
from PyQt4 import QtGui
from MainVSplitter import MainVSplitter

class MainWindow (QtGui.QMainWindow):

	def __init__ (self):
		QtGui.QMainWindow.__init__ (self)
		
		self.setWindowTitle (u'Контроллер')

		central_widget = QtGui.QWidget ()
		self.main_vsplitter = MainVSplitter (self, central_widget)
		self.setCentralWidget (central_widget)

		self.statusBar ().showMessage (u'Готов')

		self.resize (800, 600)
		