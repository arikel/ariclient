#!/usr/bin/python
# -*- coding: utf8 -*-

import pygame
import sys
import math
import re
import string

from guiFunctions import *
from guiWindow import Window
from guiTextArea import TextArea
from guiButton import TextButton


OK = 0
YESNO = 1

class MessageBox(Window):
	
	def __init__(self,
		message,
		title = 'MessageBox',
		buttons = OK,
		width = 200,
		height = 150,
		bgcolor = COLOR_BG,
		bordercolor = COLOR,
		hoverbordercolor = COLOR_HOVER,
		borderwidth = 1,
		parent = None,
		gui = None):
		
		Window.__init__(self, title, width, height, bgcolor, bordercolor, hoverbordercolor, borderwidth, parent, gui)
		
		self.buttons = buttons
		self.message = message
		
		self.textMessage = TextArea(self.message,\
									width=int(width*0.9),\
									bgcolor=bgcolor,\
									bordercolor=bordercolor,\
									hoverbordercolor=bordercolor,\
									borderwidth = 0,\
									parent=self)
									
		self.yesButton = TextButton("Yes", color_bg=bgcolor,\
									color=bordercolor,\
									color_hover=bordercolor,\
									borderwidth = borderwidth,\
									parent=self)
		self.noButton = TextButton("No", color_bg=bgcolor,\
									color=bordercolor,\
									color_hover=bordercolor,\
									borderwidth = borderwidth,\
									parent=self)
		self.okButton = TextButton("Ok", color_bg=bgcolor,\
									color=bordercolor,\
									color_hover=bordercolor,\
									borderwidth = borderwidth,\
									parent=self)

		self.textMessage.setPadding(int(width*0.03))
		self.lastclickedbutton = None
		self.yesButton.bind(self.setClickedButton, 'yes')
		self.noButton.bind(self.setClickedButton, 'no')
		self.okButton.bind(self.setClickedButton, 'ok')
		
		if buttons == YESNO:
			self.yesButton.show()
			self.noButton.show()
			self.okButton.hide()
		elif buttons == OK:
			self.yesButton.hide()
			self.noButton.hide()
			self.okButton.show()
			
		self.autolayout(offset=(0,30))
		self.hide()
		
	def setMessageBox(self, message, buttons=OK):
		self.message = message
		self.buttons = buttons
		if buttons == YESNO:
			self.yesButton.show()
			self.noButton.show()
			self.okButton.hide()
		elif buttons == OK:
			self.yesButton.hide()
			self.noButton.hide()
			self.okButton.show()
		self.textMessage.setText(message)
		self.autolayout(offset=(0,30))
		
	def setClickedButton(self,button):
		self.lastclickedbutton = button
		self.hide()
		
	def getClickedButton(self):
		clicked = self.lastclickedbutton
		self.lastclickedbutton = None
		return clicked
