#!/usr/bin/python
# -*- coding: utf8 -*-

import sys
from time import sleep

from PodSixNet.Connection import connection, ConnectionListener
from gui import ustr
from gameEngine import *

class GameClient(ConnectionListener):
	def __init__(self, host, port):
		self.Connect((host, port))
		#print "ariclient started"
		
	def Loop(self):
		connection.Pump()
		self.Pump()
	
	def SendLogin(self, name, password):
		print "GameClient : sent login %s %s" % (name, password)
		connection.Send({"action": "login", "id":name, "password" : password})
	
	def SendRegister(self, name, password):
		print "GameClient : sent register %s %s" % (name, password)
		connection.Send({"action": "register", "id":name, "password" : password})
	
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
		
	def SendSitRequest(self):
		connection.Send({"action": "sit_request"})
		
	def SendEmote(self, emote):
		connection.Send({"action": "emote", "emote" : emote})
		
	def SendWarpRequest(self, mapName, x, y):
		connection.Send({"action": "warp_request", "mapName":mapName, "x":x, "y":y})
		
	def SendWarpInfoRequest(self):
		connection.Send({"action": "warp_info_request"})
		
	#######################################
	### Network event/message callbacks ###
	#######################################
	
	#-------------------------------------------------------------------
	# on client receive from server :
	#-------------------------------------------------------------------
	
	def Network_login_error(self, data):
		msg = data["msg"]
		print "Login error : %s" % (msg)
		self.loginGui.infoLabel.setText(msg)
		
	def Network_login_accepted(self, data):
		self.loginGui.running = False
		mapFileName = data["mapFileName"]
		print "Login accepted, entering map : %s" % (mapFileName)
		x = data["x"]
		y = data["y"]
		self.setMap(mapFileName, x, y)
		#self.gui.loginScreen.infoLabel.setText(msg)
		
	def Network_register_error(self, data):
		msg = data["msg"]
		print "Register error : %s" % (msg)
		self.loginGui.infoLabel.setText(msg)
		
	def Network_register_accepted(self, data):
		msg = data["msg"]
		print "Register accepted"
		self.loginGui.infoLabel.setText(msg)
		
		#self.gui.loginScreen.infoLabel.setText(msg)
			
	def Network_warp_info(self, data):
		name = data['name']
		x = data['x']
		y = data['y']
		w = data['w']
		h = data['h']
		self.displayMap.addWarp(name, x, y, w, h)
		print "received warp info for %s" % (name)
		
	def Network_player_enter_map(self, data):
		name = data["id"]
		x = data['x']
		y = data['y']
		dx = data['dx']
		dy = data['dy']
		self.displayMap.addPlayer(name, x, y)
		self.displayMap.players[name].setMovement(dx, dy)
		print "Player %s entered the map" % (name)
		
	def Network_player_leave_map(self, data):
		name = data["id"]
		self.displayMap.delPlayer(name)
		print "Player %s left the map" % (name)
		
	
	def Network_player_update_move(self, data):
		name = data['id']
		if name == self.name:
			# if we're not connected yet
			if self.name not in self.displayMap.players:
				self.addPlayer(self.name, data['x'], data['y'])
				print("Looks like we're on the map now...")
			#else:
				#d= getDist(self.displayMap.players[self.id].mapRect, pygame.Rect((data['x'], data['y'],0,0)))
				#if d>16.0:
				#	self.displayMap.players[self.id].setPos(data['x'], data['y'])
				#	print "server corrected our location"
			#	else:
			#		print "on update move, server sees me at %s pixels from where i am" % (d)
			return
		
		x = data['x']
		y = data['y']
		dx = data['dx']
		dy = data['dy']
		if name in self.displayMap.players:
			self.displayMap.players[name].setPos(x, y)
			self.displayMap.players[name].setMovement(dx, dy)
			#print "updated other player pos : %s, %s/%s" % (name, x, y)
		else:
			self.addPlayer(name, x, y)
			self.displayMap.players[name].setMovement(dx, dy)
			
		#print "received move_update from server : %s is now at %s / %s, and going in %s / %s" % (id, x, y, dx, dy)
	
	def Network_player_sit(self, data):
		playerName = data["name"]
		x = data["x"]
		y = data["y"]
		dx = data["dx"]
		dy = data["dy"]
		self.displayMap.players[playerName].setPos(x, y)
		currentAnim = self.displayMap.players[playerName]._sprite.currentAnim
		if "walk" in currentAnim:
			currentAnim = currentAnim.replace("walk", "sit")
		elif "idle" in currentAnim:
			currentAnim = currentAnim.replace("idle", "sit")
		self.displayMap.players[playerName]._sprite.setAnim(currentAnim)
		
	def Network_mob_leave_map(self, data):
		name = data["id"]
		self.displayMap.delMob(name)
		print "Mob %s left the map" % (name)
		if self.displayMap.selected == name:
			self.displayMap.unselectTarget()
			
	def Network_mob_took_damage(self, data):
		mobName = data["id"]
		if mobName not in self.displayMap.mobs:
			return
		dmg = data["dmg"]
		
		#print "Mob %s took %s damage points" % (mobName, dmg)
		x, y = self.displayMap.mobs[mobName].mapRect.topleft
		y -= self.displayMap.mobs[mobName]._sprite.rect.h
		x -= self.displayMap.mobs[mobName]._sprite.rect.w
		
		self.displayMap.particleManager.addParticle("damage", x, y, str(dmg))
		
	def Network_mob_update_move(self, data):
		name = data['id']
		if name == self.name:# why don't i feel confident this would never happen?
			print("Something totally weird just happened, i think you're a mob.")
			return
		
		x = data['x']
		y = data['y']
		dx = data['dx']
		dy = data['dy']
		if name not in self.displayMap.mobs:
			self.addMob(name, x, y)
		self.displayMap.mobs[name].setPos(x, y)
		self.displayMap.mobs[name].setMovement(dx, dy)
		self.displayMap.mobs[name].update(1)
		
	def Network_warp(self, data):
		#print "received warp message"
		mapFileName = data['mapFileName']
		x = data['x']
		y = data['y']
		player = self.displayMap.players[self.name]
		w = self.displayMap.tileWidth
		h = self.displayMap.tileHeight
		
		print "Player in %s / %s (tile %s / %s), warping to %s , %s, %s" % (player.x, player.y, int(player.x / w), int(player.y / h), mapFileName, x, y)
		self.setMap(mapFileName, x, y)
		
	
	#-------------------------------------------------------------------
	# chat
	
	def Network_public_message(self, data):
		print data['id'] + ": " + data['message']
		msg = "<" + data['id'] + "> " + data['message'].decode('utf-8')
		self.gameGui.chatWindow.addText(msg)
		if data['id'] in self.displayMap.players:
			self.displayMap.players[data['id']]._sprite.setTalk(data['message'].decode('utf-8'))
		else:
			print "received message from %s but not in map" % (data['id'])
			self.addPlayer(data['id'], 80, 80)
		#self.chatWindow.addText(data['message'].decode('utf-8'))
		
	def Network_private_message(self, data):
		print data['id'] + "(prv): " + data['message']
		msg = "<" + data['id'] + " (prv)> " + data['message'].decode('utf-8')
		self.gameGui.chatWindow.addText(msg)
		
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
		sys.exit()
