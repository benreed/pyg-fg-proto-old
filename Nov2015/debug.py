"""
   Module for debugging functions and features
"""
import pygame

import constants

class DebugBox(pygame.sprite.Sprite):
    """A Sprite that illustrates the boundaries
       of a collision rect
    """
    def __init__(self, width, height):
        super(DebugBox, self).__init__()

        self.image = pygame.Surface([width, height])