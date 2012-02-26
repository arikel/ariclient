#!/usr/bin/python
# -*- coding: utf-8 -*-

# wxMapeditor.py

import wx
import os, sys
import pygame
from utils import KeyHandler
import thread
# warning, in wx, a frame is a window, a window is a frame.

class SimpleFrame(wx.Frame):	
	def __init__(self):
		wx.Frame.__init__(self, None, -1, "ariclient map editor", size=(800,600))
		
		#Creation of the Menu with two items, about ans quit
		menubar = wx.MenuBar()
		
		fileMenu = wx.Menu()
		OpenMn = fileMenu.Append(wx.ID_OPEN, '&Open', 'Open a map')
		fileMenu.AppendSeparator()
		QuitMn = fileMenu.Append(wx.ID_EXIT, '&Quit', 'Quit application')
		
		aboutMenu = wx.Menu()
		AboutMn = aboutMenu.Append(wx.ID_ABOUT, '&About', 'About the application')
		
		menubar.Append(fileMenu, '&File')
		menubar.Append(aboutMenu, '&?')
		
		self.SetMenuBar(menubar)
		self.CreateStatusBar()

		self.panel = TestPanel(self)

		sizer = wx.BoxSizer( wx.HORIZONTAL )
		sizer.Add( self.panel, 0, wx.ALL, 5 )
		self.SetSizer( sizer )
		
		
		#Binds the two items to the correct funcion, AboutBox and Quit application
		self.Bind(wx.EVT_MENU, self.OnOpen, OpenMn)
		self.Bind(wx.EVT_MENU, self.OnQuit, QuitMn)
		
		self.Bind(wx.EVT_MENU, self.OnAbout, AboutMn)
		
	def OnOpen(self, event):
		self.dirname = ''
		dlg = wx.FileDialog(self, "Choose a file", self.dirname, "", "*.*", wx.OPEN)
		if dlg.ShowModal() == wx.ID_OK:
			self.filename = dlg.GetFilename()
			self.dirname = dlg.GetDirectory()
			filePath = os.path.join(self.dirname, self.filename)
			
			
		dlg.Destroy()
		
	def OnQuit(self, event):
		self.Close()
		
	def OnAbout(self, event):
		about = wx.AboutDialogInfo()
		about.Name = "ariclient map editor"
		wx.AboutBox(about)
		
		
class PygameThread:
	def __init__(self, screen):
		self.running = False
		self.screen = screen

	def Start(self):
		self.running = True
		thread.start_new_thread(self.Run, ())

	def Stop(self):
		self.running = False

	def IsRunning(self):
		return self.running

	def Run(self):
		m = self.map
		kh = KeyHandler()
		while self.running:
			events = kh.getEvents()
			m.update(events)

		self.running = False
		
	def SetMap(self, map):
		self.map = map

	def NewMap(self, size):
		self.map = mapeditor.MapEditor(self.screen)
		self.map.new(*size)
		
	def LoadMap(self, filename):
		self.map = mapeditor.MapEditor(self.screen)
		self.map.open(filename)
		
		

		
		
class TestPanel(wx.Panel):
	
	draw = False
	dragOriginX = 0
	dragOriginY = 0
	
	def __init__(self, parent, wsize = wx.Size(700,500)):
		wx.Panel.__init__(self, parent, -1, size = wsize)
		
		self.hwnd = self.GetHandle()
		if sys.platform == "win32":
			os.environ['SDL_VIDEODRIVER'] = 'windib'
		os.environ['SDL_WINDOWID'] = str(self.hwnd) #must be before pygame init

		pygame.init()
		import mapeditor #import here since the screen is initialized during import
		self.screen = pygame.display.set_mode(wsize)
		self.pygamethread = PygameThread(self.screen)
		#workaround to use the mapeditor in the thread
		self.map = mapeditor.MapEditor(self.screen)
		self.map.open("maps/testmap.txt")
		self.pygamethread.SetMap(self.map)
		self.pygamethread.Start()

	def __del__(self):
		self.pygamethread.Stop()


if __name__ == "__main__":
	app = wx.App()
	frame = SimpleFrame()
	frame.Show()
	app.MainLoop()
