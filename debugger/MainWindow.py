#!/usr/bin/python
# coding: utf8

"""
Главное окно
"""

import sys
from PyQt4 import QtCore, QtGui
from MainHSplitter import MainHSplitter
from MainVSplitter import MainVSplitter
from ToolBar import ToolBar
from Channel import Channel

class MainWindow (QtGui.QMainWindow):

	def __init__ (self, application):
		QtGui.QMainWindow.__init__ (self)

		self.channel = Channel ()
		self.channel.open ()

		self.application = application
		self.setWindowTitle (u'Отладчик')

		central_widget = QtGui.QWidget ()
		self.main_vbox = MainHSplitter (self, central_widget)
		self.setCentralWidget (central_widget)

		self.connect (application, QtCore.SIGNAL ('aboutToQuit()'), self.on_quit)

		self.toolbar = ToolBar (self)
		self.statusBar ().showMessage (u'Готов')

		self.code_viewer.append (QtCore.QString.fromUtf8 (self.channel.receive ()))

		self.resize (1000, 522)

	def on_quit (self):
		self.channel.close ()