#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame
from gameEngine import *

#-------------------------------------------------------------------------------
class GraphicMap(MapBase):
	def __init__(self, screen, filename):
		self.screen = screen
		self.screenWidth = self.screen.get_width()
		self.screenHeight = self.screen.get_height()
		
		self.filename = filename
		self.mapData = TmxMapData()
		self.mapData.load(self.filename)
		#print "Parsing Map done"
		# map X Y
		self.width = self.mapData.width
		self.height = self.mapData.height
		
		# smallest tile dimensions
		self.tileWidth = self.mapData.tileWidth
		self.tileHeight = self.mapData.tileHeight
		
		
		self.offsetX = 0
		self.offsetY = 0
		
		self.tilesets = self.mapData.tilesets
		#print("Tileset retrieved")
		
		self.frames = {} # gid : img frame
		self.offsets = {} # gid : Y tile offset
		self.maxTileWidth = 0
		self.maxTileHeight = 0
		for t in self.tilesets:
			if t.tileWidth > self.maxTileWidth : self.maxTileWidth = t.tileWidth
			if t.tileHeight > self.maxTileHeight : self.maxTileHeight = t.tileHeight
			self.frames.update(t.frames)
			offset = t.tileHeight - self.tileHeight
			for nb in t.frames:
				self.offsets[nb] = offset
				#print "gid %s, offset %s" % (nb, offset)
		#del self.tilesets # all images are now in self.frames
		
		self.layerImageWidth = self.width * self.tileWidth
		self.layerImageHeight = self.height * self.tileHeight

		
		self.maxLayerImageOffsetX = self.layerImageWidth - self.screenWidth
		self.maxLayerImageOffsetY = self.layerImageHeight - self.screenHeight
		if self.maxLayerImageOffsetX<0 : self.maxLayerImageOffsetX = 0
		if self.maxLayerImageOffsetY<0 : self.maxLayerImageOffsetY = 0
		
		self.layers = {}
		self.layerList = self.mapData.getLayerNames()
		for layerName in self.layerList:
			layer = TileLayer(layerName,
				self.width,
				self.height,
				decode(self.mapData.getLayerData(layerName))
			)
			self.layers[str(layerName)] = layer
			
		
		
		self.makeLayerImages()
		
		self.dragOrigin = (0, 0)
		self.dragOriginOffset = (self.offsetX, self.offsetY)
		self.dragging = False
		
		self.players = {}
		
	def blitTile(self, layerName, x, y):
		gid = self.layers[layerName].tiles[x][y]
		if gid>0:
			#x, y = self.getTileMapCoord(x, y)
			screenX, screenY = self.getScreenXY(x*self.tileWidth, y*self.tileHeight)
			offset = self.offsets[gid]
			self.screen.blit(self.frames[gid], (screenX, screenY-offset))
		
	def makeLayerImage(self, layerName):
		if layerName not in self.layers:
			return None
		layerImage = pygame.Surface(
			(self.layerImageWidth, self.layerImageHeight),
			pygame.SRCALPHA,
			32).convert_alpha()
		for y in range(self.height):
			for x in range(self.width):
				gid = self.layers[layerName].tiles[x][y]
				if gid>0:
					screenX = self.tileWidth*x
					screenY = self.tileHeight*y
					offset = self.offsets[gid]
					layerImage.blit(self.frames[gid], (screenX, screenY-offset))
		return layerImage
		
	def makeLayerImages(self):
		self.layerImages = {}
		for layerName in self.layerList:
			self.layerImages[layerName] = self.makeLayerImage(layerName)
		
	def getScreenXY(self, x, y):
		screenX = x - self.offsetX
		screenY = y - self.offsetY
		return screenX, screenY
	
	def getTileMapCoord(self, X, Y):
		return X*self.tileWidth, Y*self.tileHeight
	
	def getMouseToTileMapCoord(self, x, y):
		pixMapX = x + self.offsetX
		pixMapY = y + self.offsetY
		mapX = pixMapX / self.tileWidth
		mapY = pixMapY / self.tileHeight
		return mapX, mapY
		
	def getTileMapCoordToScreen(self, X, Y):
		return X*self.tileWidth-self.offsetX, Y*self.tileWidth-self.offsetY
		
	def isOnScreen(self, x, y):
		sX, sY = self.getScreenXY(x, y)
		if ( (-self.frameWidth<=sX<=self.screenWidth+self.frameWidth) and (-self.frameHeight<=sY<=self.screenHeight+self.frameHeight) ):
			return True
		return False
	'''
	def updateTile(self, mapX, mapY, screen = None):
		if screen == None:
			screen = self.screen
		screenX, screenY = self.getScreenXY(mapX, mapY)
		for layerName in self.layerList:
			if (mapX, mapY) in self.layers[layerName].tiles:
				gid = self.layers[layerName].tiles[(mapX, mapY)]
				offset = self.offsets[gid]
				screen.blit(self.frames[gid], (screenX, screenY-offset))
	'''		
		
		
	def aff(self):
		print "Map (%s, %s) : tilesets = %s, layers = %s" % (self.width, self.height, self.tilesets, self.layers)
	
	def caleOffsets(self):
		self.offsetX = min(max(0,self.offsetX), self.maxLayerImageOffsetX)
		self.offsetY = min(max(0,self.offsetY), self.maxLayerImageOffsetY)
		
	def blitLayer(self, layerName):
		self.caleOffsets()
		if layerName in self.layerImages:
			width = self.layerImages[layerName].get_width()-self.offsetX
			height = self.layerImages[layerName].get_height() - self.offsetY
			if ((width < self.screenWidth) or (height < self.screenHeight) ):
				self.screen.blit(self.layerImages[layerName].subsurface((self.offsetX,self.offsetY,width,height)), (0,0))
				
			else:
				self.screen.blit(self.layerImages[layerName].subsurface((self.offsetX,self.offsetY,self.screenWidth,self.screenHeight)), (0,0))
	
	def blit(self):
		self.caleOffsets()
		for layerName in self.layerList:
			#print("Blitting layer %s" % (layerName))
			if layerName in self.layerImages and layerName != "collision":
				self.blitLayer(layerName)
		
	def blitSpritesAndFringe(self, spriteList):
		self.caleOffsets()
		
		startX = self.offsetX / self.tileWidth-1
		startY = self.offsetY / self.tileHeight-1
		nbCol = self.screenWidth / self.tileWidth + 2
		nbLin = self.screenHeight / self.tileHeight + 2
		
		spriteTileCoordDic = {}
		for sprite in spriteList:
			if (sprite.getTilePos()) not in spriteTileCoordDic:
				spriteTileCoordDic[sprite.getTilePos()] = [sprite]
				
			else:
				spriteTileCoordDic[sprite.getTilePos()].append(sprite)
		
		for y in range(nbLin):
			for x in range(nbCol):
				X = x+startX
				Y = y+startY
				if ((X<0) or (X>=self.width-1)):continue
				elif ((Y<0) or (Y>=self.height-1)):continue
				if self.layers["fringe"].tiles[X][Y]>0:
					self.blitTile("fringe", X, Y)
				if (X, Y) in spriteTileCoordDic:
					for sprite in spriteTileCoordDic[(X, Y)]:
						sprite.blit(self.screen)
						
	
	'''				
	def collideTile(self, X, Y):
		#if (X, Y) in self.layers["collision"].tiles:
		if self.layers['collision'].tiles[X][Y]>0:
			return True
		return False
	
	def collideMap(self, x, y):
		X, Y = x/self.tileWidth, y/self.tileHeight
		return self.collideTile(X, Y)
	'''
	
	def startDrag(self, x, y):
		self.dragging = True
		self.dragOrigin = (x, y)
		self.dragOriginOffset = (self.offsetX, self.offsetY)
		#print "Starting Drag!"
		
	def updateDrag(self, x, y):
		if not self.dragging:return
		self.offsetX = self.dragOriginOffset[0] - (x-self.dragOrigin[0])
		self.offsetY = self.dragOriginOffset[1] - (y-self.dragOrigin[1])
		
	def stopDrag(self):
		self.dragging = False
		#print "Stopping Drag!"
		
		

if __name__=="__main__":
	pygame.init()
	screen = pygame.display.set_mode((800,600))
	m = Map(screen, "maps/001-1.tmx")
	m.blit()
	pygame.display.update()
