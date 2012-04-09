#!/usr/bin/python
# -*- coding: utf8 -*-

import pygame
import sys
import math
import re
import string

pygame.font.init()
FONT =  pygame.font.Font("fonts/Verdana.ttf", 12)
FONT2 = pygame.font.Font("fonts/Verdana.ttf", 16)
FONT_MANGA = pygame.font.Font("fonts/mangat.ttf", 28)

BGCOLOR = (0,0,0)
TEXTCOLOR = (200,200,200)
BORDERCOLOR = TEXTCOLOR
TEXTCOLORHOVER = (255,255,255)

COLOR = (200,200,200)
COLOR_HOVER = (255,255,255)
COLOR_BG = (50,50,50)
COLOR_BG_HOVER = (80,80,80)

MIN_CARRET_SIZE = 5
CARRET_WIDTH = 20

ImgDB = {}
pathList = []
#gui elements
pathList.append("graphics/gui/guibase.png")
pathList.append("graphics/gui/emotes.png")
pathList.append("graphics/gui/progressbars.png")

#ingame sprites
pathList.append("graphics/sprites/player/male.png")
pathList.append("graphics/sprites/player/female.png")
pathList.append("graphics/sprites/mobs/monsters01.png")
pathList.append("graphics/sprites/hair/male_hair1.png")
pathList.append("graphics/sprites/clothes/armor1.png")

for imgPath in pathList:
	try:
		ImgDB[imgPath] = pygame.image.load(imgPath).convert_alpha()
	except:
		ImgDB[imgPath] = pygame.image.load(imgPath)

def coupeMsg(msg, longueur, font=FONT):
	msg = msg.replace("\n", " ")
	wordsToAdd = msg.strip().split(" ")
	#print "words to add : %s" % (wordsToAdd)
	lines = []
	currentLine = ""
	lastGoodLine = ""
	for word in wordsToAdd:
		currentLine += " " + word
		if font.size(currentLine)[0]>= longueur:
			lastGoodLine = lastGoodLine.strip()
			lines.append(lastGoodLine)
			currentLine = word
			
		else:
			lastGoodLine = currentLine
	lines.append(lastGoodLine)
	return lines

def ustr(o):
	"""This function is like 'str', except that it can return unicode as well"""
	if isinstance(o, unicode):
		o.encode("utf-8")
		return o
	#if isinstance(o, basestring):
	#	return o.value()
	return unicode(str(o.encode("utf-8")))


def bound(value, minvalue, maxvalue):
	"""returns a value which is between minvalue <= value <= maxvalue"""
	return max(minvalue, min(maxvalue, value))

def renderText(msg, font = FONT, aa=False, color = COLOR):
	#img = font.render(msg, False, color)
	#return img
	return font.render(msg, aa, color)
	
	
