#!/usr/bin/python
# coding: utf8

"""
Главное окно
"""

import sys
from PyQt4 import QtCore, QtGui
from MainFrame import MainFrame
from Channel import Channel
from DebugDataProvider import DebugDataProvider

class MainWindow (QtGui.QMainWindow):

	def __init__ (self, application):
		QtGui.QMainWindow.__init__ (self)

		self.channel = Channel ()
		self.channel.open ()

		self.application = application
		self.setWindowTitle (u'Отладчик')

		main_frame = MainFrame (self)
		self.setCentralWidget (main_frame)

		self.connect (application, QtCore.SIGNAL ('aboutToQuit()'), self.on_quit)

		self.statusBar ().showMessage (u'Готов')

		DebugDataProvider (self)
		DebugDataProvider.receive_data ()
		DebugDataProvider.update_code_text ()

		self.resize (1000, 300)

	def on_quit (self):
		self.channel.close ()