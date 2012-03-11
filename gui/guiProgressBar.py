#!/usr/bin/python
# -*- coding: utf8 -*-

import pygame
from guiFrame import Frame
from guiFunctions import *

class ProgressBar(Frame):
	"""A simple progress bar made with rectangles"""
	def __init__(self,
		minvalue = 0,
		maxvalue = 100,
		barcolor = (50,200,100),
		image = None,
		width = 100,
		height = 10,
		bgcolor = (0,0,0),
		bordercolor = (200,200,200),
		hoverbordercolor = (255,255,255),
		borderwidth = 1,
		parent = None):
		
		Frame.__init__(self, width, height, bgcolor, bordercolor, hoverbordercolor, borderwidth, parent)
		self.barcolor = barcolor
		self.minvalue = minvalue
		self.value = self.maxvalue = maxvalue
		self.image = image
		if image:
			print 'set renderer as image'
			self.render = self.drawImage
		else:
			self.render = self.drawRect
		
	def add(self, value):
		"""Increase the current absolute value of the progress bar"""
		self.value = bound(self.value + value, self.minvalue, self.maxvalue)
		self.updateSurface()
	
	def sub(self, value):
		"""Decrease the current absolute value of the progress bar"""
		self.value = bound(self.value - value, self.minvalue, self.maxvalue)
		self.updateSurface()
		
	def setValue(self, value):
		"""Set the current value of the progress bar"""
		self.value = bound(value, self.minvalue, self.maxvalue)
		self.updateSurface()
		
	def setColor(self, color):
		"""Change the bar color"""
		self.barcolor = color
		self.updateSurface()
		
	def _getPercentage(self):
		"""Get the current percentage value/(max-min)"""
		return float(self.value)/float(self.maxvalue-self.minvalue)
		
	def drawRect(self, w):
		pygame.draw.rect(self.surface,
			self.barcolor,
			(self.borderWidth+1, self.borderWidth+1,
			w, self.height-2*self.borderWidth-2))
			
	def drawImage(self, w):
		subimg = self.image.subsurface((0, 0, w, 6))
		self.surface.blit(subimg, (self.borderWidth+1, self.borderWidth+1))
		
	def updateSurface(self):
		percentage = self._getPercentage()
		lenght = max(int(percentage*self.width)-2*self.borderWidth-2, 0)
		Frame.updateSurface(self)
		self.render(lenght)


class HpBar(ProgressBar):
	"""A progress bar used to show Hp or Mp or Vp,
	   it has 3 colors binded to the 3 levels:
			High;
			Medium;
			Low;
	"""
	
	dir = 1
	
	def __init__(self,
		minvalue = 0,
		maxvalue = 100,
		barcolors = ((50,200,100), (200, 200, 50), (200,20, 50)),
		width = 100,
		height = 20,
		bgcolor = (0,0,0),
		bordercolor = (200,200,200),
		hoverbordercolor = (255,255,255),
		borderwidth = 1,
		parent=None):
			ProgressBar.__init__(self,minvalue, maxvalue, barcolors[0], None, width, height, bgcolor, bordercolor, hoverbordercolor, borderwidth, parent)
			self.barcolors = barcolors
			
	def setColor(self, color, level):
		"""Set the desired color for the value level: 
			0 or 'low,
			1 or 'medium',
			2 or 'high'
		"""
		if level not in (2, 1, 0, 'high', 'medium', 'low'):
			return
		if type(level) is not int:
			level = {'high': 1, 'medium': 1, 'low': 0}[level]
		self.barcolors[level] = color
		self.updateSurface()
	
	def _getPercentage(self):
		"""Calculate the percentage and set the right color for the bar"""

		perc = float(self.value)/float(self.maxvalue-self.minvalue)
		
		if perc < .34:
			self.barcolor = self.barcolors[2]
		elif perc < .67:
			self.barcolor = self.barcolors[1]
		else:
			self.barcolor = self.barcolors[0]

		return perc
			
	def jam(self):
		self.value += self.dir
		if self.value > self.maxvalue:
			self.dir = -1
		if self.value < self.minvalue:
			self.dir = 1

		self.value = bound(self.value, self.minvalue, self.maxvalue)
		self.updateSurface()
