import pygame, sys
from pygame.locals import QUIT
pygame.init()

# Screen dimensions and frame rate
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
pygame.display.set_caption("Escape The Algorithm")
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

# Initialize variables
a = 0
room = "start"
start_frame_index = 0  # Current frame
start_frame_timer = 0  # Timer for frame updates
START_NUM_FRAMES = 4  # Total frames in the spritesheet
running_forward = True  # Direction of animation (forward or backward)
nova_name = "NOVA" # Text for the name under the image
FRAME_WIDTH, FRAME_HEIGHT = 128, 128  # Original frame size
TARGET_FRAME_WIDTH, TARGET_FRAME_HEIGHT = 80, 80  # Target frame size
CHARACTER_NUM_FRAMES = 4
NUM_DIRECTIONS = 4
character = 1
FRAME_RATE = 300  # Milliseconds per frame
x, y = 100, 300  # Starting position | Initial sprite position and state:
direction = 0  # Default direction (DOWN)
charecter_frame_index = 0  # Current frame
charecter_frame_timer = 0  # Timer for frame updates

# Load assets once
background = pygame.image.load("assets/images/start_background.jpg").convert()
background = pygame.transform.scale(background, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
door_sheet = pygame.image.load("assets/images/start-door.png").convert_alpha()
door_sheet = pygame.transform.scale(door_sheet, (door_sheet.get_width() * 8, door_sheet.get_height() * 9))
nova = pygame.image.load("assets/characters/NOVA.png")
nova = pygame.transform.scale(nova, (200, 200))  # Resize to 200x200 pixels
original_spritesheet = pygame.image.load(f"assets/characters/{character}.png").convert_alpha() # Load the spritesheet

# Ensure scaled sheet has enough space for all frames and directions
scaled_width = TARGET_FRAME_WIDTH * CHARACTER_NUM_FRAMES
scaled_height = TARGET_FRAME_HEIGHT * NUM_DIRECTIONS
spritesheet = pygame.transform.scale(original_spritesheet, (scaled_width, scaled_height))

# Load a monospace font
font = pygame.font.SysFont("monospace", 18)
novaFont = pygame.font.SysFont("monospace", 36, bold=True)

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

# Crop function for spritesheet
def crop(sheet, frame):
    crop_width = sheet.get_width() // START_NUM_FRAMES
    crop_height = sheet.get_height()
    crop_rect = pygame.Rect(frame * crop_width, 0, crop_width, crop_height)
    return sheet.subsurface(crop_rect)

# Function to draw the static text (with wrapping) and the rectangle
def draw_textbox(text):
    # Set the maximum width for each line of text
    max_width = SCREEN_WIDTH - 250  # Leave padding on both sides

    words = text.split(" ")  # Split text into words
    lines = []
    current_line = ""

    # Split words into lines based on the max width
    for word in words:
        test_line = current_line + " " + word if current_line else word
        test_surface = font.render(test_line, True, pygame.Color("white"))

        if test_surface.get_width() <= max_width:
            current_line = test_line  # Add word to the current line
        else:
            lines.append(current_line)  # Line is too long, push current line to the lines list
            current_line = word  # Start a new line with the current word

    if current_line:  # Add the last line if there is one
        lines.append(current_line)

    # Calculate the height of the entire text block
    text_height = len(lines) * font.get_height()

    rect_padding = 10  # Padding around the text inside the box
    rect_x = 20  # X position of the rectangle
    rect_y = 50  # Y position of the rectangle
    rect_width = max_width + rect_padding * 2  # Width of the rectangle (considering padding)
    rect_height = text_height + rect_padding * 2  # Height of the rectangle (considering padding)

    # Draw the rectangle (box)
    pygame.draw.rect(screen, pygame.Color("white"), (rect_x, rect_y, rect_width, rect_height))  # Outer box
    pygame.draw.rect(screen, pygame.Color("black"), (rect_x + 3, rect_y + 3, rect_width - 6, rect_height - 6))  # Inner white box (border effect)

    # Render each line and blit it to the screen
    y_offset = rect_y + rect_padding  # Starting Y position, adjusted for padding
    for line in lines:
        txt_surface = font.render(line, True, pygame.Color("white"))
        screen.blit(txt_surface, (rect_x + rect_padding, y_offset))  # Blit each line with padding inside the rectangle
        y_offset += font.get_height()  # Move the Y position down for the next line

def start_character():
    #Sprite:
    original_spritesheet = pygame.image.load(f"assets/characters/{character}.png").convert_alpha() # Load the spritesheet
    # Ensure scaled sheet has enough space for all frames and directions
    scaled_width = TARGET_FRAME_WIDTH * CHARACTER_NUM_FRAMES
    scaled_height = TARGET_FRAME_HEIGHT * NUM_DIRECTIONS
    spritesheet = pygame.transform.scale(original_spritesheet, (scaled_width, scaled_height))
    frames = extract_directional_frames(spritesheet, TARGET_FRAME_WIDTH, TARGET_FRAME_HEIGHT, CHARACTER_NUM_FRAMES, NUM_DIRECTIONS)
    return frames

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
        crop_rect = pygame.Rect((door_pos[0]+25, door_pos[1]+55), ((door_sheet.get_width() // START_NUM_FRAMES)-57, door_sheet.get_height()-60))
        
        if crop_rect.collidepoint(mouse_pos):
            # Hovering: Animate forward
            start_frame_timer += clock.get_time()
            if start_frame_timer > FRAME_RATE:
                start_frame_timer = 0
                if start_frame_index < START_NUM_FRAMES - 1:
                    start_frame_index += 1
        else:
            # Not hovering: Animate backward
            start_frame_timer += clock.get_time()
            if start_frame_timer > FRAME_RATE:
                start_frame_timer = 0
                if start_frame_index > 0:
                    start_frame_index -= 1
        
        # Blit the current frame of the sprite
        pygame.draw.rect(screen, (0, 0, 0), (crop_rect.x, crop_rect.y, crop_rect.width, crop_rect.height), 0)
        screen.blit(crop(door_sheet, start_frame_index), door_pos)
        if a == 0:
            frames = start_character()
            a = 1
        screen.blit(frames[direction][charecter_frame_index], (x, y))
        
        
        if pygame.event.get(pygame.MOUSEBUTTONDOWN):
            room = "work cited"
        

    elif room == "work cited":
        screen.fill((255, 0, 0))

        if pygame.event.get(pygame.MOUSEBUTTONDOWN):
            room = "start"
    
    # Handle events
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
    
    # Update display and tick clock
    pygame.display.flip()
    clock.tick(30)

pygame.quit()
sys.exit()