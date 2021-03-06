#!/usr/bin/python
# -*- coding: utf8 -*-

import pygame
import sys
import math
import re
import string

from guiFunctions import *
from guiFrame import Frame
from guiLabel import Label
from guiButton import TextButton, ImgButton

class Window(Frame):
	def __init__(self,
		name = "Window",
		width = 80,
		height = 60,
		bgcolor = COLOR_BG,
		bordercolor = COLOR,
		hoverbordercolor = COLOR_HOVER,
		borderwidth = 1,
		parent = None,
		gui = None):
		
		Frame.__init__(self, width, height, bgcolor, bordercolor, hoverbordercolor, borderwidth, parent)
		self.gui = gui
		
		self.name = Label(name, width = width-21, bgcolor = COLOR_BG, borderwidth = 1, parent = self)
		self.name.setPos(0, 0)
		
		self.close_button = ImgButton(self.w-20, 0, 20, 20,
			"graphics/gui/guibase.png", 1,49,1,70,
			parent=self)
		self.close_button.setPos(self.w-20, 0)
		self.close_button.bind(self.hide)
		
		self.drag_button = ImgButton(self.w-20, 0, 20, 20,
			"graphics/gui/guibase.png", 22,49,22,70,
			parent=self)
		self.drag_button.setPos(self.w-20, self.h-20)
		
		
		
		self.click = False
		self._resize = False
		
		
		
	def setSize(self, w, h):
		if w == self.width and h == self.height:
			return
		if w<40:w=40
		if h<40:h=40
		
		self.width = int(w)
		self.height = int(h)
		self.makeSurface()
		self.close_button.setPos(self.width - 21, 1)
		self.drag_button.setPos(self.w-21, self.h-21)
		self.name.setWidth(self.width-21)
		self.name.makeSurface()
		
	def OnDrag(self, x, y):
		self.gui.game.addDirtyRect(self.copy())
		self.setPos(self.x + x, self.y + y)
		self.updateSurface()
		
	def OnResize(self, x, y):
		self.gui.game.addDirtyRect(self.copy())
		self.setSize(self.w+x, self.h+y)
		self.updateSurface()
		
	def hide(self):
		if not self.visible:
			return
		# do not send the widget itself to the map, it would get modified
		self.gui.game.addDirtyRect(self.copy())
		
		self.visible = False
		for child in self._children:
			child.hide()
		
	def handleEvents(self, events=[]):
		if not events:
			return False
		if not self.visible:
			return
		for event in events:
			if event.type == pygame.MOUSEBUTTONDOWN:
					if event.button == 1 and self.hover:
						self.click = True
						
			if event.type == pygame.MOUSEBUTTONUP:
				if self.click and self.hover:
					self._resize = False
					self.click = False
					#self.OnClick()
					
			if event.type == pygame.MOUSEMOTION:
				if self.click:
					resize_rect = pygame.Rect(self.x + self.getWidth()-20, self.y + self.getHeight()-20, 20, 20)
					if self._resize:
						self.OnResize(*event.rel)
					elif resize_rect.collidepoint(*event.pos):
						self._resize = True
						self.OnResize(*event.rel)
					else:
						self.OnDrag(*event.rel)
				
				#self.name.updateSurface()
				#self.name.blit(self.surface)
				#self.close_button.blit(self.surface)
				#self.drag_button.blit(self.surface)
				self.updateSurface()
				
		for child in self._children:
			if hasattr(child, 'handleEvents'):
				child.handleEvents(events)
