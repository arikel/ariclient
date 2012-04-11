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
		bgcolor = COLOR_BG,
		bordercolor = COLOR,
		hoverbordercolor = COLOR_HOVER,
		borderwidth = 1,
		parent = None):
		
		Widget.__init__(self, 0, 0, width, height, parent)
		
		self.setBGColor(bgcolor)
		self.setBorderColor(bordercolor)
		self.borderWidth = borderwidth
		
		self.makeSurface()
		
	def autolayout(self, direction = 'vertical', autoexpand = False, griditems = 1):
		
		assert griditems > 0
		
		x, y = 0, 0
		itemsCounter = 1
		for widget in self._children:
			padding = widget.getPadding()
			widget.setPos(x+padding, y+padding)
			
			if itemsCounter < griditems and griditems > 1:
				if direction == 'vertical':
					x += widget.getWidth() + 2 * padding
				elif direction == 'horizontal':
					y += widget.getHeight() + 2 * padding
				itemsCounter +=1
			else:
				itemsCounter = 1
				if direction == 'horizontal':
					y = 0
					x += widget.getWidth() + 2 * padding
				elif direction == 'vertical':
					x = 0
					y += widget.getHeight() + 2 * padding
			
		if autoexpand:
			#yet buggy
			self.setWidth(x + widget.getWidth())
			self.setHeight(y + widget.getWidth())
			self.updateSurface()
		
	def makeSurface(self):
		Widget.makeSurface(self)
		self.surface.fill(self.borderColor)
		pygame.draw.rect(self.surface,
			self.bgColor,
			(self.borderWidth, self.borderWidth,
			self.width-2*self.borderWidth, self.height-2*self.borderWidth))
		
	def setBGColor(self, color):
		self.bgColor = color
		
	def setBorderColor(self, color):
		self.borderColor = color
		
	def setBorderWidth(self, width):
		self.borderWidth = int(width)
