#!/usr/bin/python
# -*- coding: utf-8 -*-

# mapeditor.py

import pygame
import random
from gameEngine import *
from mapDisplay import MapTileset, Map

class MapEditor(object):
	def __init__(self):
		self.map = None
		self.currentTileCode = "wwww"
		self.dragging = False
		self.dragOriginX = 0
		self.dragOriginY = 0
		self.screen = pygame.display.set_mode((800,600))
		self.currentLayer = "ground"
		
	def open(self, filename):
		self.load(filename)
		
	def load(self, filename):
		self.filename = filename
		self.map = Map()
		self.map.load(filename)
		
	def save(self, filename):
		if not self.map:return
		self.map.save(filename)
		
	def new(self, x, y):
		self.map = Map()
		self.map.setSize(x, y)
		
	def getMouseTilePos(self):
		x, y = pygame.mouse.get_pos()
		tx = (x-self.map.offsetX)/self.map.tileWidth
		ty = (y-self.map.offsetY)/self.map.tileHeight
		return tx, ty
		
	def setSize(self, x, y):
		if not self.map:return
		self.map.setSize(x, y)
		
	def update(self, events = []):
		if not self.map:return
		x, y = pygame.mouse.get_pos()
		
		if self.dragging:
			self.map.setOffset(x - self.dragOriginX, y - self.dragOriginY)
			#print "setting map offset : %s %s" % (self.map.offsetX, self.map.offsetY)
		tx, ty = self.getMouseTilePos()
		
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
					self.save("testmap.txt")
				elif event.key == pygame.K_o:
					self.open("testmap.txt")
				elif event.key == pygame.K_r:
					self.setSize(40,20)
					
		self.screen.fill((0,0,0))
		self.map.blit(self.screen)
		pygame.display.update()
		
	def drawTile(self, layerName, x, y):
		if not self.map:return
		self.map.setTile(layerName, x, y, self.currentTileCode)
	
	def drawGrass(self, layerName, x, y):
		if not self.map:return
		self.map.setTile(layerName, x, y, "gggg")
		
	def setTileCode(self, code):
		self.currentTileCode = code
		
	def toggleTileCode(self):
		if self.currentTileCode == "wwww":
			self.setTileCode("dddd")
		else:
			self.setTileCode("wwww")
			
			
	def startDrag(self):
		if not self.map:return
		print "started to drag map"
		self.dragging = True
		x, y = pygame.mouse.get_pos()
		self.dragOriginX = x - self.map.offsetX
		self.dragOriginY = y - self.map.offsetY
		
	def stopDrag(self):
		print "stopped dragging"
		self.dragging = False
	
if __name__ == "__main__":
	from utils import KeyHandler
	screen = pygame.display.set_mode((640,480))
	kh = KeyHandler()
	m = MapEditor()
	m.new(80,60)
	#m.open("testmap.txt")
	
	while kh.keyDict[pygame.K_ESCAPE]==0:
		events = kh.getEvents()
		m.update(events)

	
	
