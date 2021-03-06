#!/usr/bin/python
# coding: utf8

"""
Панель инструментов
"""

import sys
from PyQt4 import QtCore, QtGui
from DebugDataProvider import DebugDataProvider

class ToolBar (QtGui.QToolBar):

	def __init__ (self, main_window):
		QtGui.QToolBar.__init__ (self, 'ToolBar', main_window)

		main_window.toolbar = self
		self.main_window = main_window

		#self.action_connect = QtGui.QAction (QtGui.QIcon ('../debugger/icons/connect.png'), u'Подключиться', self)
		#self.addAction (self.action_connect)
		#self.connect (self.action_connect, QtCore.SIGNAL ('triggered()'), self.action_on_connect)

		#self.action_disconnect = QtGui.QAction (QtGui.QIcon ('../debugger/icons/disconnect-grey.png'), u'Отключиться', self)
		#self.addAction (self.action_disconnect)
		#self.connect (self.action_disconnect, QtCore.SIGNAL ('triggered()'), self.action_on_disconnect)

		self.action_step_over = QtGui.QAction (QtGui.QIcon ('../debugger/icons/step-over.png'), u'Шаг без захода', self)
		self.action_step_over.setShortcut (QtGui.QKeySequence ("F4"))
		self.addAction (self.action_step_over)
		self.connect (self.action_step_over, QtCore.SIGNAL ('triggered()'), self.action_on_step_over)

		self.action_step_into_procedure = QtGui.QAction (QtGui.QIcon ('../debugger/icons/step-into-procedure.png'), u'Шаг с заходом в процедуру', self)
		self.action_step_into_procedure.setShortcut (QtGui.QKeySequence ("F5"))
		self.addAction (self.action_step_into_procedure)
		self.connect (self.action_step_into_procedure, QtCore.SIGNAL ('triggered()'), self.action_on_step_into_procedure)

		self.action_step_into_module = QtGui.QAction (QtGui.QIcon ('../debugger/icons/step-into-module.png'), u'Шаг с заходом в модуль', self)
		self.action_step_into_module.setShortcut (QtGui.QKeySequence ("F6"))
		self.addAction (self.action_step_into_module)
		self.connect (self.action_step_into_module, QtCore.SIGNAL ('triggered()'), self.action_on_step_into_module)

		self.action_step_out_procedure = QtGui.QAction (QtGui.QIcon ('../debugger/icons/step-out-procedure.png'), u'Шаг с выходом из процедуры', self)
		self.action_step_out_procedure.setShortcut (QtGui.QKeySequence ("F7"))
		self.addAction (self.action_step_out_procedure)
		self.connect (self.action_step_out_procedure, QtCore.SIGNAL ('triggered()'), self.action_on_step_out_procedure)

		self.action_step_out_module = QtGui.QAction (QtGui.QIcon ('../debugger/icons/step-out-module.png'), u'Шаг с выходом из модуля', self)
		self.action_step_out_module.setShortcut (QtGui.QKeySequence ("F8"))
		self.addAction (self.action_step_out_module)
		self.connect (self.action_step_out_module, QtCore.SIGNAL ('triggered()'), self.action_on_step_out_module)

		self.resize (1000, 40)

	def action_on_connect (self):
		pass

	def action_on_disconnect (self):
		pass

	def action_on_step_over (self):
		DebugDataProvider.set_step_type (DebugDataProvider.STEP_TYPE_STEP_OVER)
		self.main_window.statusBar ().showMessage (u'Отправка команды интерпретатору')
		DebugDataProvider.send_data ()
		self.main_window.statusBar ().showMessage (u'Ожидание ответа от интерпретатора')
		DebugDataProvider.receive_data ()
		DebugDataProvider.update_code_text ()
		self.main_window.statusBar ().showMessage (u'Готов')

	def action_on_step_into_procedure (self):

		DebugDataProvider.set_step_type (DebugDataProvider.STEP_TYPE_STEP_INTO_PROCEDURE)
		DebugDataProvider.send_data ()

	def action_on_step_into_module (self):
		DebugDataProvider.set_step_type (DebugDataProvider.STEP_TYPE_STEP_INTO_MODULE)
		DebugDataProvider.send_data ()

	def action_on_step_out_procedure (self):
		DebugDataProvider.set_step_type (DebugDataProvider.STEP_TYPE_STEP_OUT_PROCEDURE)
		DebugDataProvider.send_data ()

	def action_on_step_out_module (self):
		DebugDataProvider.set_step_type (DebugDataProvider.STEP_TYPE_STEP_OUT_MODULE)
		DebugDataProvider.send_data ()