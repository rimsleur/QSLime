#!/usr/bin/python
# coding: utf8

"""
Главный горизонтальный изменяемый разделитель
"""

import sys
from PyQt4 import QtGui
from MainVSplitter import MainVSplitter
from TabContainer import TabContainer

class MainHSplitter (QtGui.QSplitter):

	def __init__ (self, main_window):
		QtGui.QSplitter.__init__ (self)

		main_window.main_hsplitter = self
		self.main_window = main_window

		main_vsplitter =  MainVSplitter (main_window)
		main_window.main_vsplitter = main_vsplitter
		self.addWidget (main_vsplitter)

		tab_container = TabContainer (main_window)
		self.addWidget (tab_container)

		self.setStretchFactor (0, 3)
		self.setStretchFactor (1, 1)