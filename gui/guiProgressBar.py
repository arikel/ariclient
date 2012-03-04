import pygame
from guiFrame import Frame
from guiFunctions import *

class ProgressBar(Frame):
	"""A simple progress bar made with rectangles"""
	def __init__(self,
		minvalue = 0,
		maxvalue = 100,
		barcolor = (50,200,100),
		width = 100,
		height = 20,
		bgcolor = (0,0,0),
		bordercolor = (200,200,200),
		hoverbordercolor = (255,255,255),
		borderwidth = 1):
		
		Frame.__init__(self, width, height, bgcolor, bordercolor, hoverbordercolor, borderwidth = 1)
		self.barcolor = barcolor
		self.minvalue = minvalue
		self.value = self.maxvalue = maxvalue
		
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
		
	def _gerPercentage(self):
		"""Get the current percentage value/(max-min)"""
		return float(self.value)/float(self.maxvalue-self.minvalue)
		
	def updateSurface(self):
		percentage = self._getPercentage()
		lenght = max(int(percentage*self.width)-2*self.borderWidth-2, 0)
		Frame.updateSurface(self)
		pygame.draw.rect(self.surface,
			self.barcolor,
			(self.borderWidth+1, self.borderWidth+1,
			lenght, self.height-2*self.borderWidth-2))


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
		borderwidth = 1):
			ProgressBar.__init__(self,minvalue, maxvalue, barcolors[0], width, height, bgcolor, bordercolor, hoverbordercolor, borderwidth = 1)
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
