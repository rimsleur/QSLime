#!/usr/bin/python
# coding: utf8

"""
Вертикальный разделитель панели инструментов и редактора
"""

import sys
from PyQt4 import QtGui
from ToolBar import ToolBar
from Editor import Editor

class VBoxLayout (QtGui.QVBoxLayout):

	def __init__ (self, main_window):
		QtGui.QVBoxLayout.__init__ (self)

		main_window.vbox_layout = self
		self.main_window = main_window

		self.setSpacing (0)
		toolbar = ToolBar (main_window)
		self.addWidget (toolbar)

		editor = Editor (main_window)
		self.addWidget (editor)