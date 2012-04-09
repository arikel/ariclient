#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame
from config import *
#from guiFunctions import ImgDB
from gui import *
from gameEngine import *
from sprite import BaseSprite, makePlayerSprite, makeMobSprite
from mapParticle import MapParticleManager

#-------------------------------------------------------------------------------
# MapTileset
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
		#self.emptyTile.fill((255,0,255))
		#self.emptyTile.set_colorkey((255,0,255))
		#self.emptyTile.set_alpha(100)
		
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

#-------------------------------------------------------------------------------
# Map
class Map(GameMap):
	def __init__(self, filename = None):
		self.filename = filename
		self.screenRect = pygame.Rect((0,0,SCREEN_WIDTH,SCREEN_HEIGHT))
		
		self.tileWidth = 16
		self.tileHeight = 16
		self.tileset = MapTileset("tilesets.txt")
		
		self.layers = {} # name : MapLayer
		self.layerImages = {} # name : (big) surface
		
		self.dirtyRects = []
		self.dirtySprites = []
		self.needFullBlit = True
		
		self.mobs = {} # name : Mob
		self.players = {} # name : Player
		self.sprites = {} # name : Sprite (for players and mobs)
		
		if filename:
			self.load(filename)
		
		
		#self.addLayer("ground")
		#self.layers["ground"].fill("gggg")
		self.updateLayerImage("ground")
		
		self.imgW = self.layerImages["ground"].get_width()
		self.imgH = self.layerImages["ground"].get_height()
		
		self.offsetX = 0
		self.offsetY = 0
		
		self.offsetXmax = 0
		self.offsetYmax = 0
		
		self.selected = None
		self.collisionVisible = False
		self.warpVisible = False
		self.warpImg = None
		
		self.warps = []
		
		self.particleManager = MapParticleManager(self)
		
		self.arrayblit = [self.dirtyBlit, self.fullBlit]
		
	def addWarp(self, name, x, y, w, h):
		for warp in self.warps:
			if warp.name == name:
				return
		self.warps.append(MapWarp(name, x, y, w, h))
		self.makeWarpImage()
		
	def selectTarget(self, name):
		self.selected = name
		self.selectCursor = ImgDB["graphics/gui/guibase.png"].subsurface((16,32,32,16)).convert_alpha()
		
	def unselectTarget(self):
		self.selected = None
		
	def addPlayer(self, name, x=50.0, y=50.0):
		if name not in self.players:
			self.players[name]=Player(name, self, x, y)
			self.players[name].setSprite(makePlayerSprite(name, self))
			self.players[name].setPos(x,y)
			self.players[name].setMovement(0,0)
			self.players[name].update()
		else:
			pass
			#print("Error, asked to add player %s, but that one is already here." % (name))
			
	def delPlayer(self, playerName):
		if playerName in self.players:
			self.addDirtyRect(self.players[playerName]._sprite.getDirtyRect())
			del self.players[playerName]
		
		
	def addMob(self, name, mobId, x=50.0, y=50.0):
		if name not in self.mobs:
			self.mobs[name]=Mob(name, mobId, self, x, y)
			self.mobs[name].setSprite(makeMobSprite(name, self))
			self.mobs[name].setPos(x,y)
			self.mobs[name].setMovement(0,0)
			self.mobs[name].update()
			
	def delMob(self, name):
		self.addDirtyRect(self.mobs[name]._sprite.getDirtyRect())
		del self.mobs[name]
		
	def update(self, dt):
		self.particleManager.update()
		
		for playerName in self.players:
			self.players[playerName].update(dt)
			
		for mobName in self.mobs:
			self.mobs[mobName].update(dt)
	
	def handleClick(self):
		#print "--- Map handle click ---"
		x, y = pygame.mouse.get_pos()
		for playerName in self.players:
			player = self.players[playerName]
			if player._sprite.rect.collidepoint(x, y):
				print "Player %s was clicked on" % (playerName)
				return
		for mobName in self.mobs:
			mob = self.mobs[mobName]
			if mob._sprite.rect.collidepoint(x, y):
				self.selectTarget(mobName)
				print "Monster %s was clicked on" % (mobName)
	
	def setOffset(self, x, y):
		if x != self.offsetX or y != self.offsetY:
			self.offsetX = x
			self.offsetY = y
			self.needFullBlit = True
			
		
		
	def isValidPos(self, x, y):
		if (0<=x<self.w) and (0<=y<self.h):
			return True
		return False
		
	def isMobOnScreen(self, mobName):
		if mobName not in self.mobs:
			return False
		if self.screenRect.colliderect(self.mobs[mobName]._sprite.rect):
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
				if key.strip() == "name":
					self.name = value.strip()
				elif key.strip() == "w":
					self.w = int(value.strip())
				elif key.strip() == "h":
					self.h = int(value.strip())
				else:
					codes = value.split(',')
					if len(codes) == self.w * self.h:
						layerName = key.strip()
						value = value.strip()
						#print "Loading layer %s" % (layerName)
						self.addLayer(layerName)
						self.layers[layerName].setData(value)
						self.updateLayerImage(layerName)
		self.makeCollisionGrid()
						
	def addLayer(self, name):
		self.layers[name] = MapLayer(name, self.w, self.h, self.tileWidth, self.tileHeight)
		self.makeLayerImage(name)
		
	def makeLayerImage(self, name):
		if name not in self.layers:return
		#print "map makes layer image for %s" % (name)
		self.layerImages[name] = pygame.surface.Surface((self.w*self.tileWidth, self.h * self.tileHeight))
		self.layerImages[name].convert_alpha()
		
		self.updateLayerImage(name)
		
	def updateLayerImage(self, name):
		self.layerImages[name].fill((255,0,255))
		self.layerImages[name].set_colorkey((255,0,255))
		
		for x in range(self.w):
			for y in range(self.h):
				code = self.layers[name].getTile(x, y)
				if code:
					self.layerImages[name].blit(self.tileset.getTile(code), (x*self.tileWidth, y*self.tileHeight))
	
	def makeWarpImage(self):
		self.warpImg = pygame.surface.Surface((self.w*self.tileWidth, self.h * self.tileHeight))
		self.warpImg.fill((255,0,255))
		self.warpImg.set_colorkey((255,0,255))
		
		for warp in self.warps:
			pygame.draw.rect(self.warpImg, (255,120,120), (warp.x, warp.y, warp.w, warp.h))
		self.warpImg.set_alpha(120)
		
	def addDirtyRect(self, rect):
		self.dirtyRects.append(rect)
		
	def blit(self, screen):
		self.arrayblit[self.needFullBlit](screen)
		
	def dirtyBlit(self, screen):
		for rect in self.dirtyRects:
			x = rect.x+self.offsetX
			y = rect.y+self.offsetY
			needFill = False
			baseRect = rect.copy()
				
			if x<0:
				rect.w = rect.w-abs(x)
				rect.x -= x
				x=0
				needFill = True
				
			if y<0:
				rect.h = rect.h-abs(y)
				rect.y -= y
				y = 0
				needFill = True
				
			if x+rect.w>self.imgW:
				rect.w = self.imgW - x
				needFill = True
				
			if y+rect.h>self.imgH:
				rect.h = self.imgH - y
				needFill = True
			
			if needFill:
				pygame.draw.rect(screen, (0,0,0), (baseRect.x,baseRect.y, baseRect.w, baseRect.h))
				
			img = self.layerImages["ground"].subsurface(x,y, rect.w, rect.h)
			screen.blit(img, (rect.x,rect.y))
			
				
		for sprite in sorted(self.dirtySprites, key = lambda k:k.mapRect.y):
			if self.selected:
				if sprite.name == self.selected:
					screen.blit(self.selectCursor, (sprite.rect.x-4, sprite.rect.y+24))
			sprite.blit(screen)
		
		self.particleManager.blit(screen)
		
		self.dirtyRects = []
		self.dirtySprites = []
		
	def fullBlit(self, screen):
		screen.fill((0,0,0))
		# ground
		screen.blit(self.layerImages["ground"], (-self.offsetX,-self.offsetY))
		#print "Map offset : %s %s " % (self.offsetX, self.offsetY)
		
		
		# collision
		#screen.blit(self.layerImages["collision"], (-self.offsetX,-self.offsetY))
		
		
		# warps
		if self.warpVisible and self.warpImg:
			screen.blit(self.warpImg, (-self.offsetX, -self.offsetY))
		
		# map objects
		sprites = [p._sprite for p in self.players.values()]
		sprites.extend([p._sprite for p in self.mobs.values() if self.isMobOnScreen(p.name)])
		
		for sprite in sorted(sprites, key = lambda k:k.mapRect.y):
			if self.selected:
				if sprite.name == self.selected:
					screen.blit(self.selectCursor, (sprite.rect.x-4, sprite.rect.y+24))
			sprite.blit(screen)
		
		# particles
		self.particleManager.blit(screen)
		
		# reset dirty lists
		self.dirtyRects = []
		self.dirtySprites = []
		self.needFullBlit = False
		
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
	m = Map("maps/testmap.txt")
	m.blit(screen)
	pygame.display.update()
