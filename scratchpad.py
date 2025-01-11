import pygame


pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
FRAME_WIDTH, FRAME_HEIGHT = 128, 128  # Original frame size
TARGET_FRAME_WIDTH, TARGET_FRAME_HEIGHT = 80, 80  # Target frame size
NUM_FRAMES = 4
NUM_DIRECTIONS = 4
FRAME_RATE = 300  # Milliseconds per frame
SPEED = 5

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Scaled Spritesheet Animation")
clock = pygame.time.Clock()

# Load the spritesheet
original_spritesheet = pygame.image.load("assets/characters/2.png").convert_alpha()

# Ensure scaled sheet has enough space for all frames and directions
scaled_width = TARGET_FRAME_WIDTH * NUM_FRAMES
scaled_height = TARGET_FRAME_HEIGHT * NUM_DIRECTIONS
spritesheet = pygame.transform.scale(original_spritesheet, (scaled_width, scaled_height))



# Extract frames with bounds checking
def extract_directional_frames(spritesheet, frame_width, frame_height, num_frames, num_directions):
    frames = []
    for direction in range(num_directions):
        direction_frames = []
        for frame in range(num_frames):
            x = frame * frame_width
            y = direction * frame_height 
            frame_surface = spritesheet.subsurface((x, y, frame_width, frame_height))
            direction_frames.append(frame_surface)
        frames.append(direction_frames)
    return frames

frames = extract_directional_frames(spritesheet, TARGET_FRAME_WIDTH, TARGET_FRAME_HEIGHT, NUM_FRAMES, NUM_DIRECTIONS)

# Initial sprite position and state
x, y = 100, 300  # Starting position
direction = 0  # Default direction (DOWN)
frame_index = 0  # Current frame
frame_timer = 0  # Timer for frame updates

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Handle movement input
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        x += SPEED
        direction = 1  # RIGHT
    elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
        x -= SPEED
        direction = 3  # LEFT
    elif keys[pygame.K_UP] or keys[pygame.K_w]:
        y -= SPEED
        direction = 2  # UP
    elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
        y += SPEED
        direction = 0  # DOWN
    else:
        direction = 0  # Default to DOWN
        
    # Update frame based on timer
    frame_timer += clock.get_time()
    if frame_timer > FRAME_RATE:
        frame_index = (frame_index + 1) % NUM_FRAMES
        frame_timer = 0

    # Clear the screen
    screen.fill((30, 30, 30))

    # Draw the current frame
    screen.blit(frames[direction][frame_index], (x, y))

    # Update the display
    pygame.display.flip()
    clock.tick(30)  # Limit to 30 FPS

pygame.quit()
