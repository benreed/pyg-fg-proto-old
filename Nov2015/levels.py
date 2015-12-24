"""
    Module for classes representing stages, including play stages
    as well as menu screens
    Written Dec 4, 2015 by Benjamin Reed
"""
import pygame

import constants
from phys_surface import *

# Generic level superclass
class Level(object):

    # Background image
    # DEBUG: background is a black window-sized surface to black out frame
    # background = None
    background = pygame.Surface([constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT])

    # How far this world has been scrolled left/right
    world_shift = 0
    level_limit = -1000

    #def __init__(self):
        #print "I'm a level."

    # Generic state update method to be overridden
    #   in subclasses
    # def update(self):
        # print "Updating..."

    # Generic draw method to be overriden
    #   in subclasses
    def draw(self, screen):
        # Wipe contents of previous frame
        # (DEBUG: Fill with black)
        screen.fill(constants.BLACK)
        # DEBUG: Don't forget to blit!
        screen.blit(self.background,[0,0])

# Subclass for a play stage, where actual gameplay
#   takes place
class PlayLevel(Level):
    def __init__(self, player):
        super(PlayLevel, self).__init__()

        # Create a sprite group for level platforms
        #   (which of course extend the pygame Sprite)
        self.platform_list = pygame.sprite.Group()

        # Add player param as a member of this level
        #   so that the level can reference player
        #   members/properties
        self.player = player

    def update(self):
        # Update members of the platform list
        self.platform_list.update()

    def draw(self, screen):
        # Wipe contents of previous frame
        # (DEBUG: Fill with black)
        screen.fill(constants.BLACK)
        # DEBUG: Don't forget to blit!
        screen.blit(self.background,[0,0])

        # Draw all the sprite lists that we have
        self.platform_list.draw(screen)

# Test level: Flat empty stage (Final Destination jokes go here)
class PlayLevel_01(PlayLevel):
    def __init__(self, player):
        super(PlayLevel_01, self).__init__(player)

        # Single flat platform to serve as floor
        level = [[constants.SCREEN_WIDTH,15,0,(constants.SCREEN_HEIGHT-30)]]

        # Add platforms to platform list
        for platform in level:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block)

# Test level: ground + elevated platforms to jump on
class PlayLevel_02(PlayLevel):
    def __init__(self, player):
        super(PlayLevel_02, self).__init__(player)

        # Ground platform plus two raised platforms
        level = [ [constants.SCREEN_WIDTH,15,0,(constants.SCREEN_HEIGHT-30)],
                  [80, 15, 140, (constants.SCREEN_HEIGHT-200)],
                  [80, 15, (constants.SCREEN_WIDTH-240), (constants.SCREEN_HEIGHT-150)]
                  ]

        # Add platforms to platform list
        for platform in level:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block)