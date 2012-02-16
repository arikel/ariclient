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
from mapDisplay import GraphicMap
from gui import *
from utils import KeyHandler
from gameEngine import *
from gameClient import GameClient


class Game(GameClient):
	def __init__(self, host, port):
		GameClient.__init__(self, host, port)
		
		self.sprites = {}
		
		self.screen = pygame.display.set_mode((640,480))
		
		self.displayMap = GraphicMap(self.screen, "maps/001-1.tmx")
		
		#self.sprite = BaseSprite(self.name)
		#self.sprite.addAnim("walk", "graphics/sprites/male0.png", 0, 0, 32,64,8,75)
		#self.sprite.setAnim("walk")
		#self.sprite.setPos(320,240)
		
		
		# GUI
		self.chatWindow = ScrollTextWindow(0,360,640,100)
		self.entry = TextEntry("")
		self.entry.setPos(5,460)
		
		self.kh = KeyHandler()
		self.dx = 0
		self.dy = 0
		self.prevMove = (0,0)
		
		self.running = True
		
		self.sendPosCooldown = 0.0
		
		self.prevTime = 0.0
		self.speed = 0.01
		
		pygame.init()
		
	def addPlayer(self, id, x=50.0, y=50.0):
		if id == "anonymous":
			return
		self.displayMap.addPlayer(Player(id, self.displayMap, x, y))
		self.sprites[id] = BaseSprite(id)
		self.sprites[id].addAnim("walk", "graphics/sprites/male0.png", 0, 0, 32,64,8,75)
		self.sprites[id].setAnim("walk")
		
		#if name not in self.players and name != self.name:
		#	self.players[name] = BaseSprite(name)
		#	self.players[name].addAnim("walk", "graphics/sprites/male0.png", 0, 0, 32,64,8,75)
		#	self.players[name].setAnim("walk")
		#	self.players[name].setPos(320,240)
		
	def delPlayer(self, id):
		del self.sprites[id]
		self.displayMap.delPlayer(id)
		
	def update(self):
		
		t = pygame.time.get_ticks()
		x, y = pygame.mouse.get_pos()
		dt = t - self.prevTime
		self.prevTime = t
		self.prevMove = (self.dx, self.dy)
		
		if self.id not in self.displayMap.players:
			# network
			self.Loop()
			return
		
		#print "dt = %s , mouv = %s" % (dt, self.speed*dt)
		events = self.kh.getEvents()
		moved = False
		
		# keyboard handling
		
		# player direction
		self.dx = self.kh.keyDict[pygame.K_d] - self.kh.keyDict[pygame.K_q]
		self.dy = self.kh.keyDict[pygame.K_s] - self.kh.keyDict[pygame.K_z]
		
		if not self.entry.has_focus:
			
			#self.displayMap.players[self.id].update(dt)
			if (self.prevMove != (self.dx, self.dy)):# or (t>self.sendPosCooldown):
				self.displayMap.players[self.id].setMovement(self.dx, self.dy)
				#self.sendPosCooldown = t+25
				#print "Player direction changed from %s to %s/%s" % (self.prevMove, self.dx, self.dy)
				self.SendUpdateMove(self.displayMap.players[self.id].x, self.displayMap.players[self.id].y, self.dx, self.dy)
				
		self.displayMap.offsetX = self.displayMap.players[self.id].mapRect.x-320
		self.displayMap.offsetY = self.displayMap.players[self.id].mapRect.y-240
		self.displayMap.update(dt)
		
		self.chatWindow.handleEvents(x,y,events)
		
		for event in events:
			if event.type == pygame.KEYDOWN:
				key = event.key
					
				if key == pygame.K_ESCAPE and not self.entry.has_focus:
					print "Escape and no typing : quit"
					#pygame.quit()
					self.running = False
				
		res = self.entry.handleInput(events)
		
		if res:
			msg = "<" + self.name + "> " + res
			self.SendMessagePublic(msg)
			self.entry.has_focus = False
			print "message sent, losing focus"
		
		# game data
		
			
		
		
		self.displayMap.caleOffsets()
		
		# graphics 
		#self.screen.fill((100,100,140))
		#spriteList = [self.sprite] + self.sprites.values()
		spriteList = self.sprites.values()
		
		for sprite in spriteList:
			#if sprite.id not in self.displayMap.players:
			#	continue
			posx, posy = self.displayMap.players[sprite.id].getPos()
			sprite.setPos(posx, posy)
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
	pygame.quit()
