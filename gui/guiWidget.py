#!/usr/bin/python
# -*- coding: utf8 -*-

import pygame
from guiFunctions import *

#-----------------------------------------------------------------------
# Widget
#-----------------------------------------------------------------------
class Widget(pygame.Rect):
	"""Main class used to define all the GUI components"""
	_hover = False
	
	# rect
	def __init__(self, x=0, y=0, width=10, height=10, parent=None):
		#self.rect = pygame.Rect(x, y, width, height)
		pygame.Rect.__init__(self, x, y, width, height)
		self._parent = parent
		self.setPos(x,y)
		if parent:
			parent.add_child(self)
		self._children = []
		self.show()

	# width
	def getWidth(self):
		"""Returns the width of the widget"""
		return self.width		
	def setWidth(self, x):
		"""Sets the width of the widget"""
		self.width = int(x)
	# height
	def getHeight(self):
		"""Returns the height of the widget"""
		return self.height
	def setHeight(self, x):
		"""Sets the height of the widget"""
		self.height = int(x)
	# pos
	def set_parent(self, _parent):
		"""Sets the parent widget"""
		self._parent = _parent

	def reparentTo(self, _parent):
		"""Changes the parent of the widget"""
		self.set_parent(_parent)
		
	def add_child(self, child):
		self._children.append(child)
		
	def detach(self):
		"""Detatch the widget from its parent"""
		self._parent = None
		
	def getPos(self):
		"""Returns the widget position as a touple (x, y)
		if the widget is a child of another widget the position
		is relative to the parent widget"""
		if self._parent:
			return (self.x-self._parent.x, self.y-self._parent.y)
		return self.topleft
		
	def setPos(self, x, y):
		"""Sets the widget position
		if the widget is a child of another widget the position
		is relative to the parent widget"""
		self.topleft = (x, y)
		
	def centerH(self, screen):
		w = screen.get_width()
		self.w = w-40
		self.x = 20
		
	# hover
	def hover(self, x, y):
		return self.collidepoint((x, y))
	
	# surface
	def makeSurface(self):
		"""Creates the widget surface"""
		self.surface = pygame.Surface((self.width, self.height))
		return self.surface
	
	# blit	
	def blit(self, screen):
		"""Blits the widget to the "screen" surface"""
		self._blitfunction(screen)
		for child in self._children:
			child.blit(self.surface)
		
	def doblit(self, screen):
		screen.blit(self.surface, self)
		
	def donothing(self, *args):
		pass
		
	def show(self, visibility=True):
		"""Shows or hide the widget"""
		if visibility:
			self._blitfunction = self.doblit
		else:
			self._blitfunction = self.donothing
		for child in self._children:
			child.show(visibility)
		
	def hide(self):
		self.show(False)
		
	def is_visible(self):
		return self._blitfunction == self.doblit
	
	def __repr__(self):
		return "<%s %x>" % (self.__class__.__name__, id(self))
		
	def __str__(self):
		return repr(self)
