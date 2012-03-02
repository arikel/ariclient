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
from mapDisplay import Map
from gui import *
from utils import KeyHandler
from gameEngine import *
from gameClient import GameClient

class Game(GameClient):
	def __init__(self, host, port):
		self.screen = SCREEN
		
		pygame.init()
		
		# GUI
		self.gui = ClientGUI(self)
		self.id = self.gui.launchLogin()
		
		GameClient.__init__(self, host, port)
		
		self.Send({"action": "nickname", "id": self.id})
		
		self.displayMap = Map("maps/testmap.txt")
		
		self.kh = KeyHandler()
		self.dx = 0
		self.dy = 0
		self.prevMove = (0,0)
		
		self.running = True
		
		self.sendPosCooldown = 0.0
		
		self.prevTime = 0.0
		self.speed = 0.05

	def addPlayer(self, id, x, y):
		if id == "anonymous":
			return
		print "adding player to map : %s, at %s, %s" % (id, x, y)
		self.displayMap.addPlayer(id, x, y)
		#self.displayMap.players[id].setMovement(1, 1)
		#self.displayMap.players[id].setMovement(0, 0)
		#print "Player %s 's map = %s" % (self.displayMap.players[id].id, self.displayMap.players[id]._map)
		
	def delPlayer(self, id):
		self.displayMap.delPlayer(id)
	
	def addMob(self, id, x=50.0, y=50.0):
		#print "adding mob %s" % (id)
		self.displayMap.addMob(id, 1, x, y)
			
	def delMob(self, id):
		self.displayMap.delMob(id)
		
	def setMap(self, mapFileName, x, y):
		self.displayMap = Map(mapFileName)
		self.addPlayer(self.id, x, y)
		
	def getClosestMobName(self):
		myRect = self.displayMap.players[self.id].mapRect
		minDist = 2000.0
		closestMob = None
		for mobName, mob in self.displayMap.mobs.items():
			dist = getDist(mob.mapRect, myRect)
			if dist < minDist:
				minDist = dist
				closestMob = mobName
		return closestMob
		
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
		
		events = self.kh.getEvents()
		moved = False
		
		# keyboard handling
		
		# player direction
		self.dx = self.kh.keyDict[KEY_RIGHT] - self.kh.keyDict[KEY_LEFT]
		self.dy = self.kh.keyDict[KEY_DOWN] - self.kh.keyDict[KEY_UP]
		
		if not self.gui.entry.has_focus:
			
			if (self.prevMove != (self.dx, self.dy)):# or (t>self.sendPosCooldown):
				self.displayMap.players[self.id].setMovement(self.dx, self.dy)
				#self.sendPosCooldown = t+25
				#print "Player direction changed from %s to %s/%s" % (self.prevMove, self.dx, self.dy)
				self.SendUpdateMove(self.displayMap.players[self.id].x, self.displayMap.players[self.id].y, self.dx, self.dy)
		
		else:
			self.dx = 0
			self.dy = 0
				
		self.displayMap.offsetX = self.displayMap.players[self.id].mapRect.x-SCREEN_WIDTH/2
		self.displayMap.offsetY = self.displayMap.players[self.id].mapRect.y-SCREEN_HEIGHT/2
		self.displayMap.update(dt)
		
		for event in events:
			if event.type == pygame.KEYDOWN:
				key = event.key

				if key == pygame.K_ESCAPE and not self.gui.entry.has_focus:
					#print "Escape and no typing : quit"
					#pygame.quit()
					self.running = False
				
				if key == pygame.K_SPACE and not self.gui.entry.has_focus:
					#print "Starting to type text..."
					self.SendWarpRequest("second", 50,70)
				
				if key == KEY_SELECT_TARGET:
					mobName = self.getClosestMobName()
					if mobName:
						self.displayMap.selectTarget(mobName)
				
				if key == KEY_ATTACK:
					if self.displayMap.selected:
						self.SendAttackMob(self.displayMap.selected)
					
			if event.type == pygame.QUIT:
				#pygame.quit()
				self.running = False
		
		self.gui.handleEvents(events)

		
		# graphics 
		
		self.screen.fill((0,0,0))
		self.displayMap.blit(self.screen)
		
		# gui display
		self.gui.blit()
		
		pygame.display.flip()
		
		# network
		self.Loop()
		
		
		
if __name__=="__main__":

	#Efficient command-line options parser
	parser = OptionParser(prog = "ariclient", usage = "usage: %prog [options] arg")

	#Definition of the command-line options
	parser.add_option("-s", "--server", dest = "SERVER_ADDRESS", help = "Override the server address.\nDefault: %s" % (SERVER_ADDRESS,))
	parser.add_option("-p", "--port", dest = "SERVER_PORT", help = "Override the server port.\nDefault: %d" % (SERVER_PORT,))

	(options, args) = parser.parse_args()

	if(options.SERVER_ADDRESS):
		SERVER_ADDRESS = options.SERVER_ADDRESS
	if(options.SERVER_PORT):
		SERVER_PORT = int(options.SERVER_PORT)

	g = Game(SERVER_ADDRESS, SERVER_PORT)
	
	while g.running:
		g.update()

	pygame.quit()
