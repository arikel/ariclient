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
		self._padding = 0 ##fixed padding can be changed with the padding function 
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
		if x<1: x=1
		self.width = int(x)
		self.makeSurface()
		
	# height
	def getHeight(self):
		"""Returns the height of the widget"""
		return self.height
	def setHeight(self, x):
		"""Sets the height of the widget"""
		if x<1: x=1
		self.height = int(x)
		self.makeSurface()
		
	def setPadding(self, padding):
		self._padding = padding
		
	def getPadding(self):
		return self._padding
		
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
		
	def __eq__(self, widget):
		if id(self) == id(widget):
			return True
		return False
		
	def add_child(self, child):
		if child not in self._children:
			self._children.append(child)
		'''
		# pygame.Rect.__eq__ override above
		else: #workaround to fix "the same kind of widget is in list" issue
			pos = self._children.index(child)
			if id(self._children[pos]) != id(child):
				self._children.append(child)
		'''
		
	def remove_child(self, child):
		if child in self._children:
			self._children.remove(child)
		
	# pos
	def getPos(self):
		"""Returns the widget position as a tuple (x, y)
		if the widget is a child of another widget the position
		is relative to the parent widget"""
		return self.topleft
		
	def setPos(self, x, y):
		"""Sets the widget position
		if the widget is a child of another widget the position
		is relative to the parent widget"""
		self.topleft = (x, y)
		#for child in self._children:
		#	child.dx = x
		#	child.dy = y
			
	def centerH(self, screen):
		w = screen.get_width()
		self.setPos(w/2 - self.w/2, self.y)
		
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
		#self.updateSurface()
		return self.surface
	
	def updateSurface(self):
		#if not hasattr(self, "surface"):
		#	return
		if not self.visible:
			return
		for child in self._children:
			child.updateSurface()
			child.blit(self.surface)
		
	def toggleVisible(self):
		if self.visible:
			self.hide()
		else:
			self.show()
		
	def show(self):
		self.visible = True
		for child in self._children:
			child.show()
			
	def hide(self):
		self.visible = False
		for child in self._children:
			child.hide()
			
	def blit(self, screen):
		if self.visible:
			screen.blit(self.surface, self)

	def __repr__(self):
		return "<%s %x @(%d, %d)>" % (self.__class__.__name__, id(self), self.x, self.y)
		
	def __str__(self):
		return repr(self)
