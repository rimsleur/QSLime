#!/usr/bin/python
# coding: utf8

"""
Редактор команд
"""

import sys
from PyQt4 import QtGui

class Editor (QtGui.QTextEdit):

	def __init__ (self, main_window):
		QtGui.QTextEdit.__init__ (self)

		main_window.editor = self
		self.main_window = main_window