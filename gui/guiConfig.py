#!/usr/bin/python
# -*- coding: utf8 -*-

import pygame
from guiFunctions import *
from guiFrame import Frame
from guiLayout import BaseLayouter
from guiButton import AbstractButton
from guiLabel import Label
from guiEntry import TextEntry
from guiWidget import Widget

#class CloseButton(AbstractButton):

class ConfigWindow(Frame):
	def __init__(self,
		x,y,
		width = 400,
		height = 300,
		bgcolor = (86,111,175),
		bordercolor = (200,200,200),
		hoverbordercolor = (255,255,255),
		borderwidth = 1,
		parent=None):
		
		Frame.__init__(self, width, height, bgcolor, bordercolor, hoverbordercolor, borderwidth, parent)
		self.updateSurface()
		self.setPos(x,y)
		baselayout = BaseLayouter('vertical', self)
		cols = [BaseLayouter(parent=baselayout), Widget(height=50,parent=baselayout), BaseLayouter(parent=baselayout), BaseLayouter(parent=baselayout), BaseLayouter(parent=baselayout), BaseLayouter(parent=baselayout)]
		for col in cols:
			baselayout.add(col)
			
		cols[0].add(Label('Keys', parent=self), 5)
		
		cols[2].add(Label('Up', parent=self), 5)
		cols[2].add(TextEntry('', parent=self), 5)
		cols[3].add(Label('Down', parent=self), 5)
		cols[3].add(TextEntry('', parent=self), 5)
		cols[4].add(Label('Left', parent=self), 5)
		cols[4].add(TextEntry('', parent=self), 5)
		cols[5].add(Label('Right', parent=self), 5)
		cols[5].add(TextEntry('', parent=self), 5)
		
		
		baselayout.fit()
		
		self.hide()
		
	
		
		
