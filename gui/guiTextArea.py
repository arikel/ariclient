#!/usr/bin/python
# -*- coding: utf8 -*-

import pygame
import sys
import math
import re
import string

from guiFunctions import *
from guiWidget import Widget
from guiFrame import Frame
from guiLabel import Label

class TextArea(Label):
	
	def __init__(self,
		text= "OK",
		textcolor=COLOR,
		font=FONT,
		width=80,
		height=20,
		bgcolor=COLOR_BG,
		bordercolor=COLOR,
		hoverbordercolor=COLOR_HOVER, 
		borderwidth = 1,
		parent=None):
		
		self.i = 0
		#Frame.__init__(self, width, height, bgcolor, bordercolor, hoverbordercolor, borderwidth, parent)
		
		self.lineStep = 14
		self.baseText = text
		self.padding = 2
		self.font = font
		self.textColor = textcolor
		
		Label.__init__(self, text, font, width, height, bgcolor, bordercolor, hoverbordercolor, borderwidth, parent)
		self.setText(self.baseText)
		
		
	def setText(self, msg):
		self.baseText = msg
		self.text = ustr(msg) #unicode(msg, "utf-8")
		nbLines = 0
		lines = []

		for line in self.text.split("\n"):
			toAdd = coupeMsg(line, self.w, self.font)
			lines.extend(toAdd)
			nbLines += len(toAdd)
			
		self.msg = pygame.Surface((self.w, len(lines)*self.lineStep))
		self.msg.fill(self.bgColor)
		
		self.msgRect = self.msg.get_rect()
		if self.w < self.msgRect.width+self.padding*2:
			self.width = self.msgRect.width+self.padding*2
		if self.height < self.msgRect.height+self.padding*2:
			self.height = self.msgRect.height+self.padding*2
		
		n=0
		for line in lines:
			(w, h) = self.font.size(line)
			msg = self.font.render(line, False, self.textColor)
			self.msg.blit(msg, (0,n*self.lineStep, w, h))
			n += 1

		self.makeSurface()
		self.updateSurface()

	def updateSurface(self):
		Frame.updateSurface(self)
		self.surface.blit(self.msg, (self.msgRect.left+self.padding,self.msgRect.top+self.padding,self.msgRect.width,self.msgRect.height))
		
