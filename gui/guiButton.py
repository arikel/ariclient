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
from guiFrame import Frame

#-----------------------------------------------------------------------
# Button
#-----------------------------------------------------------------------	
class AbstractButton(Label):
	
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
		
		self.baseText = text
		self.padding = 2
		self.font = font
		
		self.click = False
		
		self.setText("  " + self.baseText + "  ")
		
	def OnClick(self):
		raise Exception('AbstractButton cannot be used directly, derivate it')
		
	def handleEvents(self, events):
		
		for event in events:
				
			if event.type == pygame.MOUSEBUTTONDOWN:
				if event.button == 1 and self.hover:
					self.click = True
					
			if event.type == pygame.MOUSEBUTTONUP:
				if self.click and self.hover:
					self.click = False
					self.OnClick()
					#print "AbstractButton OnClick"
					
					
class ShowFrameButton(AbstractButton):
	
	def __init__(self,
		text= "Menu",
		font=FONT,
		width=0,
		height=0,
		widget=Frame()):
		AbstractButton.__init__(self, text, font, width, height, (86,111,175), (200,200,200), (255,255,255), 1)
		self.widget = widget
		self._auxtext = text.split(':')
		#self.setText("  " +  self._auxtext[widget.is_visible()] + "  ")
		self.setText("  " +  self._auxtext[widget.visible] + "  ")
		
	def OnClick(self):
		#fshow = not self.widget.is_visible()
		#fshow = not self.widget.visible
		if not self.visible:
			return
		if self.widget.visible:
			self.widget.hide()
		else:
			self.widget.show()
		#self.widget.show(fshow)
		#self.setText("  " +  self._auxtext[fshow] + "  ")
		self.setText("  " +  self._auxtext[self.visible] + "  ")


class ButtonBase(Widget):
	def blit(self, screen):
		if self.hover:
			screen.blit(self.surfaceHover, self)
		else:
			screen.blit(self.surface, self)
		
	def bind(self, func, params=None):
		self.func = func
		self.params = params
		
	def OnClick(self):
		if self.func:
			if self.params:
				self.func(self.params)
			else:
				self.func()
		else:
			print "Error : no function bound for Button"
			
	def handleEvents(self, events):
		
		for event in events:
				
			if event.type == pygame.MOUSEBUTTONDOWN:
				if event.button == 1 and self.hover:
					self.click = True
					
			if event.type == pygame.MOUSEBUTTONUP:
				if self.click and self.hover:
					self.click = False
					self.OnClick()

class TextButton(ButtonBase):
	
	def __init__(self,
		text= "OK",
		font=FONT,
		width=0,
		height=0,
		color = COLOR,
		color_bg = COLOR_BG,
		color_hover = COLOR_HOVER,
		color_bg_hover = COLOR_BG_HOVER,
		borderwidth = 1,
		parent = None):
		
		Widget.__init__(self, 0, 0, width, height, parent)
		
		self.color = color
		self.color_bg = color_bg
		self.color_hover = color_hover
		self.color_bg_hover = color_bg_hover
		self.borderWidth = borderwidth
		
		self.baseText = text
		self.padding = 2
		self.font = font
		self.has_focus = False
		self.click = False
		
		self.setText("  " + self.baseText + "  ")
		self.makeSurface()
		
	def autolayout(self, direction='vertical', autoexpand = False):
		x, y = 0, 0
		for widget in self._children:
			padding = widget.getPadding()
			widget.setPos(x+padding, y+padding)
			
			if direction == 'horizontal':
				x += widget.getWidth() + 2 * padding
			elif direction == 'vertical':
				y += widget.getHeight() + 2 * padding
				
		if autoexpand:
			self.setWidth(x + widget.getWidth())
			self.setHeight(y + widget.getWidth())
			self.updateSurface()
			
	
		
	def setText(self, msg):
		self.baseText = msg
		self.text = ustr(msg) #unicode(msg, "utf-8")
		if self.has_focus:
			self.msg = self.font.render(self.text + "_", False, self.color)
			self.msgHover = self.font.render(self.text + "_", False, self.color_hover)
		else:
			self.msg = self.font.render(self.text, False, self.color)
			self.msgHover = self.font.render(self.text, False, self.color_hover)
			
		self.msgRect = self.msg.get_rect()
		if self.w < self.msgRect.width+self.padding*2:
			self.width = self.msgRect.width+self.padding*2
		if self.height < self.msgRect.height+self.padding*2:
			self.height = self.msgRect.height+self.padding*2
		
		self.makeSurface()
		self.updateSurface()
	
	
	def makeSurface(self):
		"""Creates the widget surface"""
		self.surface = pygame.Surface((self.width, self.height))
		self.surfaceHover = pygame.Surface((self.width, self.height))
		
		# surface
		self.surface.fill(self.color)
		pygame.draw.rect(self.surface,
			self.color_bg,
			(self.borderWidth, self.borderWidth,
			self.width-2*self.borderWidth, self.height-2*self.borderWidth))
		
		self.surface.blit(self.msg, (self.msgRect.left+self.padding,self.msgRect.top+self.padding,self.msgRect.width,self.msgRect.height))
		
		# surface hover
		self.surfaceHover.fill(self.color_hover)
		pygame.draw.rect(self.surfaceHover,
			self.color_bg_hover,
			(self.borderWidth, self.borderWidth,
			self.width-2*self.borderWidth, self.height-2*self.borderWidth))
		
		self.surfaceHover.blit(self.msgHover, (self.msgRect.left+self.padding,self.msgRect.top+self.padding,self.msgRect.width,self.msgRect.height))
		
		return self.surface
		
	
					
class ImgButton(ButtonBase):
	
	def __init__(self,
		x=0,
		y=0,
		width=0,
		height=0,
		imgPath= "OK",
		imgx=0,
		imgy=0,
		imghoverx=0,
		imghovery=0,
		parent = None):
		
		Widget.__init__(self, x, y, width, height, parent)
		
		self.has_focus = False
		self.click = False
		
		self.surface = ImgDB[imgPath].subsurface((imgx, imgy, self.w, self.h))
		self.surfaceHover = ImgDB[imgPath].subsurface((imghoverx, imghovery, self.w, self.h))
		
	
		
