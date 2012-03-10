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
from guiButton import ShowFrameButton
from guiLogin import LoginScreen
from guiLayout import *

class ClientGUI(object):
	def __init__(self, game):
		self.game = game
		self.screen = self.game.screen
		
		self.loginScreen = LoginScreen()
		self.mode = "login"
		
		toplayout = BaseLayouter()
		barlayout = BaseLayouter(direction='vertical')
		self.chatWindow = ScrollTextWindow(0,SCREEN_HEIGHT-120,SCREEN_WIDTH,100)
		self.entry = TextEntry("")
		self.entry.setPos(5,SCREEN_HEIGHT-20)
		self.emoteEngine = EmoteEngine(SCREEN_WIDTH-21,2)
		
		self.menubutton = ShowFrameButton(text='Show:Hide',widget=self.chatWindow)

		self.hpbar = ProgressBar(0,100, image = ImgDB["graphics/gui/progressbars.png"].subsurface(0,0,96,6))
		self.hpbar.setValue(1)
		
		self.mpbar = ProgressBar(0,100, image = ImgDB["graphics/gui/progressbars.png"].subsurface(0,5,96,6))
		self.mpbar.setValue(100)
		
		toplayout.add(self.menubutton, 2)
		
		toplayout.add(barlayout, 2)
		barlayout.add(self.hpbar, 0)
		barlayout.add(self.mpbar, 0)
		toplayout.fit()
		barlayout.fit()
		

	def launchLogin(self):
		self.id = self.loginScreen.launch(self.screen)
		return self.id
		
	def handleEvents(self, events=[]):
		x, y = pygame.mouse.get_pos()
		self.chatWindow.handleEvents(x,y,events)
		
		for event in events:
			if event.type == pygame.KEYDOWN:
				key = event.key
				if key == pygame.K_RETURN:
					if self.entry.has_focus:
						if len(self.entry.baseText)>0:
							self.game.SendMessagePublic(self.entry.baseText)
							self.entry.setText("")
							self.entry.loseFocus()
						else:
							self.entry.loseFocus()
					else:
						self.entry.getFocus()
				self.chatWindow.updateSurface(x, y)
			
		res = self.entry.handleInput(events)
		if res:
			self.game.SendMessagePublic(res)
			self.entry.has_focus = False
		
		emote = self.emoteEngine.handleEvents(events)
		if emote > -1:
			self.game.SendEmote(emote)
			
		self.menubutton.handleEvents(events)
		
	def blit(self):
		self.chatWindow.blit(self.screen)
		self.entry.blit(self.screen)
		
		self.emoteEngine.blit(self.screen)
		
		#hpbar test
		self.hpbar.add(1)
		self.hpbar.blit(self.screen)

		self.mpbar.blit(self.screen)
		
		self.menubutton.blit(self.screen)

if __name__=="__main__":
	
	pygame.init()
	screen = pygame.display.set_mode((640, 480))
	
