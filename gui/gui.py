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
from guiFrame import Frame
from guiScroll import *
from guiEntry import *
from guiEmote import *
from guiProgressBar import *
from guiButton import ShowFrameButton
from guiLogin import LoginGUI
from guiLayout import *
from guiConfig import *

class GameGUI(object):
	def __init__(self, game):
		self.game = game
		self.screen = self.game.screen
		
		guilayout = BaseLayouter('vertical')
		toplayout = BaseLayouter()
		
		separator = Widget(0,0,0,SCREEN_HEIGHT-140)
		print "Screen : %s %s" % (SCREEN_WIDTH, SCREEN_HEIGHT)
		print "creating chatwindow from clientGui : %s, %s, %s, %s" % (0,SCREEN_HEIGHT*4/5.0,SCREEN_WIDTH,SCREEN_HEIGHT/5.0)
		self.chatWindow = ChatWindow(0,SCREEN_HEIGHT*4/5.0,SCREEN_WIDTH,SCREEN_HEIGHT/5.0, gui=self)
		
		self.emoteEngine = EmoteEngine(SCREEN_WIDTH-21,2)
		
		self.configwindow = ConfigWindow(100,100, gui=self)
		
		self.menubutton = ShowFrameButton(text='Configuration:Configuration', widget = self.configwindow)
		self.chatbutton = ShowFrameButton(text='ChatWindow:ChatWindow', widget = self.chatWindow)
		
		self.BarFrame = Frame(SCREEN_WIDTH/2, 40)
		self.BarFrame.setPos(220, 2)
		
		
		self.hpbar = ProgressBar(0,100, width = 100, image = ImgDB["graphics/gui/progressbars.png"].subsurface(0,0,96,6), parent=self.BarFrame)
		self.hpbar.setValue(1)
		
		#somehow seems that this is not shown without the width set to framesize -1... weird thing to be checked ...
		self.mpbar = ProgressBar(0,100, width = 100, image = ImgDB["graphics/gui/progressbars.png"].subsurface(0,5,96,6), parent=self.BarFrame)
		self.mpbar.setValue(1)
		
		
		self.BarFrame.autolayout()
		
		guilayout.add(toplayout)
		guilayout.add(separator)
			
		toplayout.add(self.menubutton, 2)
		toplayout.add(self.chatbutton, 2)
		guilayout.fit()
		

	def handleEvents(self, events=[]):
		self.chatWindow.handleEvents(events)
		
		for event in events:
			if event.type == pygame.KEYDOWN:
				key = event.key
				if key == pygame.K_RETURN:
					if self.chatWindow.entry.has_focus:
						if len(self.chatWindow.entry.baseText)>0:
							self.game.SendMessagePublic(self.chatWindow.entry.baseText)
							self.chatWindow.entry.setText("")
							self.chatWindow.entry.loseFocus()
						else:
							self.chatWindow.entry.loseFocus()
					else:
						self.chatWindow.entry.getFocus()
				self.chatWindow.updateSurface()
			
		emote = self.emoteEngine.handleEvents(events)
		if emote > -1:
			self.game.SendEmote(emote)
			
		self.menubutton.handleEvents(events)
		self.chatbutton.handleEvents(events)
		self.configwindow.handleEvents(events)
		
	def blit(self):
		self.chatWindow.blit(self.screen)
		
		self.emoteEngine.blit(self.screen)
		
		#hpbar test
		self.hpbar.add(1)
		self.mpbar.add(1)
		self.BarFrame.updateSurface()
		self.BarFrame.blit(self.screen)
		#self.hpbar.blit(self.screen)

		#self.mpbar.blit(self.screen)
		
		self.menubutton.blit(self.screen)
		self.chatbutton.blit(self.screen)
		
		self.configwindow.blit(self.screen)

if __name__=="__main__":
	
	pygame.init()
	screen = pygame.display.set_mode((640, 480))
	
