#!/usr/bin/python
# coding: utf8

"""
Окно просмотра информации по объектам кода (константы, поля, записи, таблицы, списки)
"""

import sys
from PyQt4 import QtGui

class ObjectViewer (QtGui.QTableView):

	def __init__ (self, main_window):
		QtGui.QTableView.__init__ (self)

		main_window.object_viewer = self
		self.main_window = main_window