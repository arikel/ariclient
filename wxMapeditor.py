#!/usr/bin/python
# -*- coding: utf-8 -*-

# wxMapeditor.py

import wx
import os, sys
import pygame
from utils import KeyHandler
import thread

import mapeditor
# warning, in wx, a frame is a window, a window is a frame.

class wxMapEditor(wx.Frame):	
	def __init__(self):
		wx.Frame.__init__(self, None, -1, "ariclient map editor", size=(800,600))
		
		self.__init_menu__()
		
		self.CreateStatusBar()
		
		self.__init_controls__()

	def __init_menu__(self):
		#Creation of the Menu with two items, about ans quit
		menubar = wx.MenuBar()
		
		fileMenu = wx.Menu()
		OpenMn = fileMenu.Append(wx.ID_OPEN, '&Open', 'Open a map')
		SaveMn = fileMenu.Append(wx.ID_SAVE, '&Save', 'Save a map')
		fileMenu.AppendSeparator()
		QuitMn = fileMenu.Append(wx.ID_EXIT, '&Quit', 'Quit application')
		
		aboutMenu = wx.Menu()
		AboutMn = aboutMenu.Append(wx.ID_ABOUT, '&About', 'About the application')
		
		menubar.Append(fileMenu, '&File')
		menubar.Append(aboutMenu, '&?')
		
		self.SetMenuBar(menubar)
		
		#Binds the two items to the correct funcion, AboutBox and Quit application
		self.Bind(wx.EVT_MENU, self.OnOpen, OpenMn)
		self.Bind(wx.EVT_MENU, self.OnSave, SaveMn)
		self.Bind(wx.EVT_MENU, self.OnQuit, QuitMn)
		self.Bind(wx.EVT_MENU, self.OnAbout, AboutMn)
		
	def __init_controls__(self):
		
		self.brushes = wx.TreeCtrl(self, -1, size = wx.Size(100,600))
		self.brushesRoot = self.brushes.AddRoot("Brushes")
		self.brushes.AppendItem(self.brushesRoot, "Grass")
		self.brushes.AppendItem(self.brushesRoot, "Water")		

		self.panel = PygamePanel(self)

		sizer = wx.BoxSizer( wx.HORIZONTAL )
		sizer.Add( self.brushes, 0, wx.ALL, 5 )
		sizer.Add( self.panel, 0, wx.ALL, 5 )
		self.SetSizer( sizer )
		
				
	def OnOpen(self, event):
		self.dirname = ''
		dlg = wx.FileDialog(self, "Open a file...", self.dirname, "", "*.txt", wx.OPEN)
		if dlg.ShowModal() == wx.ID_OK:
			self.filename = dlg.GetFilename()
			self.dirname = dlg.GetDirectory()
			filePath = os.path.join(self.dirname, self.filename)
			print filePath
			self.panel.pygamethread.LoadMap(filePath)
			
			
		dlg.Destroy()
		
	def OnSave(self, event):
		self.dirname = ''
		dlg = wx.FileDialog(self, "Save file as...", self.dirname, "", "*.txt", wx.SAVE)
		if dlg.ShowModal() == wx.ID_OK:
			self.filename = dlg.GetFilename()
			self.dirname = dlg.GetDirectory()
			filePath = os.path.join(self.dirname, self.filename)
			print filePath
			self.panel.pygamethread.SaveMap(filePath)
			
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
		self._wait = False
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
			while self._wait: #lock the update
				pass
			events = kh.getEvents()
			m.update(events)

		self.running = False
		
	def LockUpdate(self):
		self._wait = True
		
	def ReleaseUpdate(self):
		self._wait = False
		
	def SetMap(self, map):
		self.LockUpdate()
		self.map = map
		self.ReleaseUpdate()

	def NewMap(self, size):
		#self.map = mapeditor.MapEditor(self.screen)
		self.LockUpdate()
		self.map.new(*size)
		self.ReleaseUpdate()
		
	def LoadMap(self, filename):
		#self.map = mapeditor.MapEditor(self.screen)
		self.LockUpdate()
		self.map.open(filename)
		self.ReleaseUpdate()
		
	def SaveMap(self, filename):
		self.LockUpdate()
		self.map.save(filename)
		self.ReleaseUpdate()

		
		
class PygamePanel(wx.Panel):
	
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
	frame = wxMapEditor()
	frame.Show()
	app.MainLoop()
