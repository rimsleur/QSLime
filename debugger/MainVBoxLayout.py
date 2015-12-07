#!/usr/bin/python
# coding: utf8

"""
Вертикальный разделитель панели инструментов и окон отладчика
"""

import sys
from PyQt4 import QtGui
from ToolBar import ToolBar
from MainHSplitter import MainHSplitter

class MainVBoxLayout (QtGui.QVBoxLayout):

	def __init__ (self, main_window, central_widget):
		QtGui.QVBoxLayout.__init__ (self, central_widget)

		main_window.main_vbox_layout = self
		self.main_window = main_window

		self.setSpacing (0)
		toolbar = ToolBar (main_window)
		self.addWidget (toolbar)

		main_hsplitter = MainHSplitter (main_window)
		self.addWidget (main_hsplitter)