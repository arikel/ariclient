#!/usr/bin/python
# -*- coding: utf8 -*-

import pygame
import sys
import math
import re
import string

from guiWidget import Widget
from guiLabel import Label
from guiEntry import TextEntry

class LoginScreen(Widget):
	def __init__(self):
		self.infoLabel = Label("Info")
		self.infoLabel.setPos(10,180)
		
		self.loginLabel = Label("LOGIN")
		self.loginLabel.setPos(10,20)
		self.passwordLabel = Label("PASSWORD")
		self.passwordLabel.setPos(10,100)
		self.loginEntry = TextEntry("")
		self.loginEntry.setPos(10,60)
		self.loginEntry.getFocus()
		self.passwordEntry = TextEntry("")
		self.passwordEntry.setPos(10,140)
		
	def blit(self, screen):
		self.infoLabel.blit(screen)
		self.loginLabel.blit(screen)
		self.passwordLabel.blit(screen)
		self.loginEntry.blit(screen)
		self.passwordEntry.blit(screen)
		
	def handleEvents(self, x, y, events=None):
		if not events:return False
		res = self.loginEntry.handleInput(events)
		self.passwordEntry.handleInput(events)
		return res
		
	def launch(self, screen):
		self.running = True
		while self.running:
			screen.fill((100,120,160))
			x, y = pygame.mouse.get_pos()
			#print "mouse at %s, %s" % (x, y)
			events = pygame.event.get()
			res = self.handleEvents(x, y, events)
			if res:
				self.running = False
			self.blit(screen)
			pygame.display.flip()
		return res
		
	
if __name__=="__main__":
	pygame.init()
	screen = pygame.display.set_mode((640,480))
	l = LoginScreen()
	l.loginEntry.getFocus()
	
	running = True
	while running:
		screen.fill((100,120,160))
		t = pygame.time.get_ticks()
		(x, y) = pygame.mouse.get_pos()
		events = pygame.event.get()
		l.handleEvents(x, y, events)
		
		for event in events:
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					running = False
		l.blit(screen)
		pygame.display.flip()
	print "Exited loop"
	pygame.quit()
