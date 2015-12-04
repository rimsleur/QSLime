#!/usr/bin/python
# coding: utf8

"""
Панель инструментов
"""

import sys
from PyQt4 import QtCore, QtGui

class ToolBar (QtGui.QToolBar):

	def __init__ (self, main_window):
		QtGui.QToolBar.__init__ (self, 'ToolBar', main_window)

		main_window.toolbar = self
		self.main_window = main_window

		self.action_connect = QtGui.QAction (QtGui.QIcon ('qlpdbg/icons/connect.png'), u'Подключиться', self)
		self.addAction (self.action_connect)
		self.connect (self.action_connect, QtCore.SIGNAL ('triggered()'), self.action_do_connect)

		self.action_disconnect = QtGui.QAction (QtGui.QIcon ('qlpdbg/icons/disconnect_grey.png'), u'Отключиться', self)
		self.addAction (self.action_disconnect)
		self.connect (self.action_disconnect, QtCore.SIGNAL ('triggered()'), self.action_do_disconnect)

		self.resize (1000, 40)

	def action_do_connect (self):
		self.main_window.close ()

	def action_do_disconnect (self):
		self.main_window.close ()