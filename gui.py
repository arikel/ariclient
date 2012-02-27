#!/usr/bin/python
# -*- coding: utf8 -*-

import pygame
import sys
import math
import re
import string

from guiFunctions import *
from guiWidget import Widget
from guiScroll import *
from guiEntry import *
from guiEmote import *
from guiGauge import *


if __name__=="__main__":
	
	pygame.init()
	screen = pygame.display.set_mode((640, 480))
	
