#!/usr/bin/python
# -*- coding: utf8 -*-

import pygame
import sys
import math
import re
import string

from guiFunctions import *
from guiWidget import Widget

#-----------------------------------------------------------------------
# ScrollButton
#-----------------------------------------------------------------------	
class ScrollButton(Widget):
	def __init__(self, x=0, y=0, direction = "up"):
		self.initRect(x, y, 20,20)
		self.makeSurface()
		#print("making button, direction = %s" % (direction))
		self.img = ImgDB["graphics/gui/guibase.png"].subsurface((1,1,20,20)).convert_alpha()
		self.imgHover = ImgDB["graphics/gui/guibase.png"].subsurface((22,1,20,20)).convert_alpha()
		if direction == "down":
			self.img = pygame.transform.rotate(self.img, 180)
			self.imgHover = pygame.transform.rotate(self.imgHover, 180)
		elif direction == "left":
			self.img = pygame.transform.rotate(self.img, 90)
			self.imgHover = pygame.transform.rotate(self.imgHover, 90)
		elif direction == "right":
			self.img = pygame.transform.rotate(self.img, 270)
			self.imgHover = pygame.transform.rotate(self.imgHover, 270)
			
		self.surface.blit(self.img, (0,0,20,20))
		
	def updateSurface(self, x=0, y=0):#x, y = pygame.mouse.get_pos()
		
		if self.hover(x, y) and not self._hover:
			self._hover = True
			self.surface.blit(self.imgHover, (0,0,20,20))
			
		elif self._hover and not self.hover(x, y):
			self._hover = False
			self.surface.blit(self.img, (0,0,20,20))
			
		
		
#-----------------------------------------------------------------------
# VScrollBar
#-----------------------------------------------------------------------

class VScrollBar(Widget):
	def __init__(self, nbPos=1, x=0, y=0, w=20, h=90):
		self.initRect(x, y, w, h)
		self.makeSurface()
		
		self.currentPos = 0
		self.dragging = False
		self.setNbPos(nbPos)
		
	def setNbPos(self, nb):
		self.nbPos = int(nb)
		if self.nbPos <1:
			self.nbPos = 1
		self.maxPos = self.nbPos - 1
		self.updateCarret()
		#self.info()
		
	def updateCarret(self):
		# ascenseur
		self.carretSize = max( self.h/float(self.nbPos), MIN_CARRET_SIZE )
		#print("carretSize : %s" % (self.carretSize))
		
		self.delta = self.h - self.carretSize # nb of pixel positions available to the carret
		
		if self.maxPos>0:
			self.step = self.delta / float(self.maxPos)
		else:
			self.step = 0
		#print("step = %s" % (self.step))
		
		self.carretRect = pygame.Rect(self.x, self.y, self.w, self.carretSize)
		self.carretSurface = pygame.Surface((self.w, self.carretSize))
		
		self.carretPosMin = self.y 
		self.carretPosMax = self.y + self.h - self.carretSize
		
		
		#self.dragging = False
		
		self.checkCarretPos()
	
	
	def info(self):
		print("total h : %s, nbPos = %s, currentPos:%s, carretSize : %s, step : %s, minPos : %s, carretMaxPos : %s, carretPos:%s" % (self.h, self.nbPos, self.currentPos, self.carretSize, self.step, self.carretPosMin, self.carretPosMax, self.carretRect.y))
	
		
	def checkCarretPos(self):
		if self.currentPos > self.maxPos:
			self.currentPos = self.maxPos
		if self.currentPos < 0:
			self.currentPos = 0
		
		self.carretRect.y = self.y + self.currentPos*self.step
		#if self.carretRect.y > self.carretPosMax: self.carretRect.y = self.carretPosMax
		#if self.carretRect.y < self.carretPosMin: self.carretRect.y = self.carretPosMin
		
		#print("after check : pos = %s" % (self.carretRect.y))
		#self.info()
		
	def setCarretPos(self, n=0):
		self.currentPos = int(n)
		self.checkCarretPos()
	
	def moveCarretPos(self, n=0):
		self.currentPos += int(n)
		self.checkCarretPos()
	
	def carretHover(self, x, y):
		return self.carretRect.collidepoint(x, y)
	
		
	def startDrag(self, x, y):
		#print("started to drag")
		self.dragging = True
		self.dragOffset = float(self.carretRect.y - y)
		
	def drag(self, x, y):
		if not self.dragging:return
		self.carretRect.y = y + self.dragOffset
		
		self.updatePos()
		#self.currentPos = int(round(pos))
		
	def stopDrag(self):
		if not self.dragging: return
		self.dragging = False
		#self.setCarretPos(int( (self.carretMax-self.carretMin)/self.carretSize ) )
		#print("stopped dragging")
		self.updatePos()
		
	def updatePos(self):
		if self.carretRect.y > self.carretPosMax: self.carretRect.y = self.carretPosMax
		if self.carretRect.y < self.carretPosMin: self.carretRect.y = self.carretPosMin
		
		#pos = (self.carretRect.y - self.rect.y) / float(self.carretSize)
		#pos = (self.carretRect.y - self.carretPosMin) * self.nbPos / float(self.delta - self.carretSize/2.0)
		if self.delta <=0:
			return
		pos = (self.carretRect.y - self.carretPosMin) * self.nbPos / float(self.delta)
		#pos = (self.carretRect.y - self.carretPosMin) * self.nbPos / float(self.delta)
		#if pos - int(pos)>=0.5:
		#	pos = pos+0.5
		#self.currentPos = int(pos)
		self.currentPos = round(pos)
		self.checkCarretPos()
		#print("position found : %s -> %s" % (pos, self.currentPos))
		
		
	def updateSurface(self, x=0, y=0):
		
		self.drag(x, y)
		self.surface.fill(TEXTCOLOR)
		pygame.draw.rect(self.surface, BGCOLOR, (1,1,self.w-2, self.h-2))
		
		if self.carretHover(x, y):
			self.carretSurface.fill(TEXTCOLORHOVER)
		else:
			self.carretSurface.fill(TEXTCOLOR)
		
		self.surface.blit(self.carretSurface, (0, self.carretRect.y-self.y, self.carretRect.width, self.carretRect.height))
		
	def scrollToBottom(self):
		self.setCarretPos(self.maxPos)
		
	def scrollToTop(self):
		self.setCarretPos(0)
		
	def handleEvents(self, x, y, events = None):
		self.updateSurface(x, y)
		
		for event in events:
			if event.type == pygame.KEYDOWN:
				key = event.key
				if key == pygame.K_DOWN:
					self.setCarretPos(self.currentPos + 1)
					#self.info()
				if key == pygame.K_UP:
					self.setCarretPos(self.currentPos - 1)
					#self.info()
					
				
			if event.type == pygame.MOUSEBUTTONDOWN:
				if pygame.mouse.get_pressed() == (1, 0, 0):
					#print "Vertical scroll bar received click"
					
					if self.carretHover(x, y):
						#print "Vertical scroll starting drag!"
						self.startDrag(x, y)
						
					elif self.hover(x,y):
						if y > self.carretRect.bottom:
							self.setCarretPos(self.currentPos + 1)
						elif y < self.carretRect.y:
							self.setCarretPos(self.currentPos - 1)
				if event.button==4 and self.hover(x,y):# wheel up
					self.setCarretPos(self.currentPos - 1)
				elif event.button==5 and self.hover(x,y): # wheel down
					self.setCarretPos(self.currentPos + 1)
					
			if event.type == pygame.MOUSEBUTTONUP:
				#print "Stopping carret drag"
				self.stopDrag()


class VScrollBar_buttons(Widget):
	def __init__(self, x, y, h, nbPos=2):
		w = 20
		self.initRect(x, y, w, h)
		self.makeSurface()
		self.currentPos = 0
		self.nbPos=int(nbPos)
		self.posMax = self.nbPos-1
		
		self.buttonUp = ScrollButton(self.x, self.y, "up")
		self.buttonDown = ScrollButton(self.x, self.y+self.h - 20, "down")
		
		self.bar = VScrollBar(self.nbPos, self.x, self.y+20, self.w, self.h-40)
		#print(Vscrollbuttons init : %s %s %s %s" % (x,y,w,h))
		
	def updateSurface(self, x, y):
		self.buttonUp.updateSurface(x,y)
		self.buttonDown.updateSurface(x,y)
		self.surface.blit(self.buttonUp.surface, (0,0,20,20))
		self.surface.blit(self.buttonDown.surface, (0,self.h-20,20,20))
		
		self.bar.updateSurface(x,y)
		self.surface.blit(self.bar.surface, (0,20))
		
	def handleEvents(self, x, y, events = None):
		self.bar.handleEvents(x, y, events)
		for event in events:
			if event.type == pygame.MOUSEBUTTONDOWN:
				if pygame.mouse.get_pressed() == (1, 0, 0):
					if self.buttonUp.hover(x,y):
						#print("click on button up")
						self.bar.setCarretPos(self.bar.currentPos-1)
					elif self.buttonDown.hover(x,y):
						#print("click on button down")
						self.bar.setCarretPos(self.bar.currentPos+1)

class ScrollTextWindow(Widget):
	def __init__(self, x, y, w, h):
		self.initRect(x,y,w,h)
		self.makeSurface()
		
		self.bar = VScrollBar_buttons(x+w-20, y, h, nbPos = 2)
		self.currentPos = 0
		
		self.padding = 5
		self.lineStep = 14
		
		self.nbVisibleLines = self.h /self.lineStep
		#print("%s visible lines" % (self.nbVisibleLines))
		
		self.baseText = ""
		self.setText("Welcome.\n")
		
	def updateSurface(self, x, y):
		self.surface.fill(BGCOLOR)
		self.bar.updateSurface(x,y)
		self.surface.blit(self.bar.surface, (self.w-20,0))
		self.surface.blit(self.textSurface.subsurface((0, self.currentPos*self.lineStep,self.textSurface.get_width(), self.textSurface.get_height()-(self.currentPos*self.lineStep))), (self.padding,0))
		
		
	def handleEvents(self, x, y, events = None):
		self.bar.handleEvents(x,y,events)
		if self.currentPos != self.bar.bar.currentPos:
			self.currentPos = self.bar.bar.currentPos
			self.makeTextSurface()
		
	def setNbPos(self, nb):
		self.bar.bar.setNbPos(nb)
		self.currentPos = self.bar.bar.currentPos
		self.nbPos = self.bar.bar.nbPos
		self.maxPos = self.bar.bar.maxPos
		
	def setCarretPos(self, n):
		self.bar.bar.setCarretPos(n)
		
	def setText(self, text):
		self.baseText = ustr(text)
		self.trimText()
		self.makeTextSurface()
		
		
	def trimText(self):
		#print "trimming, len = %s" % (len(self.baseText))
		while len(self.baseText)> 5000:
			self.baseText = self.baseText[1:]
		
	def addText(self, text):
		self.baseText = self.baseText + ustr(text) + "\n"
		self.trimText()
		self.makeTextSurface()
		self.setCarretPos(self.maxPos)
		
	def makeTextSurface(self):
		
		#lines = coupeMsg(self.baseText, self.getWidth()-2*self.padding-15, self.font)
		#self.nbLines = len(lines)
		lines = []
		self.nbLines = 0
		for line in self.baseText.split("\n"):
			toAdd = coupeMsg(line, self.w-2*self.padding-20, FONT)
			lines.extend(toAdd)
			self.nbLines += len(toAdd)
		
		self.textSurface = pygame.Surface((self.w-2*self.padding-15, (len(lines)+1)*self.lineStep))
		self.textSurface.fill((110,100,100))
		
		n = 0
		for line in lines:
			#print("Adding line : %s" % (line))
			#gline = unicode(line, "utf-8")
			#(w, h) = FONT.size(gline)
			#msg = FONT.render(gline, False, TEXTCOLOR)
			(w, h) = FONT.size(line)
			msg = FONT.render(line, False, TEXTCOLOR)
			self.textSurface.blit(msg, (0,n*self.lineStep, w, h))
			n += 1
		
		#self.surface.fill(BGCOLOR)
		#self.surface.blit(self.textSurface, (self.padding,self.padding, self.textSurface.get_rect().w, self.textSurface.get_rect().h))
		#print("setting nbPos : %s" % (self.nbLines - self.nbVisibleLines))
		self.setNbPos(self.nbLines - self.nbVisibleLines)
		#print("NbLines : %s , - %s visible = %s positions" % (self.nbLines, self.nbVisibleLines, self.nbPos))
		x, y = pygame.mouse.get_pos()
		self.updateSurface(x,y)
		#self.surface.blit(self.textSurface.subsurface((0, self.currentPos*self.lineStep,self.textSurface.get_width(), self.textSurface.get_height()-(self.currentPos*self.lineStep))), (self.padding,0))
	
