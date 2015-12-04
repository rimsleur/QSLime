#!/usr/bin/python
# coding: utf8

"""
Главный вертикальный разделитель
"""

import sys
from PyQt4 import QtCore, QtGui
from HistoryViewer import HistoryViewer
from VBoxLayout import VBoxLayout

class MainVSplitter (QtGui.QSplitter):

	def __init__ (self, main_window, central_widget):
		QtGui.QSplitter.__init__ (self, central_widget)

		main_window.main_vsplitter = self
		self.main_window = main_window

		self.setOrientation (QtCore.Qt.Vertical)

		history_viewer = HistoryViewer (main_window)
		self.addWidget (history_viewer)

		vbox_layout = VBoxLayout (main_window)
		frame = QtGui.QFrame ()
		frame.setLayout (vbox_layout)
		frame.setContentsMargins (-10,-10,-10,-10)
		self.addWidget (frame)

		self.setStretchFactor (0, 3)
		self.setStretchFactor (1, 1)

		self.resize (800, 600)