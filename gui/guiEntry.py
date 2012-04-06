#!/usr/bin/python
# -*- coding: utf8 -*-

import pygame
import sys
import math
import re
import string

from guiFunctions import *
from guiWidget import Widget
from guiLabel import Label


#-----------------------------------------------------------------------
# TextEntry
#-----------------------------------------------------------------------	
class TextEntry(Label):
	def __init__(self,
		text= "OK",
		font=FONT,
		width=0,
		height=0,
		bgcolor=COLOR_BG,
		bordercolor=COLOR,
		hoverbordercolor=COLOR_HOVER, 
		borderwidth = 1,
		parent=None):
		
		self.has_focus = False
		self.shift = False
		
		Label.__init__(self, text, font, width, height, bgcolor, bordercolor, hoverbordercolor, borderwidth, parent)
		
		
	def getFocus(self):
		self.has_focus = True
		self.setText(self.baseText)
		
	def loseFocus(self):
		self.has_focus = False
		self.setText(self.baseText)
	
	def setText(self, msg):
		self.baseText = msg
		self.text = ustr(msg) #unicode(msg, "utf-8")
		if self.has_focus:
			self.msg = self.font.render(self.text + "_", False, self.borderColor)
		else:
			self.msg = self.font.render(self.text, False, self.borderColor)
		self.msgRect = self.msg.get_rect()
		if self.w < self.msgRect.width+self.padding*2:
			self.width = self.msgRect.width+self.padding*2
		if self.height < self.msgRect.height+self.padding*2:
			self.height = self.msgRect.height+self.padding*2
		
		self.makeSurface()
		self.updateSurface()
	
	def handleEvents(self, events=None):
		if not self.has_focus or events==None:
			return None
		for event in events:
			if event.type == pygame.KEYDOWN:
				key = event.key
				if key == pygame.K_ESCAPE:
					self.baseText = ""
					self.setText(self.baseText)
					self.loseFocus()
					return None
				if key == pygame.K_BACKSPACE:
					self.baseText = self.baseText[0:-1]
				elif key == pygame.K_SPACE:
					self.baseText = self.baseText + " "
				elif key == pygame.K_MINUS:
					self.baseText = self.baseText + "_"
				elif 33<=key<=127:
					toAdd = ustr(event.unicode)
					self.baseText = self.baseText + toAdd
					
				elif key == pygame.K_RETURN:
					#res = self.baseText
					#self.baseText = ""
					#self.setText(self.baseText)
					#return res
					return self.baseText
					
				elif key == 303 or key == 304:
					self.shift = True
				else:
					print "Key %s was pressed, unicode = %s" % (key, event.unicode)
					toAdd = ustr(event.unicode)
					if len(toAdd.strip())>0:
						self.baseText = self.baseText + toAdd
				
				self.setText(self.baseText)
			
			if event.type == pygame.KEYUP:
				key = event.key
				if key == 303 or key == 304:
					self.shift = False
		return None
	
	# blit	
	def blit(self, screen):
		#if self.has_focus:
		screen.blit(self.surface, self)





