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
from guiColorPicker import ColorPicker

class CharCreationWindow(Window):
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
		
		Window.__init__(self, "Character Creation", width, height, bgcolor, bordercolor, hoverbordercolor, borderwidth, parent, gui)
		
		ColorPicker(rotated = True, bgcolor = bgcolor, parent = self).setPadding(10)
		
		self.autolayout(offset=(0, 30))
