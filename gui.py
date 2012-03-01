#!/usr/bin/python
# -*- coding: utf8 -*-

import pygame
import sys
import math
import re
import string

from config import *

from guiFunctions import *
from guiWidget import Widget
from guiScroll import *
from guiEntry import *
from guiEmote import *
from guiProgressBar import *
from guiLogin import LoginScreen

class ClientGUI(object):
	def __init__(self, game):
		self.game = game
		self.screen = self.game.screen
		
		self.loginScreen = LoginScreen()
		self.mode = "login"
		
		self.chatWindow = ScrollTextWindow(0,SCREEN_HEIGHT-120,SCREEN_WIDTH,100)
		self.entry = TextEntry("")
		self.entry.setPos(5,SCREEN_HEIGHT-20)
		self.emoteEngine = EmoteEngine(SCREEN_WIDTH-21,2)
		self.hpbar = HpBar(0,100)
		self.hpbar.setPos(2, 2)
		self.hpbar.setValue(1)

	def launchLogin(self):
		self.id = self.loginScreen.launch(self.screen)
		return self.id
		
	def handleEvents(self, events=[]):
		x, y = pygame.mouse.get_pos()
		for event in events:
			self.chatWindow.handleEvents(x,y,events)
			if event.type == pygame.KEYDOWN:
				key = event.key	
				if key == pygame.K_RETURN and not self.entry.has_focus:
					#print "Starting to type text..."
					self.entry.getFocus()
		res = self.entry.handleInput(events)
		if res:
			self.game.SendMessagePublic(res)
			self.entry.has_focus = False
		
		emote = self.emoteEngine.handleEvents(events)
		if emote > -1:
			self.game.SendEmote(emote)
			
	def blit(self):
		self.chatWindow.blit(self.screen)
		self.entry.blit(self.screen)
		
		self.emoteEngine.blit(self.screen)
		
		#hpbar test
		self.hpbar.add(1)
		self.hpbar.blit(self.screen)
		
if __name__=="__main__":
	
	pygame.init()
	screen = pygame.display.set_mode((640, 480))
	
