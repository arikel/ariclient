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
		self.has_focus = True
		self.shift = False
		
	def getFocus(self):
		self.has_focus = True
		
	def handleInput(self, events=None):
		for event in events:
			if event.type == pygame.KEYDOWN:
				key = event.key
				if key == pygame.K_RETURN and not self.has_focus:
					self.has_focus = True
					return None
					
		if not self.has_focus or events==None:
			return None
			
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
					self.has_focus = False
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
#-----------------------------------------------------------------------
# TextScrollFrame
#-----------------------------------------------------------------------
class TextScrollFrame(Widget):
	def __init__(self, text, width=600, height=100, lineStep=16, padding = 10, font=FONT):
		self.lineScrollFactor = 1
		self.lineStep = lineStep
		self.padding = padding
		self.baseText = text + "\n"
		
		self.initRect(0, 0, width, height)
		self.makeSurface()
		self.font = font
		
		self.makeTextSurface()
		
		self.nbVisibleLines = int( (self.getHeight()-2*self.padding) / self.lineStep )
		self.nbPos = (self.nbLines - self.nbVisibleLines +1)*self.lineScrollFactor
		if self.nbPos <=1:
			self.nbPos = 1
		self.scrollBar = ScrollBar(self.nbPos, 0, 0, 15, self.getHeight())
		self.scrollBar.setPos(self.rect.right - 20, self.rect.top)
		
	def setCarretPos(self, n):
		self.surface.fill(BGCOLOR)
		self.surface.blit(self.textSurface, (self.padding,self.padding-n*self.lineStep/self.lineScrollFactor, self.textSurface.get_rect().w, self.textSurface.get_rect().h))
		
	def setPos(self, x, y):
		Widget.setPos(self, x, y)
		self.scrollBar.setPos(self.rect.right-15, self.rect.y)
		self.scrollBar.getCarretPixelRange()
		self.scrollBar.checkCarretPos()
		
	def makeTextSurface(self):
		
		#lines = coupeMsg(self.baseText, self.getWidth()-2*self.padding-15, self.font)
		#self.nbLines = len(lines)
		lines = []
		self.nbLines = 0
		for line in self.baseText.split("\n"):
			toAdd = coupeMsg(line, self.getWidth()-2*self.padding-15, self.font)
			lines.extend(toAdd)
			self.nbLines += len(toAdd)
		
		self.textSurface = pygame.Surface((self.getWidth()-2*self.padding-15, (len(lines)+1)*self.lineStep))
		n = 0
		for line in lines:
			#print "Adding line : %s" % (line)
			gline = unicode(line, "utf-8")
			(w, h) = self.font.size(gline)
			msg = self.font.render(gline, False, TEXTCOLOR)
			self.textSurface.blit(msg, (0,n*self.lineStep, w, h))
			n += 1
		self.surface.fill(BGCOLOR)
		self.surface.blit(self.textSurface, (self.padding,self.padding, self.textSurface.get_rect().w, self.textSurface.get_rect().h))
		
	def setText(self, txt):
		self.baseText = txt
		self.makeTextSurface()
		
	def addText(self, txt):
		self.baseText = self.baseText + txt + "\n"
		self.makeTextSurface()
		
	
		
	def updateSurface(self, x, y):
		self.setCarretPos(self.scrollBar.currentPos)
		self.scrollBar.updatePos()
		self.scrollBar.updateSurface(x, y)
		
	def blit(self, screen):
		screen.blit(self.surface, self.rect)
		self.scrollBar.blit(screen)
	



if __name__=="__main__":
	msg = """Je ne connaîtrai pas la peur, car la peur tue l'esprit. La peur
	est la petite mort qui conduit à l'oblitération totale.
	J'affronterai ma peur. Je la laisserai passer en moi, au travers de moi,
	et lorsqu'elle sera passée, je tournerai mon oeil intérieur sur son chemin,
	et là où elle sera passée, il n'y aura plus rien. Rien que moi."""
	pygame.init()
	screen = pygame.display.set_mode((640, 480))
	
