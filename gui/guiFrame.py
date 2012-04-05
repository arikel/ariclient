#!/usr/bin/python
# -*- coding: utf8 -*-

import pygame
import sys
import math
import re
import string

from guiFunctions import *
from guiWidget import Widget


#-----------------------------------------------------------------------
# Frame
#-----------------------------------------------------------------------		
class Frame(Widget):
	def __init__(self,
		width = 100,
		height = 20,
		bgcolor = (0,0,0),
		bordercolor = (200,200,200),
		hoverbordercolor = (255,255,255),
		borderwidth = 1,
		parent = None):
		
		Widget.__init__(self, 0, 0, width, height, parent)
		self.makeSurface()
		
		self.setBGColor(bgcolor)
		self.setBorderColor(bordercolor)
		self.borderWidth = borderwidth
		
	def autolayout(self, direction='vertical', autoexpand = False):
		x, y = 0, 0
		last_width, last_height = 0, 0
		for widget in self._children:
			padding = widget.getPadding()
			widget.setPos(x+padding, y+padding)
			
			last_width = widget.getWidth()
			last_height = widget.getHeight()
			
			if direction == 'horizontal':
				x += widget.getWidth() + 2 * padding
			elif direction == 'vertical':
				y += widget.getHeight() + 2 * padding
				
		if autoexpand:
			self.setWidth(x + last_width)
			self.setHeight(y + last_height)
	
		
	def updateSurface(self):
		self.surface.fill(self.borderColor)
		pygame.draw.rect(self.surface,
			self.bgColor,
			(self.borderWidth, self.borderWidth,
			self.width-2*self.borderWidth, self.height-2*self.borderWidth))
		
		Widget.updateSurface(self)
		
		
	def setBGColor(self, color):
		self.bgColor = color
		
	def setBorderColor(self, color):
		self.borderColor = color
		
	def setBorderWidth(self, width):
		self.borderWidth = int(width)
