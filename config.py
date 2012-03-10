#!/usr/bin/python
# -*- coding: utf-8 -*-
import pygame

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

SERVER_ADDRESS = "88.173.217.230"
#SERVER_ADDRESS = "127.0.0.1"
SERVER_PORT = 18647

# controls
KEY_UP = pygame.K_z
KEY_DOWN = pygame.K_s
KEY_LEFT = pygame.K_q
KEY_RIGHT = pygame.K_d
KEY_SELECT_TARGET = pygame.K_a
KEY_ATTACK = pygame.K_e

CONTROL_KEY_LIST = [KEY_UP, KEY_DOWN, KEY_LEFT, KEY_RIGHT, KEY_SELECT_TARGET, KEY_ATTACK]
