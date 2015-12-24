"""Module for game objects with physical properties
   (movement, collision, etc.)
   Written Dec 4, 2015 by Benjamin Reed
"""
import pygame

import constants
from spritesheet import *

class PhysObject(pygame.sprite.Sprite):
    """Generic physical object class that extends Sprite"""

    # --- Attributes ---

    # Vector attributes
    deltaX = 0
    deltaY = 0

    def __init__(self, color=constants.RED, width=30, height=50):
        """Constructor (color=constants.RED, width=30, height=50)"""

        # Call superconstructor
        super(PhysObject, self).__init__()

        # DEBUG: Set image to a Surface so as to draw a rect
        self.image = pygame.Surface([width, height])
        self.image.fill(color)

        # DEBUG: Set collision rect to image rect
        self.rect = self.image.get_rect()

        # DEBUG: Initialize rect coords to determine
        #   drawing coords
        self.rect.x = 10
        self.rect.y = 10

#class Player(PhysObject):
class Player(pygame.sprite.Sprite):
    """Test player character class.

       INSTANCE VARIABLES:
       RUN_SPEED :
          Character's left/right speed while standing on a surface
       AIR_STEER_SPEED :
          Character's left/right speed during a jump or fall
       movement_speed :
          Character's current left/right movement speed
       jump_force :
          Force applied when character jumps from ground
       air_jump_force :
          Force applied when character jumps in air
       gravity_force:
          Downward force applied while character is airborne

       direction :
          Character's sprite facing direction
       airborne :
          Tracks if character is grounded or airborne
       air_jumped:
          Tracks if character has jumped in the air or not
    """
    # -------- Input state variables --------
    left_held = False
    right_held = False

    # -------- Movement attributes --------
    deltaX = 0
    deltaY = 0
    RUN_SPEED = 6
    AIR_STEER_SPEED = 3
    movement_speed = RUN_SPEED
    jump_force = -10
    #air_jump_force = 0.75 * jump_force
    air_jump_force = jump_force
    gravity_force = .35

    # -------- Character state variables --------
    direction = "R"
    airborne = True
    air_jumped = False

    # -------- Frame counting variables --------
    #time_since_jump = 0
    #counter_limit = 0

    # -------- Lists for animation frames --------
    idle_frames_R = []
    idle_frames_L = []
    running_frames_R = []
    running_frames_L = []
    jumping_frames_R = []
    jumping_frames_L = []

    # List of surfaces player can collide with
    #   (from level)
    level = None

    def __init__(self, color=constants.RED, width=30, height=50):
        #super(Player, self).__init__(color, width, height)
        super(Player, self).__init__()

        # Call function to populate frame lists from sprite
        #   sheet
        self.init_frames()

        # Set the image the player starts with
        self.image = self.idle_frames_R[0]

        # Set a referance to the image rect.
        self.rect = self.image.get_rect()
        self.rect.x = 10
        self.rect.y = 10

    def init_frames(self):
        # Get sprite sheet using a SpriteSheet object
        sprite_sheet = SpriteSheet("img/nov2015_spritesheet_2.png")

        # Initialize sprite sheet attributes
        #   (draw coords and frame dimensions)
        originX = 0
        originY = 0
        image_width = 120
        image_height = 114

        # Initialize right-facing frames
        # (Right idle frames)
        image = sprite_sheet.get_image(originX, originY, image_width, image_height)
        self.idle_frames_R.append(image)

        # (Right running frames)
        originX = 240
        for x in range (0, 6):
            image = sprite_sheet.get_image(originX, originY, image_width, image_height)
            self.running_frames_R.append(image)
            originX += image_width

        # (Right jumping frames)
        for x in range (0, 4):
            image = sprite_sheet.get_image(originX, originY, image_width, image_height)
            self.jumping_frames_R.append(image)
            originX += image_width

        # Load right-facing images again and flip them to face left
        # (Left idle frames)
        originX = 0
        originY = 0
        image = sprite_sheet.get_image(originX, originY, image_width, image_height)
        image = pygame.transform.flip(image, True, False)
        self.idle_frames_L.append(image)

        # (Left running frames)
        originX = 240
        for x in range (0, 6):
            image = sprite_sheet.get_image(originX, originY, image_width, image_height)
            image = pygame.transform.flip(image, True, False)
            self.running_frames_L.append(image)
            originX += image_width

        # (Left jumping frames)
        for x in range (0, 4):
            image = sprite_sheet.get_image(originX, originY, image_width, image_height)
            image = pygame.transform.flip(image, True, False)
            self.jumping_frames_L.append(image)
            originX += image_width

    def update(self):
        # Calculate and apply gravity
        self.calc_grav()

        # Move left/right (apply deltaX)
        self.rect.x += self.deltaX
        pos = self.rect.x + self.level.world_shift

        # Set running frame based on direction, screen position,
        #   and frame rate
        if self.direction == "R":
            frame = (pos // 30) % len(self.running_frames_R)
            self.image = self.running_frames_R[frame]
        else:
            frame = (pos // 30) % len(self.running_frames_L)
            self.image = self.running_frames_L[frame]

        # Check for collisions (x-axis)
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            # If we are moving right,
            # set our right side to the left side of the item we hit
            if self.deltaX > 0:
                self.rect.right = block.rect.left
            elif self.deltaY < 0:
                # Otherwise if we are moving left, do the opposite.
                self.rect.left = block.rect.right

        # Move up/down (apply deltaY)
        self.rect.y += self.deltaY

        # Check for collisions (y-axis)
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:

            # Reset rect position based on the top/bottom of the object.
            if self.deltaY > 0:
                self.rect.bottom = block.rect.top
                # DEBUG: Land only if character was falling when
                #   collision occurred
                self.land()
            elif self.deltaY < 0:
                self.rect.top = block.rect.bottom
                # Cause character to start falling if they bump
                #   their head on the bottom of a platform
                self.stop_rising()
                #print "Bump" + str(self.deltaY)

        #DEBUG: If character is rising, display jumping animation
        if self.deltaY < 0:
            if self.direction == "R":
                self.image = self.jumping_frames_R[0]
            else:
                self.image = self.jumping_frames_L[0]

        # DEBUG: If character is falling, display falling animation
        if self.deltaY > 0:
            if self.direction == "R":
                if self.deltaY < 1.6:
                    self.image = self.jumping_frames_R[1]
                elif self.deltaY < 3.3:
                    self.image = self.jumping_frames_R[2]
                else:
                    self.image = self.jumping_frames_R[3]
            else:
                if self.deltaY < 1.6:
                    self.image = self.jumping_frames_L[1]
                elif self.deltaY < 3.3:
                    self.image = self.jumping_frames_L[2]
                else:
                    self.image = self.jumping_frames_L[3]

        # DEBUG: If not airborne or moving horizontally, display
        #   idle standing animation (currently 1 frame)
        if self.airborne == False and self.deltaX == 0:
            if self.direction == "R":
                self.image = self.idle_frames_R[0]
            else:
                self.image = self.idle_frames_L[0]

        # -------- Counter logic --------
        # Check the frame counter(s) against the counter limit to
        #   make sure we don't count past it
        # If we hit the counter limit, reset our counter(s)
        #if self.time_since_jump == self.counter_limit:
            #self.time_since_jump = 0

        # If time since jump is greater than 0, that means we're
        #   counting frames, so we'll increase the counter
        #if self.time_since_jump > 0:
            #self.time_since_jump+=1
            #print "Frames passed since jump began: " + str(self.time_since_jump)

        # -------- DEBUG: Monitor values at the end of update() --------
        # print "Left held: " + str(self.left_held) + "   Right held: " + str(self.right_held)

    # Method to calculate gravity
    def calc_grav(self):
        # Calculate effect of gravity
        if self.deltaY == 0:
            self.deltaY = 1
        else:
            self.deltaY += self.gravity_force

    # Player-controlled movement:
    def go_left(self):
        """ Called when the user hits the left arrow. """
        #if not self.right_held:
        self.left_held = True
        self.deltaX = -1 * self.movement_speed
        if not self.airborne:
            self.direction = "L"

    def go_right(self):
        """ Called when the user hits the right arrow. """
        self.right_held = True
        self.deltaX = self.movement_speed
        if not self.airborne:
            self.direction = "R"

    def jump(self):
        """ Called when user hits 'jump' button. """
        # move down a bit and see if there is a platform below us.
        # Move down 2 pixels because it doesn't work well if we only move down
        # 1 when working with a platform moving down.
        self.rect.y += 2
        platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        self.rect.y -= 2

        # If it is ok to jump, apply jump force and
        #   declare the character airborne
        if len(platform_hit_list) > 0 or self.rect.bottom >= constants.SCREEN_HEIGHT:
            self.deltaY = self.jump_force
            self.airborne = True
            self.movement_speed = self.AIR_STEER_SPEED

    def air_jump(self):
        """ Called when user hits 'jump' button while airborne """
        if self.airborne == True and self.air_jumped == False:
            self.air_jumped = True
            self.deltaY = self.air_jump_force

    def stop(self):
        """ Called when the user lets off the keyboard. """
        self.deltaX = 0

    def stop_rising(self):
        # Apply this velocity change only to ground jump
        #if not self.air_jumped:
            # Apply half of jump force in the opposite
            #   y direction to deltaY to accelerate
            #   the effect of gravity, resulting in
            #   a short jump
        self.deltaY += -0.5 * self.jump_force

    def land(self):
        """ Called when player lands on a platform """
        # Stop player's vertical movement
        self.deltaY = 0

        # Reset jumping state values
        self.airborne = False
        self.air_jumped = False

        # Re-adjust movement speed
        self.movement_speed = self.RUN_SPEED

        # Re-adjust deltaX to ground movement speed,
        #   based on directional facing
        if self.deltaX < 0:
            self.deltaX = -self.movement_speed
            self.direction = "L"

        if self.deltaX > 0:
            self.deltaX = self.movement_speed
            self.direction = "R"

    # -------- DEBUG: Output variables of interest --------
    #def debug_output(self):
        # print self.deltaX
        # print self.air_jumped
        # print "deltaX         : " + str(self.deltaX)
        # print "movement speed : " + str(self.movement_speed)