#!/usr/bin/python
# coding: utf8

"""
Главный горизонтальный разделитель
"""

import sys
from PyQt4 import QtGui
from MainVSplitter import MainVSplitter
from TabContainer import TabContainer

class MainHSplitter (QtGui.QSplitter):

	def __init__ (self, main_window, central_widget):
		QtGui.QSplitter.__init__ (self, central_widget)

		main_window.main_hsplitter = self
		self.main_window = main_window

		main_vsplitter =  MainVSplitter (main_window)
		main_window.main_vsplitter = main_vsplitter
		self.addWidget (main_vsplitter)

		tab_container = TabContainer (main_window)
		self.addWidget (tab_container)

		self.resize (1000, 500)