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
		self.pipein = os.open ("/tmp/qlp-ctl-out", os.O_RDONLY | os.O_NONBLOCK)
		self.pipeout = os.open ("/tmp/qlp-ctl-in", os.O_WRONLY)

	def send (self, text):
		print text

	def receive (self):
		text = "OK"
		text = u"<b>система:</b> " + text
		return text

	def close (self):
		os.close (self.pipeout)
		os.close (self.pipein)