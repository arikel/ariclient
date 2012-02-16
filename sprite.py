#!/usr/bin/python
# -*- coding: utf8 -*-

import pygame
from gui import *

class Animation(object):
	def __init__(self, id, imgPath, x, y, w, h, nbFrames, frameTime, mirrored = False):
		self.id = id
		self.x = x
		self.y = y
		self.w = w
		self.h = h
		self.nbFrames = nbFrames
		self.frameTime = frameTime
		
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
		self.currentAnim = None
		self.currentFrame = 0
		self.frameUpdateTime = 0
		
		self.tileWidth = tileWidth
		self.tileHeight = tileHeight
		self.mapOffsetX = 0
		self.mapOffsetY = 0
		
	def addAnim(self, id, imgPath, x, y, w, h, nbFrames, frameTime=20):
		self.anim[id] = Animation(id, imgPath, x, y, w, h, nbFrames, frameTime)
		
	def setAnim(self, animName):
		if animName in self.anim:
			#self.currentAnim = self.anim[animName]
			self.currentAnim = animName
			self.rect.w = self.anim[self.currentAnim].w
			self.rect.h = self.anim[self.currentAnim].h
		
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
		self.rect.y = self.mapRect.y - y + self.tileHeight - self.rect.h
	
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
	
	def blit(self, screen):
		if self.currentAnim:
			screen.blit(self.anim[self.currentAnim].frames[self.currentFrame], self.rect)
			screen.blit(FONT.render(self.id, False, TEXTCOLOR), (self.rect.x, self.rect.y+66))
			
			screen.blit(
				FONT.render("X", False, TEXTCOLOR),
				(self.rect.x+self.rect.w/2, self.rect.y+self.rect.h-16))
			
	def destroy(self):
		pass
			
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
	
