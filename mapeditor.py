#!/usr/bin/python
# -*- coding: utf-8 -*-

# mapeditor.py

import pygame
import random

from config import *
from gameEngine import *
from mapDisplay import MapTileset, Map

SCREEN = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

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
		
	def getMouseTilePos(self, x, y):
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
					self.save("testmap.txt")
				elif event.key == pygame.K_o:
					self.open("testmap.txt")
				elif event.key == pygame.K_r:
					self.setSize(40,20)
					
		self.screen.fill((0,0,0))
		self.map.blit(self.screen)
		pygame.display.update()
		
	def blit(self, dest):
		self.map.blit(dest)
		
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
	kh = KeyHandler()
	m = MapEditor()
	m.open("maps/testmap.txt")
	
	while kh.keyDict[pygame.K_ESCAPE]==0:
		events = kh.getEvents()
		m.update(events)

	
	
