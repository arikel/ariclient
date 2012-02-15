#!/usr/bin/python
# -*- coding: utf-8 -*-
import pygame
from sprite import BaseSprite
from mapHandler import Map
from gui import *
from utils import KeyHandler


	
if __name__=="__main__":
	screen = pygame.display.set_mode((640,480))
	
	s = ScrollTextWindow(0,380,640,80)
	msg = u"""1.Ok, on va voir ça
	est-ce qu'on garde les tabs aussi?
	Et les accents, c'est autorisé?
	
	2.Oui puis alors tu vois on peut aussi coller de longues phrases comme ça, qui devraient être coupées à un moment...
	Oui puis alors tu vois on peut aussi coller de longues phrases comme ça, qui devraient être coupées à un moment... Oui puis alors tu vois on peut aussi coller de longues phrases comme ça, qui devraient être coupées à un moment... Oui puis alors tu vois on peut aussi coller de longues phrases comme ça, qui devraient être coupées à un moment...
	
	3.Oui puis alors tu vois on peut aussi coller de longues phrases comme ça, qui devraient être coupées à un moment... Oui puis alors tu vois on peut aussi coller de longues phrases comme ça, qui devraient être coupées à un moment...
	
	4.Oui puis alors tu vois on peut aussi coller de longues phrases comme ça, qui devraient être coupées à un moment...
	5.Oui puis alors tu vois on peut aussi coller de longues phrases comme ça, qui devraient être coupées à un moment... Oui puis alors tu vois on peut aussi coller de longues phrases comme ça, qui devraient être coupées à un moment... Oui puis alors tu vois on peut aussi coller de longues phrases comme ça, qui devraient être coupées à un moment...
	
	6.Oui puis alors tu vois on peut aussi coller de longues phrases comme ça, qui devraient être coupées à un moment...
	
	7.END
	
	1.Ok, on va voir ça
	est-ce qu'on garde les tabs aussi?
	Et les accents, c'est autorisé?
	
	2.Oui puis alors tu vois on peut aussi coller de longues phrases comme ça, qui devraient être coupées à un moment...
	Oui puis alors tu vois on peut aussi coller de longues phrases comme ça, qui devraient être coupées à un moment... Oui puis alors tu vois on peut aussi coller de longues phrases comme ça, qui devraient être coupées à un moment... Oui puis alors tu vois on peut aussi coller de longues phrases comme ça, qui devraient être coupées à un moment...
	
	3.Oui puis alors tu vois on peut aussi coller de longues phrases comme ça, qui devraient être coupées à un moment... Oui puis alors tu vois on peut aussi coller de longues phrases comme ça, qui devraient être coupées à un moment...
	
	4.Oui puis alors tu vois on peut aussi coller de longues phrases comme ça, qui devraient être coupées à un moment...
	5.Oui puis alors tu vois on peut aussi coller de longues phrases comme ça, qui devraient être coupées à un moment... Oui puis alors tu vois on peut aussi coller de longues phrases comme ça, qui devraient être coupées à un moment... Oui puis alors tu vois on peut aussi coller de longues phrases comme ça, qui devraient être coupées à un moment...
	
	6.Oui puis alors tu vois on peut aussi coller de longues phrases comme ça, qui devraient être coupées à un moment...
	
	7.END
	"""
	
	
	s.setText(msg)
	
	e = TextEntry("")
	e.setPos(5,460)
	
	l = Label("ok")
	l.setPos(80,20)
	
	
	kh = KeyHandler()
	running = True
	while running:
		
		x, y = pygame.mouse.get_pos()
		
		events = kh.getEvents()
		if kh.keyDict[pygame.K_ESCAPE]:
			running = False
		res = e.handleInput(events)
		if res:
			s.addText(res)
			
		s.handleEvents(x, y, events)
				
		screen.fill((150,150,150))
		s.updateSurface(x,y)
		s.blit(screen)
		msg = "" + str(s.currentPos)
		l.setText(msg)
		l.blit(screen)
		e.updateSurface()
		e.blit(screen)
		
		pygame.display.flip()
	pygame.quit()
	
