#!/usr/bin/python
# -*- coding: utf8 -*-

import pygame
import sys
import math
import re
import string

from guiFunctions import *
from guiWidget import Widget
from guiLabel import Label
from guiEntry import TextEntry
from guiButton import ShowFrameButton

class LoginScreen(Widget):
	def __init__(self):
		self.x = 220
		self.y = 180
		self.step1 = 120
		self.step2 = 60
		
		self.loginLabel = Label("Name", FONT2, width=100)
		self.loginLabel.setPos(self.x,self.y)
		
		self.loginEntry = TextEntry("")
		self.loginEntry.setPos(self.x + self.step1 ,self.y)
		self.loginEntry.getFocus()
		
		
		self.passwordLabel = Label("Password", FONT2, width=100)
		self.passwordLabel.setPos(self.x,self.y +  + 2*self.step2)
		
		self.passwordEntry = TextEntry("")
		self.passwordEntry.setPos(self.x + self.step1, self.y +  + 2*self.step2)
		
		self.infoLabel = Label("Info")
		self.infoLabel.setPos(self.x,self.y + 5*self.step1)
		
		self.loginButton = ShowFrameButton(text='LOG IN:Login')
		
	def blit(self, screen):
		self.infoLabel.blit(screen)
		self.loginLabel.blit(screen)
		self.passwordLabel.blit(screen)
		self.loginEntry.blit(screen)
		self.passwordEntry.blit(screen)
		self.loginButton.blit(screen)
		
	def handleEvents(self, x, y, events=None):
		if not events:return False
		res = self.loginEntry.handleInput(events)
		self.passwordEntry.handleInput(events)
		return res
		
	def launch(self, screen):
		self.running = True
		while self.running:
			screen.fill((100,140,160))
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
