#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame
from gameEngine import *
from sprite import BaseSprite, makePlayerSprite, makeMobSprite

#-------------------------------------------------------------------------------
class GraphicMap(MapBase):
	def __init__(self, screen, filename):
		MapBase.__init__(self, filename)
		self.screen = screen
		self.screenWidth = self.screen.get_width()
		self.screenHeight = self.screen.get_height()
		
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
		self.mobs = {}
		
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
		
class MapTileset(object):
	def __init__(self, filePath):
		self.filePath = filePath
		self.tiles = {} # tile code to surfaces list
		
		content = open(self.filePath).read()
		for line in content.split("\n"):
			if not "=" in line:continue
			if "#" in line: continue # comment
			items = line.split("=")
			if len(items)!=2:continue
			
			if items[0].strip() == "imgPath":
				self.setImgPath(items[1].strip())
				
			elif items[0].strip() == "w":# tile width
				self.w = int(items[1])
			elif items[0].strip() == "h":# tile height
				self.h = int(items[1])
				
			elif len(items[0].split(",")) == 2:
				xy = items[0].split(",")
				x = int(xy[0])
				y = int(xy[1])
				code = items[1].strip()
				self.addTile(x, y, code)
		
		self.notFoundImg = pygame.surface.Surface((self.w, self.h)).convert_alpha()
		self.notFoundImg.fill((180,40,40))
		
		self.emptyTile = pygame.surface.Surface((self.w, self.h)).convert_alpha()
		self.emptyTile.fill((0,0,0))
		self.emptyTile.set_alpha(0)
		
	def setImgPath(self, imgPath):
		self.imgPath = imgPath
		self.img = pygame.image.load(self.imgPath).convert_alpha()
		
	def addTile(self, x, y, code):
		if not code in self.tiles:
			self.tiles[code] = []
		self.tiles[code].append(self.img.subsurface((x*self.w, y*self.h, self.w, self.h)))
		
	def getTile(self, code):
		if not code in self.tiles:
			if code == 0:
				return self.emptyTile
			#print "couldn't find tile for code : %s, i only know %s" % (code, self.tiles.keys())
			return self.notFoundImg
		nb = len(self.tiles[code])
		tile = random.randint(1, nb) - 1
		return self.tiles[code][tile]

class Map(GameMap):
	def __init__(self, filename = None):
		self.filename = filename
		
		self.tileWidth = 16
		self.tileHeight = 16
		self.tileset = MapTileset("tilesets.txt")
		
		self.layers = {} # name : MapLayer
		self.layerImages = {} # name : (big) surface
		
		self.mobs = {} # id : Mob
		self.players = {} # id : Player
		self.sprites = {} # id : Sprite (for players and mobs)
		
		if filename:
			self.load(filename)
		
		
		#self.addLayer("ground")
		#self.layers["ground"].fill("gggg")
		self.updateLayerImage("ground")
		
		self.offsetX = 0
		self.offsetY = 0
		
		self.offsetXmax = 0
		self.offsetYmax = 0
		
	def addPlayer(self, id, x=50.0, y=50.0):
		if id not in self.players:
			self.players[id]=Player(id, self, x, y)
			self.players[id].setSprite(makePlayerSprite(id))
			#print "Map added player : %s, his map is : %s" % (id, self.players[id]._map)
			
	def delPlayer(self, playerName):
		del self.players[playerName]
		
		
	def addMob(self, id, mobId, x=50.0, y=50.0):
		if id not in self.mobs:
			self.mobs[id]=Mob(id, mobId, self, x, y)
			self.mobs[id].setSprite(makeMobSprite(id))
	
	def delMob(self, id):
		del self.mobs[id]
		
		
	def update(self, dt):
		for playerName in self.players:
			self.players[playerName].update(dt)
			
		for mobName in self.mobs:
			self.mobs[mobName].update(dt)
			
	def setOffset(self, x, y):
		self.offsetX = x
		self.offsetY = y
		
	def isValidPos(self, x, y):
		if (0<=x<self.w) and (0<=y<self.h):
			return True
		return False
		
	def setSize(self, x, y):
		for layerName in self.layers:
			self.w = x
			self.h = y
			self.layers[layerName].setSize(x, y)
			self.makeLayerImage(layerName)
		
	def load(self, filename):
		self.filename = filename
		content = open(filename).read()
		for line in content.split("\n"):
			line = line.strip()
			if len(line)<2:
				continue
			if "=" in line:
				if len(line.split("="))!=2: continue
				key , value = line.split("=")
				if key.strip() == "w":
					self.w = int(value.strip())
				elif key.strip() == "h":
					self.h = int(value.strip())
				else:
					codes = value.split(',')
					if len(codes) == self.w * self.h:
						layerName = key.strip()
						value = value.strip()
						print "Loading layer %s" % (layerName)
						self.addLayer(layerName)
						self.layers[layerName].setData(value)
						self.updateLayerImage(layerName)
		self.makeCollisionGrid()
						
	def addLayer(self, name):
		self.layers[name] = MapLayer(name, self.w, self.h, self.tileWidth, self.tileHeight)
		self.makeLayerImage(name)
		
	def makeLayerImage(self, name):
		if name not in self.layers:return
		print "map makes layer image for %s" % (name)
		self.layerImages[name] = pygame.surface.Surface((self.w*self.tileWidth, self.h * self.tileHeight))
		self.updateLayerImage(name)
		
	def updateLayerImage(self, name):
		self.layerImages[name].fill((150,150,150))
		for x in range(self.w):
			for y in range(self.h):
				code = self.layers[name].getTile(x, y)
				self.layerImages[name].blit(self.tileset.getTile(code), (x*self.tileWidth, y*self.tileHeight))
	
	def blit(self, screen):
		screen.blit(self.layerImages["ground"], (-self.offsetX,-self.offsetY))
		#print "Map offset : %s %s " % (self.offsetX, self.offsetY)
		sprites = [p._sprite for p in self.players.values()]
		sprites.extend([p._sprite for p in self.mobs.values()])
		
		for sprite in sorted(sprites, key = lambda k:k.mapRect.y):
			sprite.blit(screen)
		
	def clearTile(self, layerName, x, y):
		self.layers[layerName].clearTile(x, y)
		self.layerImages[layerName].blit(self.tileset.emptyTile, (x*self.tileWidth, y*self.tileHeight))
		self.updateLayerImage(layerName)
		
	def setTile(self, layerName, x, y, code):
		if not layerName in self.layers:return
		if not self.isValidPos(x, y):return
		if code == self.layers[layerName].getTile(x, y):return
		
		
		self.layers[layerName].setTile(x, y, code)
		self.layerImages[layerName].blit(self.tileset.getTile(code), (x*self.tileWidth, y*self.tileHeight))
		
		# check tile up left
		if self.isValidPos(x-1, y-1):
			oldCode = self.layers[layerName].getTile(x-1, y-1)
			newCode = oldCode[0:3] + code[0]
			self.layers[layerName].setTile(x-1, y-1, newCode)
			self.layerImages[layerName].blit(self.tileset.getTile(newCode), ((x-1)*self.tileWidth, (y-1)*self.tileHeight))
			
		# check tile up
		if self.isValidPos(x, y-1):
			oldCode = self.layers[layerName].getTile(x, y-1)
			newCode = oldCode[0:2] + code[0:2]
			self.layers[layerName].setTile(x, y-1, newCode)
			self.layerImages[layerName].blit(self.tileset.getTile(newCode), (x*self.tileWidth, (y-1)*self.tileHeight))
			
		# check tile up right
		if self.isValidPos(x+1, y-1):
			oldCode = self.layers[layerName].getTile(x+1, y-1)
			newCode = oldCode[0:2] + code[1] + oldCode[3]
			self.layers[layerName].setTile(x+1, y-1, newCode)
			self.layerImages[layerName].blit(self.tileset.getTile(newCode), ((x+1)*self.tileWidth, (y-1)*self.tileHeight))
		
		# check tile left
		if self.isValidPos(x-1, y):
			oldCode = self.layers[layerName].getTile(x-1, y)
			newCode = oldCode[0] + code[1] + oldCode[2] + code[3]
			self.layers[layerName].setTile(x-1, y, newCode)
			self.layerImages[layerName].blit(self.tileset.getTile(newCode), ((x-1)*self.tileWidth, y*self.tileHeight))
			
		# check tile right
		if self.isValidPos(x+1, y):
			oldCode = self.layers[layerName].getTile(x+1, y)
			newCode = code[0] + oldCode[1] + code[2] + oldCode[3]
			self.layers[layerName].setTile(x+1, y, newCode)
			self.layerImages[layerName].blit(self.tileset.getTile(newCode), ((x+1)*self.tileWidth, y*self.tileHeight))
			
		# check tile down left
		if self.isValidPos(x-1, y+1):
			oldCode = self.layers[layerName].getTile(x-1, y+1)
			newCode = oldCode[0] + code[2] + oldCode[2:4]
			self.layers[layerName].setTile(x-1, y+1, newCode)
			self.layerImages[layerName].blit(self.tileset.getTile(newCode), ((x-1)*self.tileWidth, (y+1)*self.tileHeight))
			
		# check tile down
		if self.isValidPos(x, y+1):
			oldCode = self.layers[layerName].getTile(x, y+1)
			newCode = code[0:2] + oldCode[2:4]
			self.layers[layerName].setTile(x, y+1, newCode)
			self.layerImages[layerName].blit(self.tileset.getTile(newCode), (x*self.tileWidth, (y+1)*self.tileHeight))
			
		# check tile down right
		if self.isValidPos(x+1, y+1):
			oldCode = self.layers[layerName].getTile(x+1, y+1)
			newCode = code[0] + oldCode[1:4]
			self.layers[layerName].setTile(x+1, y+1, newCode)
			self.layerImages[layerName].blit(self.tileset.getTile(newCode), ((x+1)*self.tileWidth, (y+1)*self.tileHeight))


if __name__=="__main__":
	pygame.init()
	screen = pygame.display.set_mode((800,600))
	m = Map(screen, "maps/001-1.tmx")
	m.blit()
	pygame.display.update()
