#!/usr/bin/python
# -*- coding: utf8 -*-

import random
import math
import pygame
from gameData import Item, Inventory, Being
from pathFind import astar

def getDist(a, b):# a, b == Rect or derivative : Player, Mob...
	return math.sqrt((a.x-b.x)**2+(a.y-b.y)**2)
	
class MapCreature:
	def __init__(self, name, _map = None):
		if not _map:
			return False
		self.name = name
		self._map = _map
		self.mapName = self._map.name
		
		self.category = None
		
		# float pixel position on map
		self.x = 0.0
		self.y = 0.0
		self.mapRect = pygame.Rect(0,0,10,4)
		
		# movement
		self.dx = 0.0
		self.dy = 0.0
		self.facing = (0,1)
		self.speed = 0.1
		self.mobile = False
		
		self.currentAnim = "idle"
		self.state = "idle"
		self.target = None
		self.timer = 0.0
		self.path = [] # [(x, y), (x2, y2)...]
		self._sprite = None
		self.sitting = False
		
	def toggleSit(self):
		self.sitting = not self.sitting
		if self._sprite:
			self._sprite.sitting = self.sitting
		
	def setMap(self, _map):
		self._map = _map
		
	def setSprite(self, sprite):
		self._sprite = sprite
		
	def setPos(self, x, y):
		self.x = x
		self.y = y
		
		if self._sprite:
			self._sprite.setPos(x, y)
			#if self._map.screenRect.colliderect(self._sprite.rect):
				#self._map.dirtyRects.append(self._sprite.getDirtyRect())
				#self._map.dirtySprites.append(self._sprite)
		self.mapRect.topleft = (x,y)
		
	def getPos(self):
		return (self.x, self.y)
	
	def move(self, x, y):
		self.setPos(self.x + x, self.y + y)
	
	def setMovement(self, x, y):
		self.dx = x # -1, 0, 1
		self.dy = y
		if self.dx != 0 or self.dy != 0:
			self.facing = (self.dx, self.dy)
		
	def updateAnim(self):
		if not self._sprite:return
		self._sprite.updateAnim(self.dx, self.dy)
	
	def update(self, dt=0.0):
		if not self.mobile:
			return
		if self._sprite:
			if self._map.screenRect.colliderect(self._sprite.rect):
				self._map.dirtyRects.append(self._sprite.getDirtyRect())
				self._map.dirtySprites.append(self._sprite)
			self._sprite.update() # Sprite takes a t (pygame.time.get_ticks), not a dt
			
		
		if self.nextMovePossible(dt):
			self.move(self.speed*self.dx*dt, self.speed*self.dy*dt)
			self.updateAnim()
			return
			
		# in case of collision, handle possible sliding
		oldDx = self.dx
		oldDy = self.dy
		
		self.setMovement(0, self.dy)
		if self.nextMovePossible(dt):
			self.move(self.speed*self.dx*dt, self.speed*self.dy*dt)
			self.updateAnim()
			
		else:
			self.setMovement(oldDx, 0)
			if self.nextMovePossible(dt):
				self.move(self.speed*self.dx*dt, self.speed*self.dy*dt)
				self.updateAnim()
		self.setMovement(oldDx, oldDy)
		
	def nextMovePossible(self, dt=0.0):
		if not self._map:
			print "player has no map"
			return False
		if self._map.posCollide(self.x + self.dx*self.speed*dt, self.y + self.dy*self.speed*dt):
			return False
		return True
		
class Mob(Being, MapCreature):
	def __init__(self, name, mobId, _map, x, y):
		Being.__init__(self, name)
		MapCreature.__init__(self, name, _map)
		self.mobile = True
		self.category = "mob"
		self.mobId = mobId
		self.setPos(x, y)
		self.timer = 0
		self.state = "idle"
		self.speed = 0.05
	
class Player(Being, MapCreature):
	def __init__(self, name, _map, x, y):
		Being.__init__(self, name)
		MapCreature.__init__(self, name, _map)
		self.mobile = True
		self.category = "player"
		self.setPos(x, y)
		
class MapLayer(object):
	def __init__(self, name, w, h, tileWidth=16, tileHeight=16):
		self.name = name
		self.w = w # width in tiles
		self.h = h # height in tiles
		self.tileWidth = tileWidth
		self.tileHeight = tileHeight
		
		self.tiles = [] # [x][y] : code
		#print "init MapLayer %s : w = %s, h = %s" % (name, w, h)
		for x in range(self.w):
			line = []
			for y in range(self.h):
				line.append("0000")
			self.tiles.append(line)
		
	def isValidPos(self, x, y):
		if (0<=x<self.w) and (0<=y<self.h):
			return True
		return False
		
	def getTile(self, x, y):
		return self.tiles[x][y]
		
	def setTile(self, x, y, code):
		if self.name == "collision":
			self.tiles[x][y] = int(code)
			return
		self.tiles[x][y] = code
		
	def clearTile(self, x, y):
		if self.name == "collision":
			self.tiles[x][y] = 0
		else:
			self.tiles[x][y] = "0000"
		
	def fill(self, code):
		for x in range(self.w):
			for y in range(self.h):
				self.setTile(x,y,code)
	
	def setSize(self, w, h):
		#print "Layer %s setting size : %s %s" % (self.name, w, h)
		self.oldTiles = self.tiles
		self.tiles = [] # [x][y] : code
		self.w = w
		self.h = h
		
		for x in range(self.w):
			line = []
			for y in range(self.h):
				if len(self.oldTiles)>x and len(self.oldTiles[0])>y:
					#print "copying tile %s %s (max = %s %s)" % (x, y, len(self.oldTiles), len(self.oldTiles[0]))
					line.append(self.oldTiles[x][y])
				else:
					line.append("gggg")
		
			self.tiles.append(line)
			
		
	def setData(self, data):
		tilecodes = data.split(",")
		if len(tilecodes) != self.w * self.h:
			#print "data not matching width and height"
			return False
		n = 0
		for x in range(self.w):
			for y in range(self.h):
				self.setTile(x, y, tilecodes[n])
				n +=1
	
	def getSaveData(self):
		data = []
		for x in range(self.w):
			for y in range(self.h):
				data.append(self.getTile(x, y))
		data = str(data)
		data = data.replace("[", "")
		data = data.replace("]", "")
		data = data.replace("'", "")
		data = data.replace('"', '')
		data = data.replace(' ', '')
		return data

class MapWarp(pygame.Rect):
	def __init__(self, name, x, y, w, h, targetMapName=None, destX=None, destY=None):
		self.name = name
		# x, y, w, h, destX, destY are in pixels
		pygame.Rect.__init__(self, (x, y, w, h))
		self.targetMap = targetMapName
		self.destX = destX
		self.destY = destY

class GameMap:
	def __init__(self, filename=None):
		self.filename = filename
		
		self.tileWidth = 16
		self.tileHeight = 16
		self.layers = {} # name : MapLayer
		
		if self.filename:
			self.load(self.filename)
		
		self.mobs = {}
		self.players = {}
		
		
	def addLayer(self, name):
		#print "adding layer with self w = %s, h = %s" % (self.w, self.h)
		self.layers[name] = MapLayer(name, self.w, self.h, self.tileWidth, self.tileHeight)
		
	
	def getSaveData(self):
		data = ""
		data = data + "name = " + str(self.name) + "\n"
		data = data + "w = " + str(self.w) + "\n"
		data = data + "h = " + str(self.h) + "\n"
		data = data + "tw = " + str(self.tileWidth) + "\n"
		data = data + "th = " + str(self.tileHeight) + "\n"
		
		for layerName in self.layers:
			data = data + layerName + " = " + str(self.layers[layerName].getSaveData()) + "\n\n"
		return data
		
	def save(self, filename):
		self.filename = filename
		f = open(filename, "w")
		f.write(self.getSaveData())
		f.close()
		print "Map saved in %s" % (filename)
		
		
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
				elif key.strip() == "tw":
					self.tileWidth = int(value.strip())
				elif key.strip() == "th":
					self.tileHeight = int(value.strip())
				else:
					codes = value.split(',')
					if len(codes) == self.w * self.h:
						layerName = key.strip()
						value = value.strip()
						print "Loading layer %s" % (layerName)
						self.addLayer(layerName)
						self.layers[layerName].setData(value)
		if "collision" not in self.layers:
			self.makeCollisionGrid()
		
	def makeCollisionGrid(self):
		if not self.filename:return False
		self.addLayer("collision")
		for x in range(self.w):
			for y in range(self.h):
				if self.layers["ground"].getTile(x, y) == "wwww":
					self.layers["collision"].tiles[x][y] = 1
				else:
					self.layers["collision"].tiles[x][y] = 0
		
		
	def isValidPos(self, x, y):
		if (0<=x<self.w) and (0<=y<self.h):
			return True
		return False
		
	def setSize(self, x, y):
		for layerName in self.layers:
			self.w = x
			self.h = y
			self.layers[layerName].setSize(x, y)
			
	def clearTile(self, layerName, x, y):
		self.layers[layerName].clearTile(x, y)
		
	def setTile(self, layerName, x, y, code):
		if not layerName in self.layers:return
		if not self.isValidPos(x, y):return
		if code == self.layers[layerName].getTile(x, y):return
		
		
		self.layers[layerName].setTile(x, y, code)
		if layerName == "ground" and code == "wwww":
			self.layers["collision"].setTile(x, y, 1)
		elif layerName == "ground":
			self.layers["collision"].setTile(x, y, 0)
			
		if layerName == "collision":
			return
		
		# check tile up left
		if self.isValidPos(x-1, y-1):
			oldCode = self.layers[layerName].getTile(x-1, y-1)
			newCode = oldCode[0:3] + code[0]
			self.layers[layerName].setTile(x-1, y-1, newCode)
			
			
		# check tile up
		if self.isValidPos(x, y-1):
			oldCode = self.layers[layerName].getTile(x, y-1)
			newCode = oldCode[0:2] + code[0:2]
			self.layers[layerName].setTile(x, y-1, newCode)
			
		# check tile up right
		if self.isValidPos(x+1, y-1):
			oldCode = self.layers[layerName].getTile(x+1, y-1)
			newCode = oldCode[0:2] + code[1] + oldCode[3]
			self.layers[layerName].setTile(x+1, y-1, newCode)
			
		# check tile left
		if self.isValidPos(x-1, y):
			oldCode = self.layers[layerName].getTile(x-1, y)
			newCode = oldCode[0] + code[1] + oldCode[2] + code[3]
			self.layers[layerName].setTile(x-1, y, newCode)
			
		# check tile right
		if self.isValidPos(x+1, y):
			oldCode = self.layers[layerName].getTile(x+1, y)
			newCode = code[0] + oldCode[1] + code[2] + oldCode[3]
			self.layers[layerName].setTile(x+1, y, newCode)
			
		# check tile down left
		if self.isValidPos(x-1, y+1):
			oldCode = self.layers[layerName].getTile(x-1, y+1)
			newCode = oldCode[0] + code[2] + oldCode[2:4]
			self.layers[layerName].setTile(x-1, y+1, newCode)
			
		# check tile down
		if self.isValidPos(x, y+1):
			oldCode = self.layers[layerName].getTile(x, y+1)
			newCode = code[0:2] + oldCode[2:4]
			self.layers[layerName].setTile(x, y+1, newCode)
			
		# check tile down right
		if self.isValidPos(x+1, y+1):
			oldCode = self.layers[layerName].getTile(x+1, y+1)
			newCode = code[0] + oldCode[1:4]
			self.layers[layerName].setTile(x+1, y+1, newCode)
			
	
	def tileCollide(self, x, y): # tile position collide test
		if not self.isValidPos(x, y):
			return True
		if self.layers["collision"].tiles[x][y]>0:
			return True
		return False
		
	def posCollide(self, x, y): # pixel position collide test
		return self.tileCollide(int(x)/self.tileWidth, int(y)/self.tileHeight)
		
	
	def addPlayer(self, playerId, x, y):
		if playerId not in self.players:
			self.players[playerId]=Player(playerId, self, x, y)
			
	def delPlayer(self, playerName):
		del self.players[playerName]
	
	def addMob(self, name, mobId, x, y):
		self.mobs[name]=Mob(name, mobId, self, x, y)
		
	def delMob(self, name):
		del self.mobs[name]
		
	def update(self, dt):
		for player in self.players.values():
			player.update(dt)
		for mob in self.mobs.values():
			mob.update(dt)
