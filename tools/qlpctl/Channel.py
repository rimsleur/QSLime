#!/usr/bin/python
# coding: utf8

"""
Канал взаимодействия с интерпретатором
"""

import sys
import os
from PyQt4 import QtGui

class Channel ():

	def __init__ (self):
		self.pipein = None
		self.pipeout = None

	def open (self):
		self.pipein = open ("/tmp/qlp-ctl-out", 'r')
		self.pipeout = os.open ("/tmp/qlp-ctl-in", os.O_WRONLY)

	def send (self, text):
		os.write (self.pipeout, (text + u'\n').encode("utf-8"))

	def receive (self):
		text = u"<b>система:</b> " + self.pipein.readline ()
		return text

	def close (self):
		os.close (self.pipein)
		os.close (self.pipeout)