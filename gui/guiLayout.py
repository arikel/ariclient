#!/usr/bin/python
# -*- coding: utf8 -*-

import pygame
from guiFunctions import *
from guiWidget import Widget

class BaseLayouter(Widget):
	
	layoutercount = 0
	
	def __init__(self, parent=None, direction='horizontal'):
		self.initRect(0, 0, 0, 0)
		self.c = BaseLayouter.layoutercount
		BaseLayouter.layoutercount += 1
		self.set_parent(parent)
		self.direction = direction
		self.set_parent(parent)
		self._widgets = []
		
	def __del__(self):
		BaseLayouter.layoutercount -= 1

	def __repr__(self):
		return '<%s %d>' % (self.__class__.__name__, self.c)
	
	def __str__(self):
		return self.__repr__()
		
	def add(self, widget, padding = 0):
		self._widgets.append((widget, padding))
	
	def remove(self, widget):
		#map(lambda x, y: del x, self._widgets)
		pass
		
	def fit(self):
		x, y = self.x, self.y
		for widget, padding in self._widgets:
			widget.setPos(x+padding, y+padding)			
			if type(widget) == type(self):
				widget.fit()

			if widget.getWidth() > self.getWidth():
				self.setWidth(widget.getWidth())
			if widget.getHeight() > self.getHeight():
				self.setHeight(widget.getHeight())	
			
			if self.direction == 'horizontal':
				x += widget.getWidth() + 2 * padding
			elif self.direction == 'vertical':
				y += widget.getHeight() + 2 * padding

