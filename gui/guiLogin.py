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
from guiButton import ShowFrameButton, TextButton

class LoginGUI(Widget):
	def __init__(self, game):
		self.game = game
		self.screen = self.game.screen
		
		screen_w = self.screen.get_width()
		screen_h = self.screen.get_height()
		self.x = 220
		self.y = 180
		self.step1 = 140
		self.step2 = 40
		
		self.title = renderText("LOGIN", FONT_MANGA, True)
		
		self.loginLabel = Label("  Name  ", FONT, width=100)
		self.loginLabel.setPos(self.x,self.y)
		
		self.loginEntry = TextEntry("", width = 180)
		self.loginEntry.setPos(self.x + self.step1 ,self.y)
		self.loginEntry.getFocus()
		
		
		self.passwordLabel = Label("  Password  ", FONT, width=100)
		self.passwordLabel.setPos(self.x,self.y + 2*self.step2)
		
		self.passwordEntry = TextEntry("", width = 180)
		self.passwordEntry.setPos(self.x + self.step1, self.y +  + 2*self.step2)
		
		self.infoLabel = Label("Info", width = screen_w-40)
		#self.infoLabel.setPos(self.x,self.y + 5*self.step1)
		self.infoLabel.setPos(20,screen_h *0.9)
		
		self.loginButton = TextButton(text='  LOG IN  ')
		#self.loginButton.setPos(0, self.y + 4*self.step2)
		self.loginButton.setPos(screen_w*0.5, screen_h*0.8)
		#self.loginButton.centerH(self.screen)
		self.loginButton.bind(self.sendLoginRequest)
		
		self.registerButton = TextButton(text='  REGISTER  ')
		self.registerButton.setPos(screen_w*0.75, screen_h*0.8)
		self.registerButton.bind(self.sendRegisterRequest)
		
	def blit(self):
		self.screen.blit(self.title, (50,50))
		self.infoLabel.blit(self.screen)
		self.loginLabel.blit(self.screen)
		self.passwordLabel.blit(self.screen)
		self.loginEntry.blit(self.screen)
		self.passwordEntry.blit(self.screen)
		self.loginButton.blit(self.screen)
		self.registerButton.blit(self.screen)
		
	def handleEvents(self, x, y, events=[]):
		if not events:
			return False
			
		self.loginEntry.handleEvents(events)
		self.passwordEntry.handleEvents(events)
		self.loginButton.handleEvents(events)
		self.registerButton.handleEvents(events)
		
		for event in events:
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_TAB:
					if self.loginEntry.has_focus:
						self.loginEntry.loseFocus()
						self.passwordEntry.getFocus()
					elif self.passwordEntry.has_focus:
						self.loginEntry.getFocus()
						self.passwordEntry.loseFocus()
						
				elif event.key == pygame.K_RETURN:
					if self.loginEntry.has_focus:
						self.loginEntry.loseFocus()
						self.passwordEntry.getFocus()
					elif self.passwordEntry.has_focus:
						self.loginEntry.getFocus()
						self.passwordEntry.loseFocus()
						
				
						
			if event.type == pygame.MOUSEBUTTONDOWN:
				if event.button == 1:
					if self.loginEntry.hover and not self.loginEntry.has_focus:
						self.loginEntry.getFocus()
						self.passwordEntry.loseFocus()
					elif self.passwordEntry.hover and not self.passwordEntry.has_focus:
						self.loginEntry.loseFocus()
						self.passwordEntry.getFocus()
						
		return False
		
	def sendLoginRequest(self):
		self.name = self.loginEntry.getText()
		self.password = self.passwordEntry.getText()
		print "Sending login request with name = %s, pass = %s" % (self.name, self.password)
		self.game.SendLogin(self.name, self.password)
		
	def sendRegisterRequest(self):
		self.name = self.loginEntry.getText()
		self.password = self.passwordEntry.getText()
		print "Sending register request with name = %s, pass = %s" % (self.name, self.password)
		self.game.SendRegister(self.name, self.password)
		
	def launch(self):
		self.running = True
		while self.running:
			self.update()
		
	def update(self):
		self.screen.fill((100,140,160))
		x, y = pygame.mouse.get_pos()
		#print "mouse at %s, %s" % (x, y)
		events = pygame.event.get()
		self.handleEvents(x, y, events)
		self.blit()
		pygame.display.flip()
			
if __name__=="__main__":
	pygame.init()
	screen = pygame.display.set_mode((640,480))
	l = LoginGUI()
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
