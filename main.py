#!/usr/bin/python
# -*- coding: utf-8 -*-
try:
	import psyco
	psyco.full()
	print("module psyco found.")
except:
	print("module psyco NOT found.")

import pygame
from config import *
from optparse import OptionParser

SCREEN = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

from sprite import BaseSprite, makePlayerSprite, makeMobSprite
from mapDisplay import GraphicMap
from gui import *
from utils import KeyHandler
from gameEngine import *
from gameClient import GameClient



class Game(GameClient):
	def __init__(self, host, port):
		self.screen = SCREEN
		pygame.init()
		
		self.loginScreen = LoginScreen()
		self.id = self.loginScreen.launch(self.screen)
		
		GameClient.__init__(self, host, port)
		
		self.Send({"action": "nickname", "id": self.id})
		
		self.sprites = {}
		
		#self.screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
		
		self.displayMap = GraphicMap(self.screen, "maps/001-1.tmx")
		
		# GUI
		self.chatWindow = ScrollTextWindow(0,SCREEN_HEIGHT-120,SCREEN_WIDTH,100)
		self.entry = TextEntry("")
		self.entry.setPos(5,SCREEN_HEIGHT-20)
		
		self.kh = KeyHandler()
		self.dx = 0
		self.dy = 0
		self.prevMove = (0,0)
		
		self.running = True
		
		self.sendPosCooldown = 0.0
		
		self.prevTime = 0.0
		self.speed = 0.05
		
		
		
	def addPlayer(self, id, x=50.0, y=50.0):
		if id == "anonymous":
			return
		print "adding player to map : %s" % (id)
		self.displayMap.addPlayer(Player(id, self.displayMap, x, y))
		self.sprites[id] = makePlayerSprite(id)
		self.displayMap.players[id].setMovement(1, 1)
		self.displayMap.players[id].setMovement(0, 0)
		
	def addMob(self, id, x=50.0, y=50.0):
		print "adding mob %s" % (id)
		self.displayMap.addMob(Mob(id, 1, self.displayMap, x, y))
		self.sprites[id] = makeMobSprite(id)
		
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
			#print "not connected to map"
			# network
			self.Loop()
			return
		
		#print "dt = %s , mouv = %s" % (dt, self.speed*dt)
		events = self.kh.getEvents()
		moved = False
		
		# keyboard handling
		
		# player direction
		self.dx = self.kh.keyDict[KEY_RIGHT] - self.kh.keyDict[KEY_LEFT]
		self.dy = self.kh.keyDict[KEY_DOWN] - self.kh.keyDict[KEY_UP]
		
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
					#print "Escape and no typing : quit"
					#pygame.quit()
					self.running = False
				if key == pygame.K_RETURN and not self.entry.has_focus:
					#print "Starting to type text..."
					self.entry.getFocus()
				
			if event.type == pygame.QUIT:
				#pygame.quit()
				self.running = False
				
		res = self.entry.handleInput(events)
		
		if res:
			#msg = "<" + self.name + "> " + res
			#self.SendMessagePublic(msg)
			self.SendMessagePublic(res)
			self.entry.has_focus = False
			#print "message sent, losing focus"
		
		# game data
		
			
		
		
		self.displayMap.caleOffsets()
		
		# graphics 
		#self.screen.fill((100,100,140))
		#spriteList = [self.sprite] + self.sprites.values()
		spriteList = self.sprites.values()
		
		for sprite in spriteList:
			#if sprite.id not in self.displayMap.players:
			#	continue
			if sprite.id in self.displayMap.players:
				player = self.displayMap.players[sprite.id]
				#print "blitting player : %s" % (sprite.id)
			elif sprite.id in self.displayMap.mobs:
				player = self.displayMap.mobs[sprite.id]
			else:
				continue
			posx, posy = player.getPos()
			sprite.setPos(posx, posy)
			
			if player.dy == 1:
				if player.dx == 1:
					sprite.setAnim("walk-down-right")
				elif player.dx == -1:
					sprite.setAnim("walk-down-left")
				else:
					sprite.setAnim("walk-down")
					
			elif player.dy == -1:
				if player.dx == 1:
					sprite.setAnim("walk-up-right")
				elif player.dx == -1:
					sprite.setAnim("walk-up-left")
				else:
					sprite.setAnim("walk-up")
			else:
				if player.dx == -1:
					sprite.setAnim("walk-left")
				elif player.dx == 1:
					sprite.setAnim("walk-right")
				else:
					if sprite.currentAnim:
						if "walk" in sprite.currentAnim:
							sprite.setAnim(sprite.currentAnim.replace("walk", "idle"))
			
			sprite.update(t)
			sprite.setMapOffset(self.displayMap.offsetX, self.displayMap.offsetY)
			
		self.displayMap.blitLayer("ground")
		self.displayMap.blitSpritesAndFringe(spriteList)
		self.displayMap.blitLayer("over")
		#self.displayMap.blitLayer("collision")
		
		# gui display
		self.chatWindow.updateSurface(x,y)
		self.entry.updateSurface()
		
		self.chatWindow.blit(self.screen)
		self.entry.blit(self.screen)
		
		pygame.display.flip()
		
		# network
		self.Loop()
		
		
		
if __name__=="__main__":

        #Efficient command-line options parser
	parser = OptionParser(prog = "ariclient",
                          usage = "usage: %prog [options] arg")

        #Definition of the command-line options
	parser.add_option("-s", "--server", dest = "SERVER_ADDRESS",
                          help = "Override the server address.\nDefault: %s" % (SERVER_ADDRESS,))
	parser.add_option("-p", "--port", dest = "SERVER_PORT",
                          help = "Override the server port.\nDefault: %d" % (SERVER_PORT,))

	(options, args) = parser.parse_args()

	if(options.SERVER_ADDRESS):
                SERVER_ADDRESS = options.SERVER_ADDRESS
	if(options.SERVER_PORT):
                SERVER_PORT = int(options.SERVER_PORT)

	
	running = True
	g = Game(SERVER_ADDRESS, SERVER_PORT)
	
	while g.running:
		g.update()

	pygame.quit()
