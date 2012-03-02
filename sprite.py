#!/usr/bin/python
# -*- coding: utf8 -*-

import pygame
import random
from gui import FONT, FONT2, TEXTCOLOR, BGCOLOR, ImgDB, EmoteDic



class Animation(object):
	def __init__(self, id, imgPath, x, y, w, h, nbFrames, frameTime, mirrored = False):
		self.id = id
		self.x = x
		self.y = y
		self.w = w
		self.h = h
		self.nbFrames = nbFrames
		self.frameTime = frameTime
		
		if imgPath in ImgDB:
			img = ImgDB[imgPath]
		else:
			img = pygame.image.load(imgPath).convert_alpha()
		#print "image loaded, rect = %s" % (img.get_rect())
		self.frames = []
		for i in range(self.nbFrames):
			#print "making frame %s %s %s %s" % (x+w*i, y, w, h)
			rect = pygame.Rect(x+w*i, y, w, h)
			if mirrored:
				frame = pygame.transform.flip(img.subsurface(rect), 1, 0)
			else:
				frame = img.subsurface(rect)
			
			self.frames.append(frame)
			


class BaseSprite(object):
	def __init__(self, id, tileWidth = 16, tileHeight = 16):
		#pygame.sprite.Sprite.__init__(self)
		self.id = id
		self.name = self.id
		
		self.rect = pygame.Rect(0,0,1,1) # screen position
		self.mapRect = pygame.Rect(0,0,1,1) # map position
		
		self.anim = {}
		self.currentAnim = "idle-down"
		self.currentFrame = 0
		self.frameUpdateTime = 0
		
		self.tileWidth = tileWidth
		self.tileHeight = tileHeight
		self.mapOffsetX = 0
		self.mapOffsetY = 0
		
		self.idImg = FONT.render(self.id, False, (20,20,20), (200,200,200,255)).convert_alpha()
		self.idImg.set_alpha(120)
		
		self.emoteCooldown = 0
		self.emote = None
		
		self.selected = False
		
		self.talkCooldown = 0
		self.talk = None
		
	def setEmote(self, emote):
		if emote in EmoteDic:
			self.emote = EmoteDic[emote]
			self.emoteCooldown = pygame.time.get_ticks() + 2000
		
	def setTalk(self, msg):
		self.talkImg = FONT.render(msg, False, (20,20,20), (200,200,200,255))
		self.talkCooldown = pygame.time.get_ticks() + 2000
		
	def addAnim(self, id, imgPath, x, y, w, h, nbFrames, frameTime=20, mirrored= False):
		self.anim[id] = Animation(id, imgPath, x, y, w, h, nbFrames, frameTime, mirrored)
		
	def setAnim(self, animName):
		if animName in self.anim and animName != self.currentAnim:
			#self.currentAnim = self.anim[animName]
			self.currentAnim = animName
			self.rect.w = self.anim[self.currentAnim].w
			self.rect.h = self.anim[self.currentAnim].h
			if self.currentFrame >= self.anim[self.currentAnim].nbFrames:
				self.currentFrame = 0
			self.frameUpdateTime = 0
				
	def setMapPos(self, x, y):
		self.mapRect.x = x
		self.mapRect.y = y
	
	def setPos(self, x, y):
		self.setMapPos(x, y)
		
	def getPos(self):
		return (self.mapRect.x, self.mapRect.y)
	
	def getTilePos(self):
		return(self.mapRect.x/self.tileWidth, self.mapRect.y/self.tileHeight+1)
	
	def setMapOffset(self, x, y):
		self.rect.x = self.mapRect.x - x - self.rect.w/2
		#self.rect.y = self.mapRect.y - y + self.tileHeight - self.rect.h
		self.rect.y = self.mapRect.y - y - self.rect.h
		
	
	
	def update(self, t=None):
		if t == None:
			t = pygame.time.get_ticks()
		
		# if no animation playing, no update
		if not self.currentAnim:
			return
		
		if t>= self.frameUpdateTime:
			self.currentFrame += 1
			if self.currentFrame >= self.anim[self.currentAnim].nbFrames:
				self.currentFrame = 0
			self.frameUpdateTime = t + self.anim[self.currentAnim].frameTime
		
		if self.emote:
			if t>self.emoteCooldown:
				self.emote = None
				
		if self.talk:
			if t>self.talkCooldown:
				self.talk = None
			
		
	def blit(self, screen):
		if self.currentAnim:
			screen.blit(self.anim[self.currentAnim].frames[self.currentFrame], self.rect)
			#screen.blit(FONT.render(self.id, False, TEXTCOLOR), (self.rect.x, self.rect.y+self.rect.h+2))
			screen.blit(self.idImg, (self.rect.x, self.rect.y+self.rect.h+2))
			if self.emote:
				screen.blit(self.emote, (self.rect.x+3, self.rect.y-16))
			if self.talk:
				screen.blit(self.talkImg, (self.rect.x+3, self.rect.y-16))
			
			#screen.blit(
			#	FONT.render("o", False, TEXTCOLOR),
			#	(self.rect.x+self.rect.w/2, self.rect.y+self.rect.h-16))
			#pygame.draw.rect(screen, (255,120,120,120), self.rect, 1)
	
	def destroy(self):
		pass

def makePlayerSprite(name, tw=16, th=16):
	sprite = BaseSprite(name, tw, th)
	if name == "ptitnem":
		imgPath = "graphics/sprites/female.png"
	else:
		imgPath = "graphics/sprites/male.png"
		
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
	return sprite
	
def makeMobSprite(name, tw=16, th=16):
	#print "created mob sprite : %s" % (name)
	sprite = BaseSprite(name, tw, th)
	imgPath = "graphics/sprites/monsters01.png"
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
	
