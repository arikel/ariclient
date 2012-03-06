#!/usr/bin/env python
# -*- coding: utf8 -*-

from OpenGL.GL import *
from OpenGL.GLU import *
import pygame
from pygame.locals import *
import random
from config import *
from utils import KeyHandler

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
		
		self.notFoundImg = pygame.surface.Surface((self.w, self.h))#.convert_alpha()
		self.notFoundImg.fill((180,40,40))
		
		self.emptyTile = pygame.surface.Surface((self.w, self.h))#.convert_alpha()
		self.emptyTile.fill((255,0,255))
		self.emptyTile.set_colorkey((255,0,255))
		self.emptyTile.set_alpha(100)
		
	def setImgPath(self, imgPath):
		self.imgPath = imgPath
		self.img = pygame.image.load(self.imgPath)#.convert_alpha()
		
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

class MapLayer(object):
	def __init__(self, name, w, h, tileWidth=16, tileHeight=16):
		self.name = name
		self.w = w # width in tiles
		self.h = h # height in tiles
		self.tileWidth = tileWidth
		self.tileHeight = tileHeight
		
		self.tiles = [] # [x][y] : code
		print "init MapLayer %s : w = %s, h = %s" % (name, w, h)
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
		print "Layer %s setting size : %s %s" % (self.name, w, h)
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


#-------------------------------------------------------------------------------
# Map
class Map(object):
	def __init__(self, filename = None):
		self.filename = filename
		self.screenRect = pygame.Rect((0,0,800,600))
		
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
			
	def setOffset(self, x, y):
		self.offsetX = x
		self.offsetY = y
		
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
		self.layerImages[name]#.convert_alpha()
		
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
		
	def blit(self, screen):
		# ground
		screen.blit(self.layerImages["ground"], (-self.offsetX,-self.offsetY))
		#print "Map offset : %s %s " % (self.offsetX, self.offsetY)
		
		
		# collision
		#screen.blit(self.layerImages["collision"], (-self.offsetX,-self.offsetY))
		
		
		# warps
		if self.warpVisible and self.warpImg:
			screen.blit(self.warpImg, (-self.offsetX, -self.offsetY))
		
		# map objects removed
		
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



class SpriteSheet(object):
	def __init__(self, filePath, frameW=16, frameH=16):
		self.file = filePath
		self.img = pygame.image.load(filePath)
		self.imgData = pygame.image.tostring(self.img, "RGBA", 1)
		self.w = self.img.get_width()
		self.h = self.img.get_height()
		self.frameW = frameW
		self.frameH = frameH
		
		self.X = self.w / self.frameW # image width in tiles
		self.Y = self.h / self.frameH # image height in tiles
		
		self.stepx = 1.0/self.X
		self.stepy = 1.0/self.Y
		
		self.makeArrays(50,40)
		
	def setTexture(self):
		glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, self.w,self.h,0,GL_RGBA, GL_UNSIGNED_BYTE, self.imgData)
	
	def makeArrays(self, X, Y):
		self.vertexList = []
		self.texList = []
		for x in range(X):
			for y in range(Y):
				vertex = (x,y,0)
				tex = (0, -0)
				self.vertexList.append(vertex)
				self.texList.append(tex)
				
				vertex = (x+1,y,0)
				tex = (self.stepx, -0)
				self.vertexList.append(vertex)
				self.texList.append(tex)
				
				vertex = (x+1,y-1,0)
				tex = (self.stepx, -self.stepy)
				self.vertexList.append(vertex)
				self.texList.append(tex)
				
				vertex = (x,y-1,0)
				tex = (0, -self.stepy)
				self.vertexList.append(vertex)
				self.texList.append(tex)
				
				
	def drawTile(self, x, y, tileIndexX=0, tileIndexY=0):
		dx0 = tileIndexX * self.stepx
		dx1 = (tileIndexX+1.0) * self.stepx
		dy0 = tileIndexY * self.stepy
		dy1 = (tileIndexY+1.0) * self.stepy
		
		glTranslatef(x, y, 0.0)
		
		glBegin(GL_QUADS)
		
		glTexCoord2f(dx0,-dy0)
		glVertex3f(0.0, 0.0, 0)
		
		glTexCoord2f(dx1,-dy0)
		glVertex3f(1.0, 0.0, 0)
		
		glTexCoord2f(dx1,-dy1)
		glVertex3f(1.0, -1.0, 0)
		
		glTexCoord2f(dx0,-dy1)
		glVertex3f(0.0, -1.0, 0)
		
		glEnd()
		
		glTranslatef(-x, -y, 0.0)


class Game(object):
	def __init__(self, mapFileName=None):
		
		if mapFileName:
			self.map = Map(mapFileName)
			self.mapGroundImgData = pygame.image.tostring(self.map.layerImages["ground"], "RGBA", 1)
			
		else:
			self.map = None
			self.mapGroundImgData = None
		
		video_flags = OPENGL|DOUBLEBUF
	
		pygame.init()
		pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT), video_flags)
		
		self.resize((SCREEN_WIDTH,SCREEN_HEIGHT))
		self.initGL()
		
		self.camX = -44
		self.camY = 29
		self.camZ = -56
		
		self.kh = KeyHandler()
		
		
	def resize(self, (width, height)):
		if height==0:
			height=1
		glViewport(0, 0, width, height)
		glMatrixMode(GL_PROJECTION)
		glLoadIdentity()
		gluPerspective(45, 1.0*width/height, 0.1, 10000.0)
		glMatrixMode(GL_MODELVIEW)
		glLoadIdentity()

	def initGL(self):
		glShadeModel(GL_SMOOTH)
		
		glClearColor(0.28, 0.78, 0.72, 0.0)
		glClearDepth(1.0)
		
		glEnable(GL_DEPTH_TEST)
		glDepthFunc(GL_LEQUAL)
		
		#glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)
		
		glEnable(GL_BLEND)
		glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
		
		glEnable(GL_TEXTURE_2D)
		
		texture = glGenTextures(1)
		glBindTexture(GL_TEXTURE_2D, texture)
		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
		
		glLoadIdentity()
		
	def blit(self):
		glTranslatef(self.camX, self.camY, self.camZ)
		
		self.blitGround()
		
		glTranslatef(-self.camX, -self.camY, -self.camZ)
		
	def blitGround(self):
		if not self.mapGroundImgData:
			return
		glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, self.map.w*16,self.map.h*16,0,GL_RGBA, GL_UNSIGNED_BYTE, self.mapGroundImgData)
	
		glBegin(GL_QUADS)
			
		glTexCoord2f(0,0)
		glVertex3f(0.0, 0.0, 0)
		
		glTexCoord2f(1,0)
		glVertex3f(self.map.w, 0.0, 0)
		
		glTexCoord2f(1,-1)
		glVertex3f(self.map.w, -self.map.h, 0)
		
		glTexCoord2f(0,-1)
		glVertex3f(0.0, -self.map.h, 0)
		
		glEnd()	
		
	def update(self):
		speed = 0.1
		if self.kh.keyDict[KEY_LEFT]:
			self.camX +=speed
		if self.kh.keyDict[KEY_RIGHT]:
			self.camX -=speed
		if self.kh.keyDict[KEY_UP]:
			self.camY -=speed
		if self.kh.keyDict[KEY_DOWN]:
			self.camY +=speed
		if self.kh.keyDict[KEY_SELECT_TARGET]:
			self.camZ -=speed*5
		if self.kh.keyDict[KEY_ATTACK]:
			self.camZ +=speed*5
		
	def run(self):
		self.running = True
		
		frames = 0
		ticks = pygame.time.get_ticks()
		
		while self.running:
			events = self.kh.getEvents()
			self.update()
			for event in events:
				if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
					self.running = False
				if event.type == KEYDOWN:
					if event.key == K_SPACE:
						print "Cam x,y,z : %s, %s, %s" % (self.camX, self.camY, self.camZ)
						
			glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
			self.blit()
			pygame.display.flip()
			frames = frames+1
			
		print("Game stopped")
		print("fps:  %d" % ((frames*1000)/(pygame.time.get_ticks()-ticks)))
		

if __name__ == '__main__':
	game = Game("maps/testmap.txt")
	game.run()
