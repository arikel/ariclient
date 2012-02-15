#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from xml.dom import minidom, Node
import base64
import gzip
import StringIO
import os.path
import pygame

#-------------------------------------------------------------------------------
def decode_base64(in_str):
	return base64.decodestring(in_str)

def encode_base64(in_str):
	return base64.encodestring(in_str)
	
def decompress_gzip(in_str):
	compressed_stream = StringIO.StringIO(in_str)
	gzipper = gzip.GzipFile(fileobj=compressed_stream)
	return gzipper.read()
	
def compress_gzip(in_str):
	compressed_stream = StringIO.StringIO()
	gzipper = gzip.GzipFile(fileobj=compressed_stream, mode="wb")
	gzipper.write(in_str)
	gzipper.close()
	return compressed_stream.getvalue()
	
def getCode(val):
	code = chr(int(val & 255))
	code = code + chr(int((val>>8) & 255))
	code = code + chr(int((val>>16) & 255))
	code = code + chr(int((val>>24) & 255))
	return code
	
def decode(encoded_content):
	s = encoded_content
	if encoded_content:
		s = decode_base64(s)
		s = decompress_gzip(s)
	#print "Content after decode and decompress : %s" % (s)
	decoded_content = []
	for idx in xrange(0, len(s), 4):
		val = ord(str(s[idx])) | (ord(str(s[idx + 1])) << 8) | \
			 (ord(str(s[idx + 2])) << 16) | (ord(str(s[idx + 3])) << 24)
		decoded_content.append(val)
	return decoded_content
	
def encode(content_list):
	"Encodes an array of ints corresponding to tiles id"
	coded_content = ""
	for n in content_list:
		coded_content = coded_content + getCode(n)
	coded_content = compress_gzip(coded_content)
	coded_content = encode_base64(coded_content)
	return coded_content
	
class Tileset(object):
	def __init__(self, name, tileWidth, tileHeight, firstgid, source):
		self.name = name
		self.tileWidth = int(tileWidth)
		self.tileHeight = int(tileHeight)
		self.firstgid = int(firstgid)
		self.imageSource = source
		self.load()
		
	def load(self):
		self.image = pygame.image.load(self.imageSource).convert_alpha()
		self.frames = {}
		self.width = self.image.get_width()
		self.height = self.image.get_height()
		
		self.nbLines = self.height / self.tileHeight
		self.nbCols = self.width / self.tileWidth
		
		nb = self.firstgid
		for y in range(self.nbLines):
			for x in range(self.nbCols):
				rect = (x*self.tileWidth, y*self.tileHeight, self.tileWidth, self.tileHeight)
				img = self.image.subsurface(rect)
				self.frames[nb] = img
				nb = nb + 1
				
				
class TileLayer(object):
	def __init__(self, name, width, height, data = []):
		self.name = name
		self.width = width
		self.height = height
		self.data = data
		#self.tiles = [] # [x][y] -> gid
		self.clearTiles()
		self.makeTiles()
		
	def clearTiles(self):
		self.tiles = []
		for x in range(self.width):
			col = []
			for y in range(self.height):
				col.append(0)
			self.tiles.append(col)
	
	def makeTiles(self):
		X = 0
		Y = 0
		for gid in self.data:
			#if gid != 0:
			self.tiles[X][Y]=gid
			X += 1
			if X == self.width:
				X = 0
				Y += 1

#-------------------------------------------------------------------------------
class TmxMapData(object):
	def __init__(self):
		self.myMap = None
		
		
	def load(self, filename):
		self.myMap = self.parseMap(filename)
		self.width = int(self.myMap.getAttribute("width"))
		self.height = int(self.myMap.getAttribute("height"))
		self.tileWidth = int(self.myMap.getAttribute("tilewidth"))
		self.tileHeight = int(self.myMap.getAttribute("tileheight"))
		
		self.tilesets = self.getTilesets(self.myMap)
		
		self.frames = {} # gid : img frame
		self.offsets = {} # gid : Y tile offset
		self.maxTileWidth = 0
		self.maxTileHeight = 0
		for t in self.tilesets:
			if t.tileWidth > self.maxTileWidth : self.maxTileWidth = t.tileWidth
			if t.tileHeight > self.maxTileHeight : self.maxTileHeight = t.tileHeight
			self.frames.update(t.frames)
			offset = t.tileHeight - self.tileHeight
			for nb in t.frames:
				self.offsets[nb] = offset
				#print "gid %s, offset %s" % (nb, offset)
		#del self.tilesets # all images are now in self.frames
		
		self.layerImageWidth = self.width * self.tileWidth
		self.layerImageHeight = self.height * self.tileHeight
		
		
	def getChildNodes(self, node, name):
		children = []
		for child in node.childNodes:
			if (child.nodeType == Node.ELEMENT_NODE and child.nodeName == name):
				children.append(child)
		return children

	def parseMap(self, filename):# return map node
		dom = minidom.parseString(open(filename, "rb").read())
		for node in self.getChildNodes(dom, "map"):
			return node
		return None
		
	def getTilesets(self, myMap):
		tilesets = []
		for node in self.getChildNodes(self.myMap, "tileset"):
			name = node.getAttribute("name")
			width = node.getAttribute("tilewidth")
			height = node.getAttribute("tileheight")
			firstgid = node.getAttribute("firstgid")
			for child in self.getChildNodes(node, "image"):
				source = child.getAttribute("source")
				# poor hack to fix the image path found in tmx files :
				source = source.replace("../", "")
			#print "name : %s, W : %s, H : %s, gid : %s" % (name, width, height, firstgid)
			tileset = Tileset(name, width, height, firstgid, source)
			
			tilesets.append(tileset)
		return tilesets
		
	def getLayerNames(self):
		data = []
		layers = self.getChildNodes(self.myMap, "layer")
		for layer in layers:
			name = layer.getAttribute("name")
			data.append(name)
		return data

	def getLayerData(self, layername):
		layers = self.getChildNodes(self.myMap, "layer")
		for layer in layers:
			name = layer.getAttribute("name")
			if name == layername:
				layerData = self.getChildNodes(layer, "data")
				return layerData[0].childNodes[0]._get_data()
		return None

	def getLayerDataDic(self, layername):
		data = {}
		layers = self.getChildNodes(self.myMap, "layer")
		for layer in layers:
			name = layer.getAttribute("name")
			if name == layername:
				layerData = self.getChildNodes(layer, "data")
				#data.append(layerData[0].childNodes[0]._get_data())
				data[layername] = layerData[0].childNodes[0]._get_data()
		return data
