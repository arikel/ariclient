#!/usr/bin/python
# -*- coding: utf8 -*-

import pygame
import sys
import math
import re
import string

from guiFunctions import *
from guiWidget import Widget
from guiFrame import Frame

class ColorPicker(Frame):
	
	def __init__(self,
		rotated = False,
		width = 218,
		height = 58,
		bgcolor = COLOR_BG,
		bordercolor = COLOR,
		hoverbordercolor = COLOR_HOVER,
		borderwidth = 1,
		parent = None):
		
		colors = [(0xfce94f, 0xedd400, 0xc4a000),\
				  (0xfcaf3e, 0xf57900, 0xce5c00),\
				  (0xe9b96e, 0xc17d11, 0x8f5902),\
				  (0x8ae234, 0x73d216, 0x4e9a06),\
				  (0x729fcf, 0x3465a4, 0x204a87),\
				  (0xad7fa8, 0x75507b, 0x5c3566),\
				  (0xef2929, 0xcc0000, 0xa40000),\
				  (0xeeeeec, 0xd3d7cf, 0xbabdb6),\
				  (0x888a85, 0x555753, 0x2e3436)]
			
		self.rotated = rotated
		if rotated == True:
			width, height = height, width
		Frame.__init__(self, width, height, bgcolor, bordercolor, hoverbordercolor, borderwidth, parent)
		
		self.setPalette(colors)
		
		
	def setPalette(self, colors):
		self.colorrects = []
		self.colors = colors
		if self.rotated == False:
			for y in range(len(colors)):
				for x in range(len(colors[y])):
					pygame.draw.rect(self.surface,
						colors[y][x],
						(y*20+4, x*20+4, 10, 10))
					pygame.draw.rect(self.surface,
						self.borderColor,
						(y*20+4, x*20+4, 10, 10), 1)
					self.colorrects.append(pygame.Rect(y*20+4, x*20+4, 10, 10))
			self.pickedcolorarea = (y*20+24, 14, 30, 30)
		else:
			for y in range(len(colors)):
				for x in range(len(colors[y])):
					pygame.draw.rect(self.surface,
						colors[y][x],
						(x*20+4, y*20+4, 10, 10))
					pygame.draw.rect(self.surface,
						self.borderColor,
						(x*20+4, y*20+4, 10, 10), 1)
					self.colorrects.append(pygame.Rect(x*20+4, y*20+4, 10, 10))
			self.pickedcolorarea = (14, y*20+24, 30, 30)
		pygame.draw.rect(self.surface,
					colors[0][0],
					self.pickedcolorarea)
		pygame.draw.rect(self.surface,
					self.borderColor,
					self.pickedcolorarea, 1)
					
		self.color = colors[0][0]
					
	def getActiveColor(self):
		return self.color
	
	def handleEvents(self, events=[]):
		for event in filter(lambda x: x.type == pygame.MOUSEBUTTONDOWN and x.button == 1 and self.hover, events):
			x, y = ((event.pos[0]-self.x)-self.dx-4)/10, ((event.pos[1]-self.y)-self.dy-4)/10
			#1x1 boundary
			if x%2 or y%2:
				return
			#getting the position in the matrix
			x, y = x/2, y/2
			if self.rotated:
				x, y = y, x
			try:
				self.color = self.colors[x][y]
				pygame.draw.rect(self.surface,\
								self.color,\
								self.pickedcolorarea)
				pygame.draw.rect(self.surface,\
								self.borderColor,\
								self.pickedcolorarea, 1)
			except IndexError:
				#x or/and y is/are outside the colors area
				#there's a very low probability to reach this point
				pass
				
				
