#!/usr/bin/python
# coding: utf8

"""
Центральный виджет главного окна
"""

import sys
from PyQt4 import QtGui
from MainVBoxLayout import MainVBoxLayout

class MainFrame (QtGui.QFrame):

	def __init__ (self, main_window):
		QtGui.QFrame.__init__ (self)

		main_window.main_frame = self
		self.main_window = main_window

		main_vbox_layout = MainVBoxLayout (main_window, self)
		self.setContentsMargins (-10,-10,-10,-10)
		self.setLayout (main_vbox_layout)