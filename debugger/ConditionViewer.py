#!/usr/bin/python
# coding: utf8

"""
Окно просмотра информации по условиям
"""

import sys
from PyQt4 import QtGui

class ConditionViewer (QtGui.QTableView):

	def __init__ (self, main_window):
		QtGui.QTableView.__init__ (self)

		main_window.condition_viewer = self
		self.main_window = main_window