#!/usr/bin/python
# -*- coding: utf8 -*-

import pygame

class KeyHandler(object):
	def __init__(self):
		self.keyDict = {}
		keyList = [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_ESCAPE,
			pygame.K_z, pygame.K_s, pygame.K_q, pygame.K_d, pygame.K_SPACE, pygame.K_RETURN]
		for key in keyList:
			self.keyDict[key] = 0
	'''
	def setKey(self, key, value):
		self.keyDict[key] = value
	'''
	def getEvents(self):
		events = pygame.event.get()
		for event in events:
			if event.type == pygame.KEYDOWN:
				self.keyDict[event.key] = 1
			elif event.type == pygame.KEYUP:
				self.keyDict[event.key] = 0
		return events
