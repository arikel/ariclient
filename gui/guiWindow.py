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
from guiButton import TextButton


class Window(Frame):
	def __init__(self,
		name = "Window",
		width = 80,
		height = 60,
		bgcolor = COLOR_BG,
		bordercolor = COLOR,
		hoverbordercolor = COLOR_HOVER,
		borderwidth = 1,
		parent = None):
		
		Frame.__init__(self, width, height, bgcolor, bordercolor, hoverbordercolor, borderwidth, parent)
		
		self.frame = Frame(width, 24, COLOR_BG, bordercolor, hoverbordercolor, borderwidth, self)
		self.name = Label(name, bgcolor = COLOR_BG, borderwidth = 0, parent = self.frame)
		self.close_button = TextButton("x", parent=self.frame)
		self.name. setPos(self.frame.borderWidth+1, self.frame.borderWidth+1)
		#is it better hide a frame or close it (deletion of the object)? 
		self.close_button.bind(lambda x: x.hide, self)
		self.setWidth(width)
		
		self.click = False
		
		
	def setWidth(self, x):
		"""Sets the width of the window"""
		self.frame.setWidth(x)
		self.close_button.setPos(x - self.close_button.getWidth()-2, self.frame.borderWidth +1)
		self.width = int(x)
		
	def OnDrag(self, x, y):
		self.setPos(self.x + x, self.y + y)	
		
		
	def handleEvents(self, events=[]):
		if not events:
			return False
		
		for event in events:
			if event.type == pygame.MOUSEBUTTONDOWN:
					if event.button == 1 and self.hover:
						self.click = True
						
			if event.type == pygame.MOUSEBUTTONUP:
				if self.click and self.hover:
					self.click = False
					#self.OnClick()
					
			if event.type == pygame.MOUSEMOTION:
				if self.click:
					self.OnDrag(*event.rel)
				
			
		#for child in self._children:
		#	if hasattr(child, 'handleEvents'):
		#		child.handleEvents(events)
