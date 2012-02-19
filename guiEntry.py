#!/usr/bin/python
# -*- coding: utf8 -*-

import pygame
import sys
import math
import re
import string

from guiFunctions import *
from guiWidget import Widget
from guiScroll import *

#-----------------------------------------------------------------------
# Frame
#-----------------------------------------------------------------------		
class Frame(Widget):
	def __init__(self,
		width = 100,
		height = 20,
		bgcolor = (0,0,0),
		bordercolor = (200,200,200),
		hoverbordercolor = (255,255,255),
		borderwidth = 1):
		
		self.initRect(0, 0, width, height)
		self.makeSurface()
		
		self.setBGColor(bgcolor)
		self.setBorderColor(bordercolor)
		self.borderWidth = borderwidth
		
	
		
	def updateSurface(self):
		self.surface.fill(self.borderColor)
		pygame.draw.rect(self.surface,
			self.bgColor,
			(self.borderWidth, self.borderWidth,
			self.width-2*self.borderWidth, self.height-2*self.borderWidth))
		
	def setBGColor(self, color):
		self.bgColor = color
		
	def setBorderColor(self, color):
		self.borderColor = color
		
	def setBorderWidth(self, width):
		self.borderWidth = int(width)


#-----------------------------------------------------------------------
# Label
#-----------------------------------------------------------------------	
class Label(Frame):
	def __init__(self,
		text= "OK",
		font=FONT,
		width=0,
		height=0,
		bgcolor=(100,100,100),
		bordercolor=(255,255,255),
		hoverbordercolor=(255,255,255), 
		borderwidth = 1):
		Frame.__init__(self, width, height, bgcolor, bordercolor, hoverbordercolor, borderwidth = 1)
		
		self.baseText = text
		self.padding = 2
		self.font = font
		
		self.setText(self.baseText)
		
		
	def setText(self, msg):
		self.baseText = msg
		self.text = ustr(msg) #unicode(msg, "utf-8")
		self.msg = self.font.render(self.text, False, self.borderColor)
		self.msgRect = self.msg.get_rect()
		
		self.width = self.msgRect.width+self.padding*2
		self.height = self.msgRect.height+self.padding*2
		#self.msgRect.topleft = self.rect.topleft
		
		self.surface = self.makeSurface()
		self.updateSurface()
	
		
	def updateSurface(self):
		Frame.updateSurface(self)
		self.surface.blit(self.msg, (self.msgRect.left+self.padding,self.msgRect.top+self.padding,self.msgRect.width,self.msgRect.height))
		#self.surface.blit(self.msg, (0,0,self.msgRect.width,self.msgRect.height))

#-----------------------------------------------------------------------
# FixedLabel
#-----------------------------------------------------------------------
class FixedLabel(Frame):
	def __init__(self,
		text= "OK",
		font=FONT,
		width=0,
		height=0,
		bgcolor=(0,0,0),
		bordercolor=(255,255,255),
		hoverbordercolor=(255,255,255),
		borderwidth = 1):
		Frame.__init__(self, width, height, bgcolor, bordercolor, hoverbordercolor, borderwidth = 1)
		
		self.baseText = text
		self.padding = 5
		self.font = font
		
		self.setText(self.baseText)
		
	def setText(self, msg):
		self.baseText = msg
		self.text = unicode(msg, "utf-8")
		self.msg = self.font.render(self.text, False, self.borderColor)
		self.msgRect = self.msg.get_rect()		
		self.makeSurface()

	def updateSurface(self, x=0, y=0):
		Frame.updateSurface(self)
		self.surface.blit(self.msg, (self.msgRect.left+self.padding,self.msgRect.top+self.padding/2,self.msgRect.width,self.msgRect.height))


#-----------------------------------------------------------------------
# TextEntry
#-----------------------------------------------------------------------	
class TextEntry(Label):
	def __init__(self,
		text= "OK",
		font=FONT,
		width=0,
		height=0,
		bgcolor=(100,100,100),
		bordercolor=(255,255,255),
		hoverbordercolor=(255,255,255), 
		borderwidth = 1):
		Label.__init__(self, text, font, width, height, bgcolor, bordercolor, hoverbordercolor, borderwidth)
		self.has_focus = False
		self.shift = False
		
	def getFocus(self):
		self.has_focus = True
		
	def handleInput(self, events=None):
		'''
		for event in events:
			if event.type == pygame.KEYDOWN:
				key = event.key
				if key == pygame.K_RETURN and not self.has_focus:
					self.has_focus = True
					return None
		'''		
		if not self.has_focus or events==None:
			return None
		#print "entry handle input!"
		for event in events:
			if event.type == pygame.KEYDOWN:
				key = event.key
				if key == pygame.K_ESCAPE:
					self.baseText = ""
					self.setText(self.baseText)
					self.has_focus = False
					return None
				if key == pygame.K_BACKSPACE:
					self.baseText = self.baseText[0:-1]
				elif key == pygame.K_SPACE:
					self.baseText = self.baseText + " "
				elif key == pygame.K_MINUS:
					self.baseText = self.baseText + "_"
				elif 33<=key<=127:
					#if self.shift:
					#	toAdd = chr(key).upper()
					#else:
					#	toAdd = chr(key)
					toAdd = ustr(event.unicode)
					self.baseText = self.baseText + toAdd
					
				elif key == pygame.K_RETURN:
					res = self.baseText
					self.baseText = ""
					self.setText(self.baseText)
					#self.has_focus = False
					#print("Focus off")
					return res
				elif key == 303 or key == 304:
					self.shift = True
				else:
					print "Key %s was pressed, unicode = %s" % (key, event.unicode)
					toAdd = ustr(event.unicode)
					if len(toAdd.strip())>0:
						self.baseText = self.baseText + toAdd
				
				self.setText(self.baseText)
			
			if event.type == pygame.KEYUP:
				key = event.key
				if key == 303 or key == 304:
					self.shift = False
		return None





class LoginScreen(Widget):
	def __init__(self):
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
		self.loginLabel.blit(screen)
		self.passwordLabel.blit(screen)
		self.loginEntry.blit(screen)
		self.passwordEntry.blit(screen)
		
	def handleEvents(self, x, y, events=None):
		if not events:return
		res = self.loginEntry.handleInput(events)
		self.passwordEntry.handleInput(events)
		return res
		
	def launch(self, screen):
		self.running = True
		while self.running:
			screen.fill((100,120,160))
			x, y = pygame.mouse.get_pos()
			print "mouse at %s, %s" % (x, y)
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
