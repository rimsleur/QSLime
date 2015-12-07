#!/usr/bin/python
# coding: utf8

"""
Окно просмотра исходного кода
"""

import sys
from PyQt4 import QtGui

class CodeViewer (QtGui.QTextEdit):

	def __init__ (self, main_window):
		QtGui.QTextEdit.__init__ (self)

		main_window.code_viewer = self
		self.main_window = main_window

		self.setReadOnly (True)

		self.setViewportMargins (20, 0, 0, 0);