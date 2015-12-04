#!/usr/bin/python
# coding: utf8

"""
Контейнер закладок
"""

import sys
from PyQt4 import QtGui
from TriggerViewer import TriggerViewer
from ConditionViewer import ConditionViewer
from ObjectViewer import ObjectViewer

class TabContainer (QtGui.QTabWidget):

	def __init__ (self, main_window):
		QtGui.QTabWidget.__init__ (self)

		main_window.tab_container = self
		self.main_window = main_window

		self.setTabPosition (QtGui.QTabWidget.South)
		self.setTabShape (QtGui.QTabWidget.Triangular)

		object_viewer = ObjectViewer (main_window)
		self.addTab (object_viewer, u'Объекты')

		trigger_viewer = TriggerViewer (main_window)
		self.addTab (trigger_viewer, u'Триггеры')

		condition_viewer = ConditionViewer (main_window)
		self.addTab (condition_viewer, u'Условия')