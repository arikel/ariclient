#!/usr/bin/python
# -*- coding: utf8 -*-

import pygame
from guiFunctions import *

#-----------------------------------------------------------------------
# Widget
#-----------------------------------------------------------------------
class Widget(pygame.Rect):
	_parent = None
	_children = []
	_hover = False
	# rect
	def initRect(self, x=0, y=0, width=10, height=10):
		#self.rect = pygame.Rect(x, y, width, height)
		pygame.Rect.__init__(self, x, y, width, height)

	# width
	def getWidth(self):
		return self.width		
	def setWidth(self, x):
		self.width = int(x)
	# height
	def getHeight(self):
		return self.height
	def setHeight(self, x):
		self.height = int(x)
	# pos
	def set_parent(self, _parent):
		self._parent = _parent
	def reparentTo(self, _parent):
		self.set_parent(_parent)
	def detach(self):
		self._parent = None
		
	def getPos(self):
		if self._parent:
			return (self.x-self._parent.x, self.y-self._parent.y)
		return self.topleft
		
	def setPos(self, x, y):
		if self._parent:
			self.topleft = (x+self._parent.x, y+self._parent.y)
		else:
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
		self.surface = pygame.Surface((self.width, self.height))
		return self.surface
	
	# blit	
	def blit(self, screen):
		screen.blit(self.surface, self)
