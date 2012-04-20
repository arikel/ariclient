#!/usr/bin/python
# -*- coding: utf8 -*-

import pygame
import random
from gui import FONT, FONT2, TEXTCOLOR, BGCOLOR, ImgDB, EmoteDic

def colorizeSurface(baseImg, color):
	w = baseImg.get_width()
	h = baseImg.get_height()
	R = color[0]
	G = color[1]
	B = color[2]
	img = pygame.surface.Surface((w, h))
	img.fill((255,0,255))
	img.set_colorkey((255,0,255))
	
	img.blit(baseImg, (0,0))
	
	colorDic = {}
	alpha = 0.5
	
	for x in range(w):
		for y in range(h):
			c = img.get_at((x, y))
			if c[0] == c[1] and c[1]== c[2] and c[3]==255:
				color = (c.r, c.g, c.b, 255)
				
				newColor = (alpha*(R-c[0])+c[0], alpha*(G-c[1])+c[1], alpha*(B-c[2])+c[2])
				
				if color not in colorDic:
					colorDic[color] = newColor
	pix = pygame.PixelArray(img)
	for c in colorDic:
		pix.replace(c, colorDic[c])
	return img
	
def randomColor():
	r = random.randint(1,255)
	g = random.randint(1,255)
	b = random.randint(1,255)
	return (r,g,b)
	
class Animation(object):
	def __init__(self, name, imgPath, x, y, w, h, nbFrames, frameTime, mirrored = False):
		self.name = name
		self.x = x
		self.y = y
		self.w = w
		self.h = h
		self.nbFrames = nbFrames
		self.frameTime = frameTime
		self.mirror = mirrored
		img = ImgDB[imgPath].convert_alpha()
		self.frames = []
		for i in range(self.nbFrames):
			rect = pygame.Rect(x+w*i, y, w, h)
			if mirrored:
				frame = pygame.transform.flip(img.subsurface(rect), 1, 0)
			else:
				frame = img.subsurface(rect)
			self.frames.append(frame)
	
	def addImage(self, imgPath, color = None):
		img = ImgDB[imgPath]
		if color:
			img = colorizeSurface(img, color)
			
		for i in range(self.nbFrames):
			rect = pygame.Rect(self.x+self.w*i, self.y, self.w, self.h)
			if self.mirror:
				frame = pygame.transform.flip(img.subsurface(rect), 1, 0)
			else:
				frame = img.subsurface(rect)
			self.frames[i].blit(frame, (0,0))
			
class BaseSprite(object):
	def __init__(self, name, _map):
		#pygame.sprite.Sprite.__init__(self)
		self.name = name
		self._map = _map
		self.tileWidth = self._map.tileWidth
		self.tileHeight = self._map.tileHeight
		
		self.rect = pygame.Rect(0,0,1,1) # screen position
		self.mapRect = pygame.Rect(0,0,4,4) # map position
		
		self.anim = {}
		self.currentAnim = ""
		self.currentFrame = 0
		self.frameUpdateTime = 0
		
		
		#self.mapOffsetX = 0
		#self.mapOffsetY = 0
		
		self.nameImg = FONT.render(self.name, False, (20,20,20), (200,200,200,255))#.convert_alpha()
		self.nameImg.set_alpha(120)
		self.nameImg_w = self.nameImg.get_width()
		self.nameImg_h = self.nameImg.get_height()
		
		self.emoteCooldown = 0
		self.emote = None
		
		self.selected = False
		
		self.talkCooldown = 0
		self.talk = None
		self.sitting = False
		
	def setEmote(self, emote):
		if emote in EmoteDic:
			self.emote = EmoteDic[emote]
			self.emoteCooldown = pygame.time.get_ticks() + 2000
		
	def setTalk(self, msg):
		self.talk = msg
		self.talkImg = FONT.render(msg, False, (20,20,20), (200,200,200,255))#.convert_alpha()
		self.talkImg.set_alpha(120)
		self.talkCooldown = pygame.time.get_ticks() + 2000
		
	def addAnim(self, name, imgPath, x, y, w, h, nbFrames, frameTime=20, mirrored= False):
		self.anim[name] = Animation(name, imgPath, x, y, w, h, nbFrames, frameTime, mirrored)
		
	def setAnim(self, animName="idle-down"):
		if animName in self.anim and animName != self.currentAnim:
			self.currentAnim = animName
			self.rect.w = self.anim[self.currentAnim].w
			self.rect.h = self.anim[self.currentAnim].h
			if self.currentFrame >= self.anim[self.currentAnim].nbFrames:
				self.currentFrame = 0
			self.frameUpdateTime = 0
	
	def addImgAnim(self, imgPath, color = None):
		for animName in self.anim:
			anim = self.anim[animName]
			anim.addImage(imgPath, color)
	
	def setMapPos(self, x, y):
		self.mapRect.x = x
		self.mapRect.y = y
		self.rect.x = self.mapRect.x - self._map.offsetX - self.rect.w/2.0
		self.rect.y = self.mapRect.y - self._map.offsetY - self.rect.h
		
	def setPos(self, x, y):
		self.setMapPos(x, y)
		
	def getPos(self):
		return (self.mapRect.x, self.mapRect.y)
	
	def getTilePos(self):
		return(self.mapRect.x/self.tileWidth, self.mapRect.y/self.tileHeight+1)

	def getDirtyRect(self):
		nameRect = pygame.Rect(self.rect.x-4, self.rect.y+self.rect.h-2, self.nameImg_w+4, self.nameImg_h+6)
		rect = self.rect.union(nameRect)
		return rect
		
	def updateAnim(self, dx, dy):
		if dy == 1:
			if dx == 1:
				self.setAnim("walk-down-right")
			elif dx == -1:
				self.setAnim("walk-down-left")
			else:
				self.setAnim("walk-down")
				
		elif dy == -1:
			if dx == 1:
				self.setAnim("walk-up-right")
			elif dx == -1:
				self.setAnim("walk-up-left")
			else:
				self.setAnim("walk-up")
		else:
			if dx == -1:
				self.setAnim("walk-left")
			elif dx == 1:
				self.setAnim("walk-right")
			else:
				if self.currentAnim:
					if "walk" in self.currentAnim:
						self.setAnim(self.currentAnim.replace("walk", "idle"))
		
	def update(self, t=None):
		if not self.currentAnim:
			return
		
		if t == None:
			t = pygame.time.get_ticks()
		
		self.rect.x = self.mapRect.x - self._map.offsetX - self.rect.w/2.0
		self.rect.y = self.mapRect.y - self._map.offsetY - self.rect.h
		
		if t>= self.frameUpdateTime:
			self.currentFrame += 1
			if self.currentFrame >= self.anim[self.currentAnim].nbFrames:
				self.currentFrame = 0
			self.frameUpdateTime = t + self.anim[self.currentAnim].frameTime
		
		if self.emote:
			self._map.addDirtyRect(pygame.Rect(self.rect.x+3, self.rect.y-16, self.emote.get_width(), self.emote.get_height()))
			if t>self.emoteCooldown:
				self.emote = None
				
		if self.talk:
			self._map.addDirtyRect(pygame.Rect(self.rect.x-5, self.rect.y-18, self.talkImg.get_width()+8, self.talkImg.get_height()+2))
			if t>self.talkCooldown:
				self.talk = None
			
		
	def blit(self, screen):
		if not self.currentAnim:
			return
		
		self.rect.x = self.mapRect.x - self._map.offsetX - self.rect.w/2.0
		self.rect.y = self.mapRect.y - self._map.offsetY - self.rect.h
		
		screen.blit(self.anim[self.currentAnim].frames[self.currentFrame], self.rect)
			
		screen.blit(self.nameImg, (self.rect.x, self.rect.y+self.rect.h+2))
		if self.emote:
			screen.blit(self.emote, (self.rect.x+3, self.rect.y-16))
		if self.talk:
			screen.blit(self.talkImg, (self.rect.x+3, self.rect.y-16))
			
			
		pygame.draw.rect(screen,
			(255,120,120,120),
			(self.mapRect.x-self._map.offsetX, self.mapRect.y-self._map.offsetY, self.mapRect.w, self.mapRect.h),
			1)
	
	def destroy(self):
		pass

def makePlayerSprite(name, _map=None):
	sprite = BaseSprite(name, _map)
	if "ptitnem" in name.lower() or "nat" in name.lower():
		imgPath = "graphics/sprites/player/female.png"
	else:
		imgPath = "graphics/sprites/player/male.png"
		
	sprite.addAnim("walk-up", imgPath, 0, 0, 24,32,4,150)
	sprite.addAnim("walk-down", imgPath, 0, 64, 24,32,4,150)
	sprite.addAnim("walk-left", imgPath, 0, 32, 24,32,4,150, True)
	sprite.addAnim("walk-right", imgPath, 0, 32, 24,32,4,150)
	sprite.anim["walk-up-left"]=sprite.anim["walk-left"]
	sprite.anim["walk-up-right"]=sprite.anim["walk-right"]
	sprite.anim["walk-down-left"]=sprite.anim["walk-left"]
	sprite.anim["walk-down-right"]=sprite.anim["walk-right"]
	
	sprite.addAnim("idle-up", imgPath, 24, 0, 24,32,1,7500)
	sprite.addAnim("idle-down", imgPath, 24, 64, 24,32,1,7500)
	sprite.addAnim("idle-left", imgPath, 24, 32, 24,32,1,7500, True)
	sprite.addAnim("idle-right", imgPath, 24, 32, 24,32,1,7500)
	sprite.anim["idle-up-left"]=sprite.anim["idle-left"]
	sprite.anim["idle-up-right"]=sprite.anim["idle-right"]
	sprite.anim["idle-down-left"]=sprite.anim["idle-left"]
	sprite.anim["idle-down-right"]=sprite.anim["idle-right"]
	
	sprite.addAnim("sit-up", imgPath, 96, 0, 24,32,1,7500)
	sprite.addAnim("sit-down", imgPath, 96, 64, 24,32,1,7500)
	sprite.addAnim("sit-left", imgPath, 96, 32, 24,32,1,7500, True)
	sprite.addAnim("sit-right", imgPath, 96, 32, 24,32,1,7500)
	sprite.anim["sit-up-left"]=sprite.anim["sit-left"]
	sprite.anim["sit-up-right"]=sprite.anim["sit-right"]
	sprite.anim["sit-down-left"]=sprite.anim["sit-down"]
	sprite.anim["sit-down-right"]=sprite.anim["sit-down"]
	
	sprite.addImgAnim("graphics/sprites/hair/male_hair1.png", randomColor())
	sprite.addImgAnim("graphics/sprites/clothes/armor1.png", randomColor())
	
	#TEMPORARY
	#remove the comment below and comment the "hair" line to avoid hat-with-hair issue
	
	#sprite.addImgAnim("graphics/sprites/clothes/head/knight-helm.png", randomColor())
	
	sprite.setAnim("idle-down")
	
	return sprite
	
def makeMobSprite(name, _map=None):
	#print "created mob sprite : %s" % (name)
	sprite = BaseSprite(name, _map)
	imgPath = "graphics/sprites/mobs/monsters01.png"
	x = random.randint(0,3)*96
	y = random.randint(0,1)*128
	sprite.addAnim("walk-up", imgPath, x, y, 24,32,4,150)
	sprite.addAnim("walk-down", imgPath, x, y+64, 24,32,4,150)
	sprite.addAnim("walk-left", imgPath, x, y+32, 24,32,4,150, True)
	sprite.addAnim("walk-right", imgPath, x, y+32, 24,32,4,150)
	sprite.anim["walk-up-left"]=sprite.anim["walk-left"]
	sprite.anim["walk-up-right"]=sprite.anim["walk-right"]
	sprite.anim["walk-down-left"]=sprite.anim["walk-left"]
	sprite.anim["walk-down-right"]=sprite.anim["walk-right"]
	
	sprite.addAnim("idle-up", imgPath, x+24, y, 24,32,1,7500)
	sprite.addAnim("idle-down", imgPath, x+24, y+64, 24,32,1,7500)
	sprite.addAnim("idle-left", imgPath, x+24, y+32, 24,32,1,7500)
	sprite.addAnim("idle-right", imgPath, x+24, y+32, 24,32,1,7500, True)
	sprite.anim["idle-up-left"]=sprite.anim["idle-left"]
	sprite.anim["idle-up-right"]=sprite.anim["idle-right"]
	sprite.anim["idle-down-left"]=sprite.anim["idle-left"]
	sprite.anim["idle-down-right"]=sprite.anim["idle-right"]
	
	sprite.setAnim("idle-down")
	
	return sprite
	
if __name__ == "__main__":
	from utils import KeyHandler
	kh = KeyHandler()
	
	screen = pygame.display.set_mode((640,480))
	
	pygame.init()
	
	s = BaseSprite("coco")
	s.addAnim("walk", "male0.png", 0, 0, 32,64,8,75)
	s.currentAnim = "walk"
	
	
	while(True):
		kh.getEvents()
		if kh.keyDict[pygame.K_ESCAPE]:
			sys.exit()
		t = pygame.time.get_ticks()
		
		screen.fill((100,100,100))
		#screen.blit(s.currentFrame, s.rect)
		s.update(t)
		s.blit(screen)
		pygame.display.update()
	
