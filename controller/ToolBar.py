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

		self.action_connect = QtGui.QAction (QtGui.QIcon ('../controller/icons/enter.png'), u'Отправить', self)
		self.addAction (self.action_connect)
		self.connect (self.action_connect, QtCore.SIGNAL ('triggered()'), self.action_on_send)

		self.resize (800, 40)

	def action_on_send (self):
		text = unicode (self.main_window.editor.toPlainText ())
		if text != "":
			self.main_window.statusBar ().showMessage (u'Отправка сообщения')
			self.main_window.channel.send (text)
			self.main_window.history_viewer.append (u'<b>пользователь:</b> ' + text)
			self.main_window.editor.clear ()
			self.main_window.statusBar ().showMessage (u'Ожидание ответа')
			self.main_window.history_viewer.append (self.main_window.channel.receive ())
			self.main_window.statusBar ().showMessage (u'Готов')