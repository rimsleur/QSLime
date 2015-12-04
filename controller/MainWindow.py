#!/usr/bin/python
# coding: utf8

"""
Главное окно
"""

import sys
from PyQt4 import QtCore, QtGui
from MainVSplitter import MainVSplitter
from Channel import Channel

class MainWindow (QtGui.QMainWindow):

	def __init__ (self, application):
		QtGui.QMainWindow.__init__ (self)
		
		self.channel = Channel ()
		self.channel.open ()

		self.application = application
		self.setWindowTitle (u'Контроллер')

		central_widget = QtGui.QWidget ()
		self.main_vsplitter = MainVSplitter (self, central_widget)
		self.setCentralWidget (central_widget)

		self.connect (application, QtCore.SIGNAL ('aboutToQuit()'), self.on_quit)

		self.statusBar ().showMessage (u'Готов')

		self.resize (800, 600)

	def on_quit (self):
		self.channel.close ()
		