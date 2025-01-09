import pygame, sys
from pygame.locals import QUIT

pygame.init()

room = "start"

# Screen dimensions and frame rate
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
pygame.display.set_caption("Escape The Algorithm")
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
FRAME_RATE = 300  # Milliseconds per frame

# Initialize variables for sprite animation
frame_index = 0  # Current frame
frame_timer = 0  # Timer for frame updates
NUM_FRAMES = 4  # Total frames in the spritesheet
running_forward = True  # Direction of animation (forward or backward)

# Load assets once
background = pygame.image.load("assets/images/start_background.jpg").convert()
background = pygame.transform.scale(background, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
door_sheet = pygame.image.load("assets/images/start-door.png").convert_alpha()
door_sheet = pygame.transform.scale(door_sheet, (door_sheet.get_width() * 8, door_sheet.get_height() * 9))

# Crop function for spritesheet
def crop(sheet, frame):
    crop_width = sheet.get_width() // NUM_FRAMES
    crop_height = sheet.get_height()
    crop_rect = pygame.Rect(frame * crop_width, 0, crop_width, crop_height)
    return sheet.subsurface(crop_rect)

# Main game loop
running = True
while running:
    screen.fill((0, 0, 0))  # Clear screen
    
    if room == "start":
        # Draw background
        screen.blit(background, (0, 0))
        screen.blit(background, (400, 0))
        screen.blit(background, (0, 300))
        screen.blit(background, (400, 300))

        # Get mouse position
        mouse_pos = pygame.mouse.get_pos()

        # Draw sprite and update frame
        door_pos = (300, 600-door_sheet.get_height())  # Position where the sprite is drawn
        crop_rect = pygame.Rect(door_pos, (door_sheet.get_width() // NUM_FRAMES, door_sheet.get_height()))

        if crop_rect.collidepoint(mouse_pos):
            # Hovering: Animate forward
            frame_timer += clock.get_time()
            if frame_timer > FRAME_RATE:
                frame_timer = 0
                if frame_index < NUM_FRAMES - 1:
                    frame_index += 1
        else:
            # Not hovering: Animate backward
            frame_timer += clock.get_time()
            if frame_timer > FRAME_RATE:
                frame_timer = 0
                if frame_index > 0:
                    frame_index -= 1

        # Blit the current frame of the sprite
        screen.blit(crop(door_sheet, frame_index), door_pos)

        # Handle events
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False

        # Update display and tick clock
        pygame.display.flip()
        clock.tick(30)

pygame.quit()
sys.exit()
