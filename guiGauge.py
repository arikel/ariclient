import pygame
from guiEntry import Frame
from guiFunctions import *

class Gauge(Frame):
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
		self.value = bound(self.value + value, self.minvalue, self.maxvalue)
		self.updateSurface()
	
	def sub(self, value):
		self.value = bound(self.value - value, self.minvalue, self.maxvalue)
		self.updateSurface()
		
	def setValue(self, value):
		self.value = bound(value, self.minvalue, self.maxvalue)
		self.updateSurface()
		
	def setColor(self, color):
		self.barcolor = color
		self.updateSurface()
		
	def _gerPercentage(self):
		return float(self.value)/float(self.maxvalue-self.minvalue)
		
	def updateSurface(self):
		percentage = self._getPercentage()
		lenght = max(int(percentage*self.width)-2*self.borderWidth-2, 0)
		Frame.updateSurface(self)
		pygame.draw.rect(self.surface,
			self.barcolor,
			(self.borderWidth+1, self.borderWidth+1,
			lenght, self.height-2*self.borderWidth-2))


class HpBar(Gauge):
	
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
			Gauge.__init__(self,minvalue, maxvalue, barcolors[0], width, height, bgcolor, bordercolor, hoverbordercolor, borderwidth = 1)
			self.barcolors = barcolors
	
	def _getPercentage(self):

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
