#!/usr/bin/python
# -*- coding: utf8 -*-

from guiFunctions import *
from guiWidget import Widget

EmoteDic = {}
for i in range(8):
	x = i
	y = 0
	while(x>3):
		x = x-4
		y += 1
	EmoteDic[i] = ImgDB["graphics/gui/emotes.png"].subsurface((x*19,y*19,19,19))

class EmoteButton(Widget):
	def __init__(self, nb=0, x=0, y=0):
		self.initRect(x, y, 19,19)
		self.nb = nb
		self.surface = EmoteDic[self.nb]

class EmoteEngine(Widget):
	def __init__(self, x, y):
		self.initRect(x,y,19,19*6)
		self.open = False
		
		self.topButton = EmoteButton(0,x,y)
		self.buttons = []
		for i in range(6):
			b = EmoteButton(i, x, y+(i+1)*20)
			self.buttons.append(b)
			
		
	def handleEvents(self, events):
		x, y = pygame.mouse.get_pos()
		for event in events:
			if event.type == pygame.MOUSEBUTTONDOWN:
				if pygame.mouse.get_pressed()[0]==1:
					if self.open:
						for b in self.buttons:
							if b.hover(x, y):
								self.closeMenu()
								return b.nb
					if self.topButton.hover(x, y):
						if self.open:
							self.closeMenu()
						else:
							self.openMenu()
		return -1
		
	def closeMenu(self):
		self.open = False
		
	def openMenu(self):
		self.open = True
	
	def blit(self, screen):
		self.topButton.blit(screen)
		if self.open:
			for b in self.buttons:
				b.blit(screen)
		
