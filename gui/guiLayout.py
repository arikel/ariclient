#!/usr/bin/python
# -*- coding: utf8 -*-

import pygame
from guiFunctions import *
from guiWidget import Widget

class BaseLayouter(Widget):
	
	layoutercount = 0
	
	def __init__(self,direction='horizontal', parent=None):
		self.c = BaseLayouter.layoutercount
		Widget.__init__(self, 0, 0, 0, 0, parent)
		BaseLayouter.layoutercount += 1
		self.direction = direction
		self.set_parent(parent)
		if parent:
			self.surface = parent.surface
		self._widgets = []
		
	def __del__(self):
		BaseLayouter.layoutercount -= 1

	def __repr__(self):
		return '<%s %x>' % (self.__class__.__name__, self.c)
	
	def __str__(self):
		return self.__repr__()
		
	def add(self, widget, padding = 0):
		self._widgets.append((widget, padding))
	
	def remove(self, widget):
		#map(lambda x, y: del x, self._widgets)
		pass
		
	def doblit(self, *args):
		for child in self._children:
			child.blit(self.surface)
			print 'drawing %s at %d,%d' % (child, child.x, child.y)
		
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

