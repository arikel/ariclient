#!/usr/bin/python
# -*- coding: utf-8 -*-
import pygame

class ConfigManager(object):
	def __init__(self, filename="playersettings.txt"):
		self.filename = filename
		self.keys = {}
		
	def load(self):
		try:
			fp = open(self.filename, "r")
		except:
			self.initConfigFile(self.filename)
			return
		for line in fp:
			key, value = map(lambda x: x.strip(), line.split("="))
			try:
				#may need to check for values < 0 and > 255
				value = int(value)
			except:
				#skipping every param that is not the server address
				if key != 'server-address':
					continue
				
			if key == 'screen-width':
				print "Setting GLOBAL Screen Width : %s" % (value)
				self.keys["SCREEN_WIDTH"] = value
			elif key == 'screen-height':
				print "Setting GLOBAL Screen Height : %s" % (value)
				self.keys["SCREEN_HEIGHT"] = value
			elif key == 'server-address':
				self.keys["SERVER_ADDRESS"] = value
			elif key == 'server-port':
				self.keys["SERVER_PORT"] = value
			elif key == 'key-up':
				self.keys["KEY_UP"] = value
			elif key == 'key-down':
				self.keys["KEY_DOWN"] = value
			elif key == 'key-left':
				self.keys["KEY_LEFT"] = value
			elif key == 'key-right':
				self.keys["KEY_RIGHT"] = value
			elif key == 'key-select':
				self.keys["KEY_SELECT_TARGET"] = value
			elif key == 'key-attack':
				self.keys["KEY_ATTACK"] = value
		fp.close()
		
	def initConfigFile(self, filename):
		print "Invalid configuration... resetting..."
		configdata = [ ('screen-width', 800),\
			('screen-height', 600),\
			('server-address', "88.173.217.230"),\
			('server-port', 18647),\
			('key-up', pygame.K_UP),\
			('key-down', pygame.K_DOWN),\
			('key-left', pygame.K_LEFT),\
			('key-right', pygame.K_RIGHT),\
			('key-select', pygame.K_a),\
			('key-attack', pygame.K_e) 
		]
		
		lines = []
		fp = open(filename, "w")
		for key, value in configdata:
			lines.append("%s = %s\n" % (key, str(value)))
		fp.writelines(lines)
		fp.close()
		self.load()

cm = ConfigManager()
cm.load()

SCREEN_WIDTH = cm.keys["SCREEN_WIDTH"]
SCREEN_HEIGHT = cm.keys["SCREEN_HEIGHT"]

SERVER_ADDRESS = cm.keys["SERVER_ADDRESS"]
SERVER_PORT = cm.keys["SERVER_PORT"]

# controls
KEY_UP = cm.keys["KEY_UP"]
KEY_DOWN = cm.keys["KEY_DOWN"]
KEY_LEFT = cm.keys["KEY_LEFT"]
KEY_RIGHT = cm.keys["KEY_RIGHT"]
KEY_SELECT_TARGET = cm.keys["KEY_SELECT_TARGET"]
KEY_ATTACK = cm.keys["KEY_ATTACK"]

CONTROL_KEY_LIST = [KEY_UP, KEY_DOWN, KEY_LEFT, KEY_RIGHT, KEY_SELECT_TARGET, KEY_ATTACK]


def read_configuration():
	global SCREEN_WIDTH, SCREEN_HEIGHT, SERVER_ADDRESS, SERVER_PORT,\
		   KEY_UP, KEY_DOWN, KEY_LEFT, KEY_RIGHT, KEY_SELECT_TARGET, KEY_ATTACK

	try:
		fp = open("playersettings.txt", "r")
		for line in fp:
			key, value = map(lambda x: x.strip(), line.split("="))
			try:
				#may need to check for values < 0 and > 255
				value = int(value)
			except:
				#skipping every param that is not the server address
				if key != 'server-address':
					continue
				
			if key == 'screen-width':
				print "Setting GLOBAL Screen Width : %s" % (value)
				SCREEN_WIDTH = value
			elif key == 'screen-height':
				print "Setting GLOBAL Screen Height : %s" % (value)
				SCREEN_HEIGHT = value
			elif key == 'server-address':
				SERVER_ADDRESS = value
			elif key == 'server-port':
				SERVER_PORT = value
			elif key == 'key-up':
				KEY_UP = value
			elif key == 'key-down':
				KEY_DOWN = value
			elif key == 'key-left':
				KEY_LEFT = value
			elif key == 'key-right':
				KEY_RIGHT = value
			elif key == 'key-select':
				KEY_SELECT_TARGET = value
			elif key == 'key-attack':
				KEY_ATTACK = value
				
		fp.close()
			
	except Exception, e:
		print "Invalid configuration... resetting..."
		configdata = [ ('screen-width', SCREEN_WIDTH),\
				   ('screen-height', SCREEN_HEIGHT),\
				   ('server-address', SERVER_ADDRESS),\
				   ('server-port', SERVER_PORT),\
				   ('key-up', KEY_UP),\
				   ('key-down', KEY_DOWN),\
				   ('key-left', KEY_LEFT),\
				   ('key-right', KEY_RIGHT),\
				   ('key-select', KEY_SELECT_TARGET),\
				   ('key-attack', KEY_ATTACK) 
				 ]
		try:
			lines = []
			fp = open("playersettings.txt", "w")
			for key, value in configdata:
				lines.append("%s = %s\n" % (key, str(value)))
			fp.writelines(lines)
			fp.close()
		except Exception, e:
			print e
			
	#updates the list...
	CONTROL_KEY_LIST = [KEY_UP, KEY_DOWN, KEY_LEFT, KEY_RIGHT, KEY_SELECT_TARGET, KEY_ATTACK]
	
#def write_configuration():
	
