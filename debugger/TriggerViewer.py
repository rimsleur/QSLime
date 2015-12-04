#!/usr/bin/python
# coding: utf8

"""
Окно просмотра информации по триггерам
"""

import sys
from PyQt4 import QtGui

class TriggerViewer (QtGui.QTableView):

	def __init__ (self, main_window):
		QtGui.QTableView.__init__ (self)

		main_window.trigger_viewer = self
		self.main_window = main_window