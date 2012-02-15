#!/usr/bin/python
# -*- coding: utf8 -*-

class Item:
	weight = 0.1
	baseCost = 2
	baseSold = 1
	itemId = 0
	def __init__(self, itemId):
		self.itemId = itemId
		
		
class Inventory:
	
	def __init__(self):
		self.clear()
		
	def clear(self):
		self.items = {}
		
	def addItem(self, itemId, number):
		if itemId in self.items:
			self.items[itemId] += int(number)
		else:
			self.items[itemId] = int(number)
	
	def get(self):
		keys = self.items.keys()
		keys.sort()
		res = ""
		for key in keys:
			res = res + str(key) + "," + str(self.items[key]) + ";"
		return res
		
	def set(self, itemString):
		self.items = {}
		itemString = itemString.strip()
		for elem in split(itemString, ';'):
			item = elem.split(',')
			if len(item)==2:
				self.addItem(item[0].strip(), item[1].strip())

class MapObject:
	def __init__(self, id):
		self.id = id
		# float pixel position on map
		self.category = None
		self.currentMapName = None
		self._map = None
		self.x = 0.0
		self.y = 0.0
		self.mapRect = pygame.Rect(0,0,1,1)
		
		# movement
		self.dx = 0.0
		self.dy = 0.0
		self.speed = 0.4
		self.mobile = False
		
		self.currentAnim = "idle"
		self.state = "idle"
		self.target = None
		self.timer = 0.0
		self.path = [] # [(x, y), (x2, y2)...]
		
	def setPos(self, x, y):
		self.x = x
		self.y = y
		self.mapRect.topleft = (x,y)
	
	def getPos(self):
		return (self.x, self.y)
	
	def move(self, x, y):
		self.setPos(self.x + x, self.y + y)
	
	def setMovement(self, x, y):
		self.dx = x # -1, 0, 1
		self.dy = y

	def update(dt=0.0):
		if self.mobile:
			self.move(self.dx*dt, self.dy*dt)


class Being(object):
	def __init__(self, id):
		self.id = id
		
		self.hp = 1
		self.hpMax = 1
		
		self.carac = {}
		for carac in ["str", "dex", "cons", "wil"]:
			self.carac[carac] = 1
		
		self.skills = {}
		
	def heal(self, n):
		self.hp += n
		# keep hp between 0 and hpMax
		self.hp = min(max(self.hp, 0), self.maxHp)
		
	def getCarac(self, caracName):
		if caracName in self.carac:
			return self.carac[caracName]
		return 0
		
	def getSkill(self, skillName):
		if skillName in self.skills:
			return self.skills[skillName]
		return 0
		
	
class Mob(Being, MapObject):
	def __init__(self, id, mobId, x, y):
		Being.__init__(self, id)
		MapObject.__init__(self, id)
		self.mobId = mobId
		
		self.setPos(x, y)
		
		
