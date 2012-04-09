#!/usr/bin/python
# -*- coding: utf8 -*-

import pygame
import sys
import math
import re
import string

from guiFunctions import *
from guiWidget import Widget
from guiEntry import TextEntry

#-----------------------------------------------------------------------
# ScrollButton
#-----------------------------------------------------------------------	
class ScrollButton(Widget):
	def __init__(self, x=0, y=0, direction = "up", parent=None):
		Widget.__init__(self, x, y, 20,20, parent)
		self.makeSurface()
		print("making button, direction = %s, parent = %s" % (direction, parent))
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
		
	def updateSurface(self):
		if self.hover:
			self.surface.blit(self.imgHover, (0,0,20,20))
			#print "scrollbutton over"
		else:
			self.surface.blit(self.img, (0,0,20,20))
	
#-----------------------------------------------------------------------
# VScrollBar
#-----------------------------------------------------------------------

class VScrollBar(Widget):
	def __init__(self, nbPos=1, x=0, y=0, w=20, h=90, parent=None):
		Widget.__init__(self, x, y, w, h, parent)
		print "init scrollbar : %s, %s, %s, %s" % (self.x, self.y, self.w, self.h)
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
		
		self.delta = self.h - self.carretSize # nb of pixel positions available to the carret
		
		if self.maxPos>0:
			self.step = self.delta / float(self.maxPos)
		else:
			self.step = 0
		
		self.carretRect = pygame.Rect(self.x, self.y, self.w, self.carretSize)
		self.carretSurface = pygame.Surface((self.w, self.carretSize))
		
		self.carretPosMin = self.y 
		self.carretPosMax = self.y + self.h - self.carretSize
		
		self.checkCarretPos()
	
	
	def info(self):
		print("total h : %s, nbPos = %s, currentPos:%s, carretSize : %s, step : %s, minPos : %s, carretMaxPos : %s, carretPos:%s" % (self.h, self.nbPos, self.currentPos, self.carretSize, self.step, self.carretPosMin, self.carretPosMax, self.carretRect.y))
	
		
	def checkCarretPos(self):
		if self.currentPos > self.maxPos:
			self.currentPos = self.maxPos
		if self.currentPos < 0:
			self.currentPos = 0
		self.carretRect.y = self.y + self.currentPos*self.step
		
	def setCarretPos(self, n=0):
		self.currentPos = int(n)
		self.checkCarretPos()
	
	def moveCarretPos(self, n=0):
		self.currentPos += int(n)
		self.checkCarretPos()
	
	def carretHover(self, x, y):
		return self.carretRect.collidepoint(x-self._parent.x, y-self._parent.y)
	
		
	def startDrag(self, x, y):
		#print("started to drag")
		self.dragging = True
		self.dragOffset = float(self.carretRect.y - y)
		
	def drag(self, x, y):
		if not self.dragging:return
		self.carretRect.y = y + self.dragOffset
		self.updatePos()
		
	def stopDrag(self):
		if not self.dragging: return
		self.dragging = False
		self.updatePos()
		
	def updatePos(self):
		if self.carretRect.y > self.carretPosMax: self.carretRect.y = self.carretPosMax
		if self.carretRect.y < self.carretPosMin: self.carretRect.y = self.carretPosMin
		
		if self.delta <=0:
			return
		pos = (self.carretRect.y - self.carretPosMin) * self.nbPos / float(self.delta)
		self.currentPos = round(pos)
		self.checkCarretPos()
		
		
	def updateSurface(self):
		x, y = pygame.mouse.get_pos()
		self.drag(x, y)
		self.surface.fill(TEXTCOLOR)
		pygame.draw.rect(self.surface, BGCOLOR, (1,1,self.w-2, self.h-2))
		
		if self.carretHover(x, y):
			self.carretSurface.fill(TEXTCOLORHOVER)
			#print "updating carret : HOVER"
		else:
			self.carretSurface.fill(TEXTCOLOR)
			#print "updating carret : not Hover"
		
		self.surface.blit(self.carretSurface, (0, self.carretRect.y-self.y, self.carretRect.width, self.carretRect.height))
		
	def scrollToBottom(self):
		self.setCarretPos(self.maxPos)
		
	def scrollToTop(self):
		self.setCarretPos(0)
		
	def handleEvents(self, events = []):
		if events:
			self.updateSurface()
			x, y = pygame.mouse.get_pos()
		
		for event in events:
			if event.type == pygame.MOUSEBUTTONDOWN:
				#if pygame.mouse.get_pressed() == (1, 0, 0):
				if event.button == 1:
					#print "Vertical scroll bar received click"
					
					if self.carretHover(x, y):
						#print "Vertical scroll starting drag!"
						self.startDrag(x, y)
						
					elif self.hover:
						if y-self._parent.y > self.carretRect.bottom:
							self.setCarretPos(self.currentPos + 1)
							
						elif y -self._parent.y < self.carretRect.y:
							self.setCarretPos(self.currentPos - 1)
							
							
				if event.button==4 and self.hover:# wheel up
					self.setCarretPos(self.currentPos - 1)
				elif event.button==5 and self.hover: # wheel down
					self.setCarretPos(self.currentPos + 1)
					
			if event.type == pygame.MOUSEBUTTONUP:
				#print "Stopping carret drag"
				self.stopDrag()


class VScrollBar_buttons(Widget):
	def __init__(self, x, y, h, nbPos=2, parent= None):
		w = 20
		Widget.__init__(self, x, y, w, h, parent)
		self.makeSurface()
		self.currentPos = 0
		self.nbPos=int(nbPos)
		self.posMax = self.nbPos-1
		
		self.buttonUp = ScrollButton(self.x, self.y, "up", parent)
		self.buttonDown = ScrollButton(self.x, self.y+self.h - 20, "down", parent)
		
		self.bar = VScrollBar(self.nbPos, self.x, self.y+20, self.w, self.h-40, parent)
		#print(Vscrollbuttons init : %s %s %s %s" % (x,y,w,h))
		
	def updateSurface(self):
		x, y = pygame.mouse.get_pos()
		
		self.buttonUp.updateSurface()
		self.buttonDown.updateSurface()
		self.surface.blit(self.buttonUp.surface, (0,0,20,20))
		self.surface.blit(self.buttonDown.surface, (0,self.h-20,20,20))
		
		self.bar.updateSurface()
		self.surface.blit(self.bar.surface, (0,20))
		
	def handleEvents(self, events = None):
		self.bar.handleEvents(events)
		for event in events:
			if event.type == pygame.MOUSEBUTTONDOWN:
				#if pygame.mouse.get_pressed() == (1, 0, 0):
				if event.button == 1:
					if self.buttonUp.hover:
						#print("click on button up")
						self.bar.setCarretPos(self.bar.currentPos-1)
						#print "button up!"
					elif self.buttonDown.hover:
						#print("click on button down")
						self.bar.setCarretPos(self.bar.currentPos+1)
						#print "button down!"
					else:
						#print "click missed buttons"
						x, y = pygame.mouse.get_pos()
						#print "target : %s %s, mouse : %s, %s" % (self.buttonUp.x - self.buttonUp.dx, self.buttonUp.y - self.buttonUp.dy, x, y)
			if event.type == pygame.MOUSEMOTION:
				self.updateSurface()

class ScrollTextWindow(Widget):
	def __init__(self, x, y, w, h, parent=None):
		Widget.__init__(self,x,y,w,h,parent)
		print "init scrolltextwindow : %s %s %s %s" % (self.x, self.y, self.w, self.h)
		self.makeSurface()
		
		self.bar = VScrollBar_buttons(x+w-20, y, h, 2, parent)
		self.currentPos = 0
		
		self.padding = 0
		self.lineStep = 14
		
		self.nbVisibleLines = self.h /self.lineStep
		#print("%s visible lines" % (self.nbVisibleLines))
		
		self.baseText = ""
		self.setText("Welcome.\n")
		
	def updateSurface(self):
		self.surface.fill(BGCOLOR)
		self.bar.updateSurface()
		self.surface.blit(self.bar.surface, (self.w-20,0))
		self.surface.blit(self.textSurface.subsurface((0, self.currentPos*self.lineStep,self.textSurface.get_width(), self.textSurface.get_height()-(self.currentPos*self.lineStep))), (self.padding,0))
		
		
	def handleEvents(self, events = None):
		self.bar.handleEvents(events)
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
		lines = []
		self.nbLines = 0
		for line in self.baseText.split("\n"):
			toAdd = coupeMsg(line, self.w-2*self.padding-20, FONT)
			lines.extend(toAdd)
			self.nbLines += len(toAdd)
		
		self.textSurface = pygame.Surface((self.w-2*self.padding-20, (len(lines)+1)*self.lineStep))
		self.textSurface.fill((110,100,100))
		
		n = 0
		for line in lines:
			(w, h) = FONT.size(line)
			msg = FONT.render(line, False, TEXTCOLOR)
			self.textSurface.blit(msg, (0,n*self.lineStep, w, h))
			n += 1
		
		self.setNbPos(self.nbLines - self.nbVisibleLines)
		self.updateSurface()
	
class ChatWindow(Widget):
	def __init__(self, x, y, w, h, parent=None, gui=None):
		Widget.__init__(self, x, y, w, h, parent)
		self.gui = gui
		self.makeSurface()
		self.entry = TextEntry("", width = w, parent=self)
		self.scrollTextWindow = ScrollTextWindow(0, 0, w, h-20, parent=self)
		
		print "created chatwindow, after init, w = %s, h = %s, x = %s, y = %s" % (self.w, self.h, self.x, self.y)
		self.entry.setPos(0, self.h-20)
		
	def addText(self, text):
		self.scrollTextWindow.addText(text)
		
	def getFocus(self):
		self.entry.getFocus()
		
	def loseFocus(self):
		self.entry.loseFocus()
		
	def handleEvents(self, events=[]):
		self.scrollTextWindow.handleEvents(events)
		self.entry.handleEvents(events)
		if events:
			self.updateSurface()
		
		
	def hide(self):
		if not self.visible:
			return
		# do not send the widget itself to the map, it would get modified
		self.gui.game.addDirtyRect(self.copy())
		
		self.visible = False
		for child in self._children:
			child.hide()
	
	def setPos(self, x, y):
		"""Sets the widget position
		if the widget is a child of another widget the position
		is relative to the parent widget"""
		self.topleft = (x, y)
		for child in self._children:
			child.dx = x
			child.dy = y
		
		
