#!/usr/bin/python
# -*- coding: utf-8 -*-

# wxMapeditor.py

import wx
import os
import pygame
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

		
		
class TestPanel(wx.Panel):
	def __init__(self, parent, refreshRate=500):
		wx.Panel.__init__(self, parent, -1, size = wx.Size(640,480))
		self.timer = wx.Timer(self, -1)
		self.timer.Start(refreshRate)

		pygame.init()
		self.screen = pygame.Surface((640,480))
		white = pygame.Color(255, 120, 140, 255)
		rect = pygame.Rect(10, 10, 100, 100)
		pygame.draw.rect(self.screen, white, rect)

		self.Bind(wx.EVT_PAINT, self.OnPaint)
		self.Bind(wx.EVT_TIMER, self.OnUpdate, self.timer)


	def OnPaint(self, evt):
		#skips exceptions (like initialized before the main App)
		try:
			s = pygame.image.tostring(self.screen, 'RGB')  # Convert the surface to an RGB string
			img = wx.ImageFromData(640, 480, s)  # Load this string into a wx image
			#dc = wx.PaintDC(self)
			bmp = wx.BitmapFromImage(img)  # Get the image in bitmap form
			dc = wx.PaintDC(self)  # Device context for drawing the bitmap
			dc.DrawBitmap(bmp, 0, 0, False)  # Blit the bitmap image to the display
			del dc
		except:
			pass

        def OnUpdate(self, evt):
                self.Refresh()




if __name__ == "__main__":
	app = wx.App()
	frame = SimpleFrame()
	frame.Show()
	app.MainLoop()
