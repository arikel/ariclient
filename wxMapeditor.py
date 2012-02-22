#!/usr/bin/python
# -*- coding: utf-8 -*-

# wxMapeditor.py

import wx
import os
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


if __name__ == "__main__":
	app = wx.App()
	frame = SimpleFrame()
	frame.Show()
	app.MainLoop()
	
