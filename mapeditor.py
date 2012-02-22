#!/usr/bin/python
# -*- coding: utf-8 -*-

# mapeditor.py

import pygame
import random
	

class MapTile(object):
	def __init__(self, id, code, w, h):
		self.id = id
		self.code = code
		self.w = w
		self.h = h
		
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
			print "couldn't find tile for code : %s, i only know %s" % (code, self.tiles.keys())
			return self.notFoundImg
		nb = len(self.tiles[code])
		tile = random.randint(1, nb) - 1
		return self.tiles[code][tile]

class MapLayer(object):
	def __init__(self, name, w, h, tileWidth=16, tileHeight=16):
		self.name = name
		self.w = w # width in tiles
		self.h = h # height in tiles
		self.tileWidth = tileWidth
		self.tileHeight = tileHeight
		
		self.tiles = [] # [x][y] : code
		for x in range(self.w):
			line = []
			for y in range(self.h):
				line.append(0)
			self.tiles.append(line)
		
		
	def getTile(self, x, y):
		return self.tiles[x][y]
		
	def setTile(self, x, y, code):
		self.tiles[x][y] = code
		
	def clearTile(self, x, y):
		self.tiles[x][y] = 0
		
	def fill(self, code):
		for x in range(self.w):
			for y in range(self.h):
				self.setTile(x,y,code)
	
	def setData(self, data):
		tilecodes = data.split(",")
		if len(tilecodes) != self.w * self.h:
			print "data not matching width and height"
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
		
class Map(object):
	def __init__(self, w, h, tileWidth=16, tileHeight=16):
		self.w = w
		self.h = h
		self.tileWidth = tileWidth
		self.tileHeight = tileHeight
		
		self.tileset = MapTileset("tilesets.txt")
		
		self.layers = {} # name : MapLayer
		self.layerImages = {} # name : (big) surface
		
		self.addLayer("ground")
		self.layers["ground"].fill("gggg")
		self.updateLayerImage("ground")
		
		self.offsetX = 0
		self.offsetY = 0
		
		self.offsetXmax = 0
		self.offsetYmax = 0
		
	def setOffset(self, x, y):
		self.offsetX = x
		self.offsetY = y
		
	def isValidPos(self, x, y):
		if (0<=x<self.w) and (0<=y<self.h):
			return True
		return False
		
	def getSaveData(self):
		data = ""
		data = data + "w = " + str(self.w) + "\n\n"
		data = data + "h = " + str(self.h) + "\n\n"
		
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
						
	def addLayer(self, name):
		self.layers[name] = MapLayer(name, self.w, self.h, self.tileWidth, self.tileHeight)
		self.makeLayerImage(name)
		
	def makeLayerImage(self, name):
		if name not in self.layers:return
		self.layerImages[name] = pygame.surface.Surface((self.w*self.tileWidth, self.h * self.tileHeight))
		self.updateLayerImage(name)
		
	def updateLayerImage(self, name):
		self.layerImages[name].fill((150,150,150))
		for x in range(self.w):
			for y in range(self.h):
				code = self.layers[name].getTile(x, y)
				self.layerImages[name].blit(self.tileset.getTile(code), (x*self.tileWidth, y*self.tileHeight))
	
	def blit(self, screen):
		screen.blit(self.layerImages["ground"], (0,0))
		
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


	
if __name__ == "__main__":
	from utils import KeyHandler
	screen = pygame.display.set_mode((640,480))
	kh = KeyHandler()
	m = Map(30,20)
	while kh.keyDict[pygame.K_ESCAPE]==0:
		events = kh.getEvents()
		for event in events:
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
					pass
				elif event.key == pygame.K_s:
					m.save("testmap.txt")
				elif event.key == pygame.K_l:
					m.load("testmap.txt")
					
		if pygame.mouse.get_pressed()[0]==1:
			x, y = pygame.mouse.get_pos()
			x, y = x/m.tileWidth, y/m.tileHeight
			m.setTile("ground", x, y, "wwww")
		
		if pygame.mouse.get_pressed()[2]==1:
			x, y = pygame.mouse.get_pos()
			x, y = x/m.tileWidth, y/m.tileHeight
			m.setTile("ground", x, y, "gggg")
			#m.clearTile("ground", x, y)
			
		screen.fill((0,0,0))
		m.blit(screen)
		pygame.display.update()

else:
	screen = pygame.display.set_mode((640,480))
	
	
