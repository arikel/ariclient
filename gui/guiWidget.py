#!/usr/bin/python
# -*- coding: utf8 -*-

import pygame
from guiFunctions import *

#-----------------------------------------------------------------------
# Widget
#-----------------------------------------------------------------------
class Widget(pygame.Rect):
	"""Main class used to define all the GUI components"""
	
	def __init__(self, x=0, y=0, width=10, height=10, parent=None):
		#self.rect = pygame.Rect(x, y, width, height)
		pygame.Rect.__init__(self, x, y, width, height)
		self.visible = True
		self.func = None
		self.params = None
		self._parent = None
		self.set_parent(parent)
		self._children = []
		self.setPos(x,y)
		

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
	
	# parent / children
	def set_parent(self, _parent):
		"""Sets the parent widget"""
		if self._parent:
			self._parent.remove_child(self)
		self._parent = _parent
		if self._parent:
			self.dx = self._parent.x
			self.dy = self._parent.y
			self._parent.add_child(self)
		else:
			self.dx = 0
			self.dy = 0
			
	def detach(self):
		"""Detatch the widget from its parent"""
		if self._parent:
			self._parent.remove_child(self)
			self._parent = None	
	def reparentTo(self, _parent):
		"""Changes the parent of the widget"""
		self.set_parent(_parent)
		
	def add_child(self, child):
		if child not in self._children:
			self._children.append(child)
		#self._children.append(child)
		
	def remove_child(self, child):
		if child in self._children:
			self._children.remove(child)
		
	# pos
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
		for child in self._children:
			child.dx = x
			child.dy = y
			
	def centerH(self, screen):
		w = screen.get_width()
		self.w = w-40
		self.x = 20
		
	# hover
	def is_hover(self):
		x, y = pygame.mouse.get_pos()
		dx, dy = 0, 0
		if self._parent:
			dx, dy = self._parent.x, self._parent.y
		if self.collidepoint((x-dx, y-dy)):
			#print "Collision found"
			return True
		#print "no collision : %s, %s not in %s, %s, %s, %s" % (x-dx, y-dy, self.x, self.y, self.w, self.h)
		return False
	
	hover = property(is_hover)
	
	# surface
	def makeSurface(self):
		"""Creates the widget surface"""
		self.surface = pygame.Surface((self.width, self.height))
		return self.surface
	
	def updateSurface(self):
		#if not hasattr(self, "surface"):
		#	return
		for child in self._children:
			child.updateSurface()
			child.blit(self.surface)
			
	def show(self):
		self.visible = True
		for child in self._children:
			child.show()
			
	def hide(self):
		self.visible = False
		for child in self._children:
			child.hide()
			
	def blit(self, screen):
		if not self.visible:
			return
		#if not hasattr(self, "surface"):
		#	return
		self.updateSurface()
		screen.blit(self.surface, self)
		
	
	'''
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
	'''
	def __repr__(self):
		return "<%s %x>" % (self.__class__.__name__, id(self))
		
	def __str__(self):
		return repr(self)
