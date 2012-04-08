#!/usr/bin/python
# -*- coding: utf-8 -*-
import pygame

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

SERVER_ADDRESS = "88.173.217.230"
#SERVER_ADDRESS = "127.0.0.1"
#SERVER_ADDRESS = "mmorg.dyndns-at-home.com"
SERVER_PORT = 18647

# controls
KEY_UP = pygame.K_UP
KEY_DOWN = pygame.K_DOWN
KEY_LEFT = pygame.K_LEFT
KEY_RIGHT = pygame.K_RIGHT
KEY_SELECT_TARGET = pygame.K_a
KEY_ATTACK = pygame.K_e

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
				SCREEN_WIDTH = value
			elif key == 'screen-height':
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
	
