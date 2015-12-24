"""Main module for platformer-fighter testbed (Nov 2015)
   Written Dec 4, 2015 by Benjamin Reed
"""

import pygame

import constants
from levels import *
from phys_object import *

def main():
    """Main function
    """

    # Initialization
    pygame.init()
    print pygame.__version__
    print pygame.font.get_default_font()

    # Set screen dimensions and window caption
    screenSize = (constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT)
    screen = pygame.display.set_mode(screenSize)
    pygame.display.set_caption(constants.WINDOW_CAPTION)

    # DEBUG: Test objects declared here
    player = Player()

    # Level list
    #test_level = PlayLevel_01(player)
    test_level = PlayLevel_02(player)
    level_list = []
    level_list.append(test_level)

    # Set a list index for the current level
    current_level_no = 0
    current_level = level_list[current_level_no]

    # Set up active sprite group
    active_sprite_list = pygame.sprite.Group()
    player.level = current_level

    # Add player to the active sprite list once their level
    #   member is set
    active_sprite_list.add(player)

    # ---------- Loop and event control initialization ----------

    # Boolean to control main loop exit
    done = False

    # DEBUG: Game-scoped input state variables
    #key = None
    left_held = False
    right_held = False

    # Frame counter variable (the first of many?)
    jump_frame_counter = 0

    # Variable limit on how high the frame counter goes
    #   (to be reassigned as needed?)
    counter_limit = 0

    # Start the clock to manage for fast the display
    #   updates
    clock = pygame.time.Clock()

    # ---------- MAIN LOOP ----------
    while not done:
        # ---------- Event polling ----------

        # Get key states
        #key = pygame.key.get_pressed()

        #pygame.event.get() clears event queue
        for event in pygame.event.get():

            # Look for quit event
            if event.type == pygame.QUIT:
                done = True

            # ---------- Input handling ----------
            # Handle KEYDOWN events
            if event.type == pygame.KEYDOWN:

                #TODO:
                # Handle player holding both left
                #   and right at once (resolve to
                #   horizontal neutral input --
                #   character does not move
                #   horizontally)

                # Keydown left: Move character left
                if event.key == pygame.K_LEFT:
                    #left_held = True
                    #if not right_held:
                        #player.go_left()
                    #else:
                        #player.stop()
                    player.go_left()

                # Keydown right: Move character right
                elif event.key == pygame.K_RIGHT:
                    #right_held = True
                    #if not left_held:
                        #player.go_right()
                    #else:
                        #player.stop()
                    player.go_right()

                # Keydown up: Jump / air jump
                elif event.key == pygame.K_UP:
                    jump_frame_counter +=1
                    if player.airborne:
                        player.air_jump()
                    else:
                        player.jump()

            # Handle KEYUP events
            if event.type == pygame.KEYUP:
                # Keyup left: Stop moving left
                if event.key == pygame.K_LEFT:
                    #left_held = False
                    #if player.deltaX < 0 and not right_held:
                        #player.stop()
                    if player.deltaX < 0:
                        player.stop()

                # Keyup right: Stop moving right
                elif event.key == pygame.K_RIGHT:
                    #right_held = False
                    #if player.deltaX > 0 and not left_held:
                        #player.stop()
                    if player.deltaX > 0:
                        player.stop()

                # Keyup up: Test how long since jump button pressed and
                #   determine height of jump
                elif event.key == pygame.K_UP:

                    # If 10 frames or less have passed between jump press
                    #   and jump release, player's upward momentum is arrested to
                    #   cause a short jump
                    if jump_frame_counter <= 10:
                        player.stop_rising()

                    # Reset jump frame counter
                    jump_frame_counter = 0

        #if key[pygame.K_LEFT] and key[pygame.K_RIGHT]:
            #print "Both held"
            #player.stop()

        # ---------- Update ----------

        # Update active sprites
        active_sprite_list.update()

        # DEBUG: Player vs screen boundary handling (right)
        if player.rect.right > constants.SCREEN_WIDTH:
            player.rect.right = constants.SCREEN_WIDTH

        # DEBUG: Player vs screen boundary handling (left)
        if player.rect.left < 0:
            player.rect.left = 0

        # ---------- Draw code begins ----------

        # Draw current level
        current_level.draw(screen)

        # Draw active sprite list
        active_sprite_list.draw(screen)

        # ---------- Draw code ends ----------

        # Test the frame counter(s) to make sure we don't
        #   count past whatever limit(s) we set
        if jump_frame_counter == counter_limit:
            jump_frame_counter = 0

        # If frame counters are greater than 0, they're clearly
        #   counting time since some event, so add 1 to their
        #   values
        if jump_frame_counter > 0:
            jump_frame_counter+=1

        # Limit to target frame rate (60 fps)
        clock.tick(constants.TARGET_FRAME_RATE)

        # DEBUG: Print FPS to console
        # print clock.get_fps()

        # Flip display
        pygame.display.flip()

    # Be IDLE friendly. If you forget this line, the program will 'hang'
    # on exit.
    pygame.quit()

if __name__ == "__main__":
    main()
