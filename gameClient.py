#!/usr/bin/python
# -*- coding: utf8 -*-

import sys
from time import sleep
from sys import stdin, exit

from PodSixNet.Connection import connection, ConnectionListener
from guiFunctions import ustr
from gameEngine import *

class GameClient(ConnectionListener):
	def __init__(self, host, port):
		self.Connect((host, port))
		print "ariclient started"
		
		# get a nickname from the user before starting
		#print "Enter your nickname: ",
		#self.name = stdin.readline().rstrip("\n")
		#self.id = self.name
		#connection.Send({"action": "nickname", "id": self.id})
		#print "asking connection with name = %s" % (self.id)
		
	def Loop(self):
		connection.Pump()
		self.Pump()
	
	
	def SendMessagePublic(self, msg):
		msg = msg.encode("utf-8", "replace")
		connection.Send({"action": "public_message", "message": msg})
		#print "sent message : %s " % (msg)
		print "Sending message : %s" % (msg)
		
	def SendMessagePrivate(self, target, msg):
		connection.Send({"action": "private_message", "target" : target, "message": msg})
		
		
	def SendUpdateMove(self, x, y, dx, dy):
		connection.Send({"action": "player_update_move", "x":x, "y":y, "dx":dx, "dy": dy})
		
	def SendAttackMob(self, mobId):
		connection.Send({"action": "attack_mob", "target":mobId})
		
	def SendLogin(self, password):
		connection.Send({"action": "login", "id":self.id, "password" : password})
		
	def SendEmote(self, emote):
		connection.Send({"action": "emote", "emote" : emote})
		
	def SendWarpRequest(self, mapName, x, y):
		connection.Send({"action": "warp_request", "mapName":mapName, "x":x, "y":y})
		
	#######################################
	### Network event/message callbacks ###
	#######################################
	
	#-------------------------------------------------------------------
	# on client receive from server :
	#-------------------------------------------------------------------
	'''
	def Network_players(self, data):
		print "*** players: " + ", ".join([p for p in data['players']])
		for playerId in data['players']:
			if playerId not in self.displayMap.players:
				self.addPlayer(playerId)
		for playerId in self.displayMap.players.keys():
			if playerId not in data['players']:
				#del self.players[player]
				self.delPlayer(playerId)
	'''
	def Network_player_enter_map(self, data):
		id = data["id"]
		x = data['x']
		y = data['y']
		dx = data['dx']
		dy = data['dy']
		self.displayMap.addPlayer(id, x, y)
		self.displayMap.players[id].setMovement(dx, dy)
		print "Player %s entered the map" % (id)
		
	def Network_player_leave_map(self, data):
		id = data["id"]
		self.displayMap.delPlayer(id)
		print "Player %s left the map" % (id)
		
	
	def Network_player_update_move(self, data):
		id = data['id']
		if id == self.id:
			# if we're not connected yet
			if self.id not in self.displayMap.players:
				self.addPlayer(self.id, data['x'], data['y'])
				print("Looks like we're on the map now...")
			else:
				if getDist(self.displayMap.players[self.id].mapRect, pygame.Rect((data['x'], data['y'],0,0)))>16.0:
					self.displayMap.players[self.id].setPos(data['x'], data['y'])
			
			return
		
		x = data['x']
		y = data['y']
		dx = data['dx']
		dy = data['dy']
		if id in self.displayMap.players:
			self.displayMap.players[id].setPos(x, y)
			self.displayMap.players[id].setMovement(dx, dy)
			#print "updated other player pos : %s, %s/%s" % (name, x, y)
		else:
			self.addPlayer(id, x, y)
			self.displayMap.players[id].setMovement(dx, dy)
			
		#print "received move_update from server : %s is now at %s / %s, and going in %s / %s" % (id, x, y, dx, dy)
	
	def Network_mob_leave_map(self, data):
		id = data["id"]
		self.displayMap.delMob(id)
		print "Mob %s left the map" % (id)
		
	def Network_mob_update_move(self, data):
		id = data['id']
		if id == self.id:# why don't i feel confident this would never happen?
			print("Something totally weird just happened, i think you're a mob.")
			return
			
		x = data['x']
		y = data['y']
		dx = data['dx']
		dy = data['dy']
		if id in self.displayMap.mobs:
			self.displayMap.mobs[id].setPos(x, y)
			self.displayMap.mobs[id].setMovement(dx, dy)
			#print "known mob pos : %s, %s/%s, %s/%s" % (id, x, y, dx, dy)
		else:
			self.addMob(id, x, y)
			self.displayMap.mobs[id].setMovement(dx, dy)
			#print "mob spotted at %s %s , moving : %s %s" % (x, y, dx, dy)
		#print "received MOB_move_update from server : %s is now at %s / %s, and going in %s / %s" % (id, x, y, dx, dy)
		
	def Network_warp(self, data):
		mapFileName = data['mapFileName']
		x = data['x']
		y = data['y']
		print "Warping to %s , %s, %s" % (mapFileName, x, y)
		self.setMap(mapFileName, x, y)
	
	
	#-------------------------------------------------------------------
	# chat
	
	def Network_public_message(self, data):
		print data['id'] + ": " + data['message']
		msg = "<" + data['id'] + "> " + data['message'].decode('utf-8')
		self.gui.chatWindow.addText(msg)
		if data['id'] in self.displayMap.players:
			self.displayMap.players[data['id']]._sprite.setTalk(data['message'].decode('utf-8'))
		else:
			print "received message from %s but not in map" % (data['id'])
		#self.chatWindow.addText(data['message'].decode('utf-8'))
		
	def Network_private_message(self, data):
		print data['id'] + "(prv): " + data['message']
		msg = "<" + data['id'] + " (prv)> " + data['message'].decode('utf-8')
		self.gui.chatWindow.addText(msg)
		
	def Network_emote(self, data):
		playerId = data['id']
		emote = data['emote']
		self.displayMap.players[playerId]._sprite.setEmote(emote)	
	
	# built in stuff

	def Network_connected(self, data):
		print "You are now connected to the server"
	
	def Network_error(self, data):
		print 'error:', data['error'][1]
		connection.Close()
	
	def Network_disconnected(self, data):
		print 'Server disconnected'
		exit()

	
'''
if len(sys.argv) != 2:
	print "Usage:", sys.argv[0], "host:port"
	print "e.g.", sys.argv[0], "localhost:31425"
else:
	host, port = sys.argv[1].split(":")
	c = Client(host, int(port))
	while 1:
		c.Loop()
		sleep(0.001)
'''
