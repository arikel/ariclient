#!/usr/bin/python
# -*- coding: utf-8 -*-

# wxMapeditor.py

import wx
import os
import pygame
import mapeditor
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
	
	draw = False
	dragOriginX = 0
	dragOriginY = 0
	
	def __init__(self, parent, refreshRate=60):
		wx.Panel.__init__(self, parent, -1, size = wx.Size(640,480))
		self.timer = wx.Timer(self, -1)
		self.refreshRate = refreshRate
		#self.timer.Start(refreshRate)

		pygame.init()
		self.screen = pygame.Surface((640,480))

		self.map = mapeditor.MapEditor(self.screen)
		self.map.new(80,60)

		self.Bind(wx.EVT_PAINT, self.OnPaint)
		self.Bind(wx.EVT_TIMER, self.OnUpdate, self.timer)
		self.Bind(wx.EVT_ENTER_WINDOW, self.OnMouseEnter)
		self.Bind(wx.EVT_LEAVE_WINDOW, self.OnMouseLeave)
		self.Bind(wx.EVT_LEFT_DOWN, self.OnStartDraw)
		self.Bind(wx.EVT_MOTION, self.OnMouseMove)
		self.Bind(wx.EVT_LEFT_UP, self.OnStopDraw)
		
		self.Update()


	def OnPaint(self, evt):
		#skips exceptions (like initialized before the main App)
		try:
			s = pygame.image.tostring(self.screen, 'RGB')  # Convert the surface to an RGB string
			img = wx.ImageFromData(640, 480, s)  # Load this string into a wx image
			bmp = wx.BitmapFromImage(img)  # Get the image in bitmap form
			dc = wx.BufferedPaintDC(self)  # Device context for drawing the bitmap
			dc.DrawBitmap(bmp, 0, 0, False)  # Blit the bitmap image to the display
			del dc
		except:
			pass

	def Update(self):
		self.screen.fill((0,0,0))
		self.map.blit(self.screen)
		
	def OnUpdate(self, evt):
		self.screen.fill((0,0,0))
		self.map.blit(self.screen)
		self.Refresh()

	def OnMouseEnter(self, evt):
		pass
		
	def OnMouseLeave(self, evt):
		if self.draw:
			self.draw = False
			self.timer.Stop()
		
	def OnStartDraw(self, evt):
		self.draw = True
		self.timer.Start(self.refreshRate)
		#self.map.startDrag()
		
	def OnMouseMove(self, evt):
		if self.draw:
			tx, ty = self.map.getMouseTilePos(evt.m_x, evt.m_y)
			self.map.drawTile(self.map.currentLayer, tx, ty)
		
	def OnStopDraw(self, evt):
		self.draw = False
		self.timer.Stop()
		#self.map.stopDrag()




if __name__ == "__main__":
	app = wx.App()
	frame = SimpleFrame()
	frame.Show()
	app.MainLoop()
