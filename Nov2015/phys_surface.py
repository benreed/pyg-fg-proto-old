"""
    Module for classes representing physical surfaces in
    a play stage -- walls or platforms that game objects
    may physically interact with
    Written Dec 4, 2015 by Benjamin Reed
"""
import pygame

import constants

# Generic surface superclass. Basic surface functionality
#   common to all Surfaces
class PhysSurface(pygame.sprite.Sprite):
    def __init__(self):
        super(PhysSurface, self).__init__()

# A Platform is a static barrier that objects can smack
#   into, land on, be obstructed by, etc
class Platform(PhysSurface):
    def __init__(self, width, height):
        super(Platform, self).__init__()

        # DEBUG: Image is a green rectangle
        self.image = pygame.Surface([width, height])
        self.image.fill(constants.GREEN)

        self.rect = self.image.get_rect()