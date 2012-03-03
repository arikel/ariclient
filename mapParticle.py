#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame
from config import *
from guiFunctions import ImgDB, FONT, FONT2
from gameEngine import *

			
class MapParticle(object):
	def __init__(self, _map, x, y, genre = "damage", text=None, ttl = 2000):
		self._map = _map
		self.genre = genre
		self.text = text
		# particle map position, in pixels
		self.x = x
		self.y = y
		self.deathTime = pygame.time.get_ticks() + ttl
		self.makeImage()
		
	def makeImage(self):
		if self.genre == "damage":
			self.img = pygame.image.load("graphics/gui/guibase.png").convert_alpha().subsurface((64,16,50,20))
		else:
			self.img = pygame.image.load("graphics/gui/guibase.png").convert_alpha().subsurface((64,36,50,20))
		
		
		if self.text:
			if self.genre == "damage":
				self.img.blit(FONT2.render(self.text, False, (250,250,120)), (16,0))
			else:
				self.img.blit(FONT2.render(self.text, False, (60,100,250)), (16,0))
		
	def update(self):
		
		self.screen_x = self.x - self._map.offsetX
		self.screen_y = self.y - self._map.offsetY
		
		if pygame.time.get_ticks()>self.deathTime:
			return
		self.y -= 0.1
		
	def blit(self, screen):
		screen.blit(self.img, (self.screen_x, self.screen_y))
		
		
class MapParticleManager(object):
	def __init__(self, _map):
		self._map = _map
		self.particles = []
		
	def addParticle(self, genre, x, y, text=None):
		particle = MapParticle(self._map, x, y, genre, text)
		self.particles.append(particle)
		
	def update(self):
		t = pygame.time.get_ticks()
		for particle in self.particles:
			particle.update()
		for particle in self.particles:
			if particle.deathTime < t:
				self.particles.remove(particle)
	
	def blit(self, screen):
		for particle in self.particles:
			particle.blit(screen)
	