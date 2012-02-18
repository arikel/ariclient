#!/usr/bin/python
# -*- coding: utf8 -*-

import pygame
from config import CONTROL_KEY_LIST

class KeyHandler(object):
	def __init__(self):
		self.keyDict = {}
		#keyList = [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_ESCAPE,
		#	pygame.K_z, pygame.K_s, pygame.K_q, pygame.K_d, pygame.K_SPACE, pygame.K_RETURN]
		for key in CONTROL_KEY_LIST:
			self.keyDict[key] = 0
	
	def getEvents(self):
		events = pygame.event.get()
		for event in events:
			if event.type == pygame.KEYDOWN:
				self.keyDict[event.key] = 1
			elif event.type == pygame.KEYUP:
				self.keyDict[event.key] = 0
		return events
