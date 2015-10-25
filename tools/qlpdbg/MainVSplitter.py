#!/usr/bin/python
# coding: utf8

"""
Главный вертикальный разделитель
"""

import sys
from PyQt4 import QtCore, QtGui
from CodeViewer import CodeViewer

class MainVSplitter (QtGui.QSplitter):

	def __init__ (self, main_window):
		QtGui.QSplitter.__init__ (self)

		main_window.main_vsplitter = self
		self.main_window = main_window

		self.setOrientation (QtCore.Qt.Vertical)

		code_viewer = CodeViewer (main_window)
		self.addWidget (code_viewer)

		#textedit = QtGui.QTextEdit ()
		#self.addWidget (textedit)