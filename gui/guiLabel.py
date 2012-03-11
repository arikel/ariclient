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


#-----------------------------------------------------------------------
# Label
#-----------------------------------------------------------------------	
class Label(Frame):
	def __init__(self,
		text= "OK",
		font=FONT,
		width=0,
		height=0,
		bgcolor=(100,100,100),
		bordercolor=(255,255,255),
		hoverbordercolor=(255,255,255), 
		borderwidth = 1,
		parent=None):
		Frame.__init__(self, width, height, bgcolor, bordercolor, hoverbordercolor, borderwidth, parent)
		
		self.baseText = text
		self.padding = 2
		self.font = font
		
		self.setText(self.baseText)
		
		
	def setText(self, msg):
		self.baseText = msg
		self.text = ustr(msg) #unicode(msg, "utf-8")
		self.msg = self.font.render(self.text, False, self.borderColor)
		self.msgRect = self.msg.get_rect()
		
		self.width = self.msgRect.width+self.padding*2
		self.height = self.msgRect.height+self.padding*2
		#self.msgRect.topleft = self.rect.topleft
		
		self.surface = self.makeSurface()
		self.updateSurface()
	
		
	def updateSurface(self):
		Frame.updateSurface(self)
		self.surface.blit(self.msg, (self.msgRect.left+self.padding,self.msgRect.top+self.padding,self.msgRect.width,self.msgRect.height))
		#self.surface.blit(self.msg, (0,0,self.msgRect.width,self.msgRect.height))

#-----------------------------------------------------------------------
# FixedLabel
#-----------------------------------------------------------------------
class FixedLabel(Frame):
	def __init__(self,
		text= "OK",
		font=FONT,
		width=0,
		height=0,
		bgcolor=(0,0,0),
		bordercolor=(255,255,255),
		hoverbordercolor=(255,255,255),
		borderwidth = 1):
		Frame.__init__(self, width, height, bgcolor, bordercolor, hoverbordercolor, borderwidth = 1)
		
		self.baseText = text
		self.padding = 5
		self.font = font
		
		self.setText(self.baseText)
		
	def setText(self, msg):
		self.baseText = msg
		self.text = unicode(msg, "utf-8")
		self.msg = self.font.render(self.text, False, self.borderColor)
		self.msgRect = self.msg.get_rect()		
		self.makeSurface()

	def updateSurface(self, x=0, y=0):
		Frame.updateSurface(self)
		self.surface.blit(self.msg, (self.msgRect.left+self.padding,self.msgRect.top+self.padding/2,self.msgRect.width,self.msgRect.height))

