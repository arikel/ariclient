#!/usr/bin/python
# -*- coding: utf8 -*-

import pygame
import sys
import math
import re
import string

pygame.font.init()
FONT =  pygame.font.Font("fonts/Verdana.ttf", 12)
FONT2 =  pygame.font.Font("fonts/Verdana.ttf", 16)

BGCOLOR = (0,0,0)
TEXTCOLOR = (200,200,200)
BORDERCOLOR = TEXTCOLOR
TEXTCOLORHOVER = (255,255,255)

GuiBaseImg = pygame.image.load("graphics/gui/guibase.png")

MIN_CARRET_SIZE = 5
CARRET_WIDTH = 20

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
