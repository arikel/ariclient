#!/usr/bin/python
# -*- coding: utf8 -*-

import pygame
import sys
import math
import re
import string

from guiFunctions import *
from guiLabel import Label
from guiFrame import Frame

#-----------------------------------------------------------------------
# Button
#-----------------------------------------------------------------------	
class AbstractButton(Label):
	
	def __init__(self,
		text= "OK",
		font=FONT,
		width=0,
		height=0,
		bgcolor=(100,100,100),
		bordercolor=(255,255,255),
		hoverbordercolor=(255,255,255), 
		borderwidth = 1):
		Label.__init__(self, text, font, width, height, bgcolor, bordercolor, hoverbordercolor, borderwidth)
		
		self.baseText = text
		self.padding = 2
		self.font = font
		
		self.click = False
		
		self.setText("  " + self.baseText + "  ")
		
	def OnClick(self):
		raise Exception('AbstractButton cannot be used directly, derivate it')
		
	def handleEvents(self, events):
		
		for event in events:
				
			if event.type == pygame.MOUSEBUTTONDOWN:
				if event.button == 1 and self.hover:
					self.click = True
					
			if event.type == pygame.MOUSEBUTTONUP:
				if self.click and self.hover:
					self.click = False
					self.OnClick()
					#print "AbstractButton OnClick"
					
					
class ShowFrameButton(AbstractButton):
	
	def __init__(self,
		text= "Menu",
		font=FONT,
		width=0,
		height=0,
		widget=Frame()):
		AbstractButton.__init__(self, text, font, width, height, (86,111,175), (200,200,200), (255,255,255), 1)
		self.widget = widget
		self._auxtext = text.split(':')
		#self.setText("  " +  self._auxtext[widget.is_visible()] + "  ")
		self.setText("  " +  self._auxtext[widget.visible] + "  ")
		
	def OnClick(self):
		#fshow = not self.widget.is_visible()
		#fshow = not self.widget.visible
		if not self.visible:
			return
		if self.widget.visible:
			self.widget.hide()
		else:
			self.widget.show()
		#self.widget.show(fshow)
		#self.setText("  " +  self._auxtext[fshow] + "  ")
		self.setText("  " +  self._auxtext[self.visible] + "  ")
		
