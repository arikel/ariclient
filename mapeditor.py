#!/usr/bin/python
# -*- coding: utf-8 -*-

# mapeditor.py

import pygame
import random

from config import *
from gameEngine import *
from mapDisplay import MapTileset, Map

import inspect, os.path

caller = inspect.stack()[-1]

if os.path.basename(caller[1]).lower() != 'wxmapeditor.py':
	SCREEN = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
else:
	SCREEN = None
	print 'Skipping display initialization'

class MapEditor(object):
	def __init__(self, screen = SCREEN):
		self.map = None
		self.currentTileCode = "wwww"
		self.dragging = False
		self.dragOriginX = 0
		self.dragOriginY = 0
		if screen:
			self.screen = screen
		else:
			self.screen = pygame.display.set_mode((800,600))
		self.currentLayer = "ground"
		
	def open(self, filename):
		self.load(filename)
		
	def load(self, filename):
		self.filename = filename
		self.map = Map(filename)
		
	def save(self, filename):
		if not self.map:return
		self.map.save(filename)
		
	def new(self, x, y):
		self.map = Map("new")
		self.map.setSize(x, y)
		
	def random(self):
		self.map.setSize(80, 60)
		#making the ocean
		for y in range(self.map.h):
			for x in range(self.map.w):
				self.drawTile(self.currentLayer, x, y)
		#each vulcan generates a small island
		vulcans = random.randint(10,30)
		for n in range(vulcans):
			x, y = random.randint(0, self.map.w-1), random.randint(0, self.map.h-1)
			radious = random.randint(0,10)
			self.randomIsland(x, y, radious)
		
	def randomIsland(self, x, y, radious):
		try:
			#tree pruning
			if radious < 1 or self.map.layers["ground"].getTile(x, y) == "gggg":
				return
		except:
			#skipping positions outside the map
			return
		self.drawGrass(self.currentLayer, x, y)
		self.randomIsland(x-1, y, radious-1)
		self.randomIsland(x-1, y-1, radious-1)
		self.randomIsland(x-1, y+1, radious-1)
		self.randomIsland(x+1, y, radious-1)
		self.randomIsland(x+1, y-1, radious-1)
		self.randomIsland(x+1, y+1, radious-1)
		self.randomIsland(x, y-1, radious-1)
		self.randomIsland(x, y+1, radious-1)
		
	def setSize(self, x, y):
		if not self.map:return
		self.map.setSize(x, y)
	
	def getMouseTilePos(self, x, y):
		tx = (x+self.map.offsetX)/self.map.tileWidth
		ty = (y+self.map.offsetY)/self.map.tileHeight
		return tx, ty
			
	def startDrag(self):
		if not self.map:return
		print "started to drag map"
		self.dragging = True
		x, y = pygame.mouse.get_pos()
		self.dragOriginX = self.map.offsetX + x
		self.dragOriginY = self.map.offsetY + y
		
		
	def stopDrag(self):
		print "stopped dragging"
		self.dragging = False
		
	def update(self, events = []):
		if not self.map:return
		x, y = pygame.mouse.get_pos()
		
		if self.dragging:
			self.map.setOffset(self.dragOriginX-x, self.dragOriginY-y)
			
			#print "setting map offset : %s %s" % (self.map.offsetX, self.map.offsetY)
		tx, ty = self.getMouseTilePos(x, y)
		
		if pygame.mouse.get_pressed()[0]==1:
			self.drawTile(self.currentLayer, tx, ty)
		elif pygame.mouse.get_pressed()[2]==1:
			self.drawGrass(self.currentLayer, tx, ty)
		
		for event in events:
			if event.type == pygame.MOUSEBUTTONDOWN:
				if pygame.mouse.get_pressed()[1]==1 and not self.dragging:
					self.startDrag()
					
			elif event.type == pygame.MOUSEBUTTONUP:
				if self.dragging:
					self.stopDrag()
					
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
					self.toggleTileCode()
				elif event.key == pygame.K_s:
					self.save("maps/testmap2.txt")
				elif event.key == pygame.K_o:
					self.open("maps/testmap2.txt")
				elif event.key == pygame.K_r:
					self.setSize(40,20)
				elif event.key == pygame.K_g:
					self.random()
					
		#self.screen.fill((0,0,0))
		self.map.blit(self.screen)
		pygame.display.update()
		
	def blit(self, dest):
		self.map.blit(dest)
		
	def drawTile(self, layerName, x, y):
		if not self.map:return
		self.map.setTile(layerName, x, y, self.currentTileCode)
		self.map.needFullBlit = True
		
	def drawGrass(self, layerName, x, y):
		if not self.map:return
		self.map.setTile(layerName, x, y, "gggg")
		self.map.needFullBlit = True
		
	def setTileCode(self, code):
		self.currentTileCode = code
		
	def toggleTileCode(self):
		if self.currentTileCode == "wwww":
			self.setTileCode("dddd")
		elif self.currentTileCode == "dddd":
			self.setTileCode("rrrr")
		else:
			self.setTileCode("wwww")
			
			
	
	
if __name__ == "__main__":
	from utils import KeyHandler
	kh = KeyHandler()
	m = MapEditor()
	m.open("maps/testmap2.txt")
	
	while kh.keyDict[pygame.K_ESCAPE]==0:
		events = kh.getEvents()
		m.update(events)

	
	
