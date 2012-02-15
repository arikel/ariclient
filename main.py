#!/usr/bin/python
# -*- coding: utf-8 -*-
try:
	import psyco
	psyco.full()
	print("module psyco found.")
except:
	print("module psyco NOT found.")

import pygame
from sprite import BaseSprite
from mapHandler import GraphicMap
from gui import *
from utils import KeyHandler
from gameClient import Client

class Game(Client):
	def __init__(self, host, port):
		Client.__init__(self, host, port)
		
		self.players = {} # name : sprite
		
		self.screen = pygame.display.set_mode((640,480))
		
		self.displayMap = GraphicMap(self.screen, "maps/001-1.tmx")
		self.sprite = BaseSprite(self.name)
		self.sprite.addAnim("walk", "graphics/sprites/male0.png", 0, 0, 32,64,8,75)
		self.sprite.setAnim("walk")
		self.sprite.setPos(320,240)
		
		
		# GUI
		self.chatWindow = ScrollTextWindow(0,360,640,100)
		self.entry = TextEntry("")
		self.entry.setPos(5,460)
		
		self.kh = KeyHandler()
		
		self.running = True
		
		self.sendPosCooldown = 0.0
		
		self.prevTime = 0.0
		self.speed = 0.2
		
		pygame.init()
		
	def addPlayer(self, name):
		if name not in self.players and name != self.name:
			self.players[name] = BaseSprite(name)
			self.players[name].addAnim("walk", "graphics/sprites/male0.png", 0, 0, 32,64,8,75)
			self.players[name].setAnim("walk")
			self.players[name].setPos(320,240)
		
	def update(self):
		t = pygame.time.get_ticks()
		x, y = pygame.mouse.get_pos()
		dt = t - self.prevTime
		self.prevTime = t
		#self.prevMove = (self.dx, self.dy)
		
		#print "dt = %s , mouv = %s" % (dt, self.speed*dt)
		events = self.kh.getEvents()
		moved = False
		
		# keyboard handling
		#if self.kh.keyDict[pygame.K_ESCAPE] == 1:
		#	self.running = False
			
		if self.kh.keyDict[pygame.K_z] and not self.entry.has_focus:
			self.sprite.mapRect.y -= dt*self.speed
			moved = True
		if self.kh.keyDict[pygame.K_s] and not self.entry.has_focus:
			self.sprite.mapRect.y += dt*self.speed
			moved = True
		if self.kh.keyDict[pygame.K_q] and not self.entry.has_focus:
			self.sprite.mapRect.x -= dt*self.speed
			moved = True
		if self.kh.keyDict[pygame.K_d] and not self.entry.has_focus:
			self.sprite.mapRect.x += dt*self.speed
			moved = True
		
		self.chatWindow.handleEvents(x,y,events)
		
			
		for event in events:
			if event.type == pygame.KEYDOWN:
				key = event.key
					
				if key == pygame.K_ESCAPE and not self.entry.has_focus:
					print "Escape and no typing : quit"
					pygame.quit()
				
				#if key == pygame.K_t and not self.entry.has_focus:
				#	self.entry.has_focus = True
		
		res = self.entry.handleInput(events)
		
		if res:
			msg = "<" + self.name + "> " + res
			self.SendMessagePublic(msg)
			self.entry.has_focus = False
			print "message sent, losing focus"
		
		# game data
		if moved and t>self.sendPosCooldown:
			self.sendPosCooldown = t+25
			self.SendPosition()
			
		self.displayMap.offsetX = self.sprite.mapRect.x-320
		self.displayMap.offsetY = self.sprite.mapRect.y-240
		
		self.displayMap.caleOffsets()
		
		# graphics 
		#self.screen.fill((100,100,140))
		spriteList = [self.sprite] + self.players.values()
		for sprite in spriteList:
			sprite.update(t)
			sprite.setMapOffset(self.displayMap.offsetX, self.displayMap.offsetY)
			
		self.displayMap.blitLayer("ground")
		self.displayMap.blitSpritesAndFringe(spriteList)
		self.displayMap.blitLayer("over")
		self.displayMap.blitLayer("collision")
		
		# gui
		self.chatWindow.updateSurface(x,y)
		self.entry.updateSurface()
		
		self.chatWindow.blit(self.screen)
		self.entry.blit(self.screen)
		
		pygame.display.flip()
		
		# network
		self.Loop()
		
		
		
if __name__=="__main__":
	running = True
	g = Game('88.173.217.230', 18647)
	
	while running:
		g.update()
		
		if not g.running:
			running = False
