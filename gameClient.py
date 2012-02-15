#!/usr/bin/python
# -*- coding: utf8 -*-

import sys
from time import sleep
from sys import stdin, exit

from PodSixNet.Connection import connection, ConnectionListener
from guiFunctions import ustr
from gameEngine import *

class Client(ConnectionListener):
	def __init__(self, host, port):
		self.Connect((host, port))
		print "Chat client started"
		print "Ctrl-C to exit"
		# get a nickname from the user before starting
		print "Enter your nickname: ",
		self.name = stdin.readline().rstrip("\n")
		
		connection.Send({"action": "nickname", "nickname": self.name})
	
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
		
		
	def SendPosition(self):
		connection.Send({"action": "position", "message":"ok :(", "x":self.sprite.mapRect.x, "y":self.sprite.mapRect.y, "who":self.name})
		
	def SendUpdateMove(self):
		connection.Send({"action": "update_move", "message":" ", "x":self.sprite.mapRect.x, "y":self.sprite.mapRect.y, "who":self.name})
		
	def SendLogin(self, password):
		connection.Send({"action": "login", "message": " ", "name":self.name, "password" : password})
		
	#######################################
	### Network event/message callbacks ###
	#######################################
	
	#-------------------------------------------------------------------
	# on client receive from server self.nickname :
	#-------------------------------------------------------------------
	
	def Network_players(self, data):
		print "*** players: " + ", ".join([p for p in data['players']])
		for player in data['players']:
			if player not in self.players:
				self.addPlayer(player)
		for player in self.players.keys():
			if player not in data['players']:
				del self.players[player]
				
	def Network_message(self, data):
		print data['who'] + ": " + data['message']
		self.chatWindow.addText(data['message'])
		
	def Network_public_message(self, data):
		print data['who'] + ": " + data['message']
		self.chatWindow.addText(data['message'].decode('utf-8'))
		
	def Network_private_message(self, data):
		print data['who'] + "(prv): " + data['message']
		
	def Network_position(self, data):
		#print "received position msg : " + data['who'] + ": " + data['message']
		#print "received pos : data = %s" % (data)
		name = data['who']
		x = data['x']
		y = data['y']
		
		if name in self.players:
			self.players[name].setPos(x, y)
			#print "updated other player pos : %s, %s/%s" % (name, x, y)
		elif name != self.name:
			self.addPlayer(name)
			self.players[name].setPos(x, y)
		
	
			
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
