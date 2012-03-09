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
	
	click = False
	
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
		
		self.setText("  " + self.baseText + "  ")
		
	def OnClick(self):
		raise Exception('AbstractButton cannot be used directly, derivate it')
		
	def handleEvents(self, events):
		x, y = pygame.mouse.get_pos()
		
		for event in events:
				
			if event.type == pygame.MOUSEBUTTONDOWN:
				if pygame.mouse.get_pressed() == (1, 0, 0) and self.hover(x,y):
					self.click = True
					
			if event.type == pygame.MOUSEBUTTONUP:
				if self.click:
					self.click = False
					self.OnClick()
					
					
class ShowFrameButton(AbstractButton):
	
	click = False
	fshow = True
	
	def __init__(self,
		text= "Menu",
		font=FONT,
		width=0,
		height=0,
		widget=Frame()):
		AbstractButton.__init__(self, text, font, width, height, (86,111,175), (200,200,200), (255,255,255), 1)
		self.fshow = True
		self.widget = widget
		self._auxtext = text.split(':')
		self.setText("  " +  self._auxtext[self.fshow] + "  ")
		
	def OnClick(self):
		self.fshow = not self.fshow
		self.widget.show(self.fshow)
		self.setText("  " +  self._auxtext[self.fshow] + "  ")
		
