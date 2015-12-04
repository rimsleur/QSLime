#!/usr/bin/python
# coding: utf8

"""
Окно просмотра истории
"""

import sys
from PyQt4 import QtGui

class HistoryViewer (QtGui.QTextEdit):

	def __init__ (self, main_window):
		QtGui.QTextEdit.__init__ (self)

		main_window.history_viewer = self
		self.main_window = main_window

		self.setReadOnly (True)