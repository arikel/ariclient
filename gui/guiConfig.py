#!/usr/bin/python
# -*- coding: utf8 -*-

import pygame
from guiFunctions import *
from guiFrame import Frame
from guiWindow import Window
from guiLayout import BaseLayouter
from guiButton import AbstractButton
from guiLabel import Label
from guiEntry import TextEntry
from guiWidget import Widget

#class CloseButton(AbstractButton):

class ConfigWindow(Window):
	def __init__(self,
		x,y,
		width = 400,
		height = 300,
		bgcolor = (86,111,175),
		bordercolor = (200,200,200),
		hoverbordercolor = (255,255,255),
		borderwidth = 1,
		parent=None,
		gui = None):
		
		Window.__init__(self, "Configuration", width, height, bgcolor, bordercolor, hoverbordercolor, borderwidth, parent, gui)
		#print "created config window, self.surface = %s" % (self.surface)
		
		Label('Keys', parent=self).setPadding(5)
		Frame(0,50, parent=self)
		Label('Up', parent=self).setPadding(5)
		self.kup = TextEntry('', parent=self)
		self.kup.setPadding(5)
		Label('Down', parent=self).setPadding(5)
		self.kdown = TextEntry('', parent=self)
		self.kdown.setPadding(5)
		Label('Left', parent=self).setPadding(5)
		self.kleft = TextEntry('', parent=self)
		self.kleft.setPadding(5)
		Label('Right', parent=self).setPadding(5)
		self.kright = TextEntry('', parent=self)
		self.kright.setPadding(5)
		Label('Select', parent=self).setPadding(5)
		self.kselect = TextEntry('', parent=self)
		self.kselect.setPadding(5)
		Label('Attack', parent=self).setPadding(5)
		self.kattack = TextEntry('', parent=self)
		self.kattack.setPadding(5)
		
		self.autolayout(offset = (0, 20), griditems=2)
		self.setPos(x,y)
		self.OnResize(1,1)
		self.hide()

	def handleEvents(self, events=[]):
		#seems slow
		for event in filter(lambda x: x.type == pygame.MOUSEBUTTONDOWN and x.button == 1, events):
			for widget in [self.kup, self.kdown, self.kleft, self.kright, self.kselect, self.kattack]:
				if widget.hover:
					widget.getFocus()
				else:
					widget.loseFocus()
								
		Window.handleEvents(self, events)
