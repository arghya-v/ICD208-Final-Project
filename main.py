import pygame, sys
from pygame.locals import QUIT
pygame.init()

# Screen dimensions and frame rate
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
pygame.display.set_caption("Escape The Algorithm")
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

# Initialize variables
room = "start"
start_frame_index = 0  # Current frame
start_frame_timer = 0  # Timer for frame updates
START_NUM_FRAMES = 4  # Total frames in the spritesheet
running_forward = True  # Direction of animation (forward or backward)
nova_name = "NOVA"  # Text for the name under the image
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

# Scaling factor for the character
SCALE_FACTOR = 8  # Scale up the character size by 2x

# Load assets once
background = pygame.image.load("assets/images/start_background.jpg").convert()
background = pygame.transform.scale(background, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
door_sheet = pygame.image.load("assets/images/start-door.png").convert_alpha()
door_sheet = pygame.transform.scale(door_sheet, (door_sheet.get_width() * 8, door_sheet.get_height() * 9))
nova = pygame.image.load("assets/characters/NOVA.png")
nova = pygame.transform.scale(nova, (200, 200))  # Resize to 200x200 pixels
original_spritesheet = pygame.image.load(f"assets/characters/{character}.png").convert_alpha()  # Load the spritesheet

# Ensure scaled sheet has enough space for all frames and directions
scaled_width = TARGET_FRAME_WIDTH * CHARACTER_NUM_FRAMES
scaled_height = TARGET_FRAME_HEIGHT * NUM_DIRECTIONS
spritesheet = pygame.transform.scale(original_spritesheet, (scaled_width, scaled_height))

# Load a monospace font
font = pygame.font.SysFont("monospace", 18)
novaFont = pygame.font.SysFont("monospace", 36, bold=True)
scrnfont = pygame.font.SysFont("monospace", 18, bold=True)

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
    max_width = SCREEN_WIDTH - 250  # Leave padding on both sides

    words = text.split(" ")  # Split text into words
    lines = []
    current_line = ""

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

    text_height = len(lines) * font.get_height()

    rect_padding = 10  # Padding around the text inside the box
    rect_x = 20  # X position of the rectangle
    rect_y = 50  # Y position of the rectangle
    rect_width = max_width + rect_padding * 2  # Width of the rectangle (considering padding)
    rect_height = text_height + rect_padding * 2  # Height of the rectangle (considering padding)

    pygame.draw.rect(screen, pygame.Color("white"), (rect_x, rect_y, rect_width, rect_height))  # Outer box
    pygame.draw.rect(screen, pygame.Color("black"), (rect_x + 3, rect_y + 3, rect_width - 6, rect_height - 6))  # Inner white box (border effect)

    y_offset = rect_y + rect_padding  # Starting Y position, adjusted for padding
    for line in lines:
        txt_surface = font.render(line, True, pygame.Color("white"))
        screen.blit(txt_surface, (rect_x + rect_padding, y_offset))  # Blit each line with padding inside the rectangle
        y_offset += font.get_height()  # Move the Y position down for the next line

def start_character():
    original_spritesheet = pygame.image.load(f"assets/characters/{character}.png").convert_alpha()  # Load the spritesheet
    scaled_width = TARGET_FRAME_WIDTH * CHARACTER_NUM_FRAMES
    scaled_height = TARGET_FRAME_HEIGHT * NUM_DIRECTIONS
    spritesheet = pygame.transform.scale(original_spritesheet, (scaled_width, scaled_height))
    frames = extract_directional_frames(spritesheet, TARGET_FRAME_WIDTH, TARGET_FRAME_HEIGHT, CHARACTER_NUM_FRAMES, NUM_DIRECTIONS)
    return frames

# Function to draw buttons
def draw_button(button_text, x, y, color, hover_color):
    button_width = 150
    button_height = 50
    button_rect = pygame.Rect(x, y, button_width, button_height)
    mouse_pos = pygame.mouse.get_pos()

    if button_rect.collidepoint(mouse_pos):
        pygame.draw.rect(screen, hover_color, button_rect)
        if pygame.mouse.get_pressed()[0]:  # Left-click
            return True  # Button clicked
    else:
        pygame.draw.rect(screen, color, button_rect)

    # Render button text
    text_surface = novaFont.render(button_text, True, pygame.Color("white"))
    text_rect = text_surface.get_rect(center=button_rect.center)
    screen.blit(text_surface, text_rect)

    return False

# Main game loop
running = True
while running:
    
    screen.fill((0, 0, 0))  # Clear screen
    direction = 0
    
    if room == "start":
        # Draw background
        screen.blit(background, (0, 0))
        screen.blit(background, (400, 0))
        screen.blit(background, (0, 300))
        screen.blit(background, (400, 300))
        
        # Player's starting position and direction
        x, y = 125, 125  # Position of the sprite
        direction = 0    # Default direction (DOWN)

        mouse_pos = pygame.mouse.get_pos()

        # Door animation logic
        door_pos = (300, 600 - door_sheet.get_height())
        crop_rect = pygame.Rect(
            (door_pos[0] + 25, door_pos[1] + 55), 
            ((door_sheet.get_width() // START_NUM_FRAMES) - 57, door_sheet.get_height() - 60)
        )
        
        if crop_rect.collidepoint(mouse_pos):
            start_frame_timer += clock.get_time()
            if start_frame_timer > FRAME_RATE:
                start_frame_timer = 0
                if start_frame_index < START_NUM_FRAMES - 1:
                    start_frame_index += 1
        else:
            start_frame_timer += clock.get_time()
            if start_frame_timer > FRAME_RATE:
                start_frame_timer = 0
                if start_frame_index > 0:
                    start_frame_index -= 1

        pygame.draw.rect(screen, (0, 0, 0), (crop_rect.x, crop_rect.y, crop_rect.width, crop_rect.height), 0)
        screen.blit(crop(door_sheet, start_frame_index), door_pos)

        frames = start_character()  # Load frames once

        charecter_frame_timer += clock.get_time()
        if charecter_frame_timer > FRAME_RATE:
            charecter_frame_timer = 0
            charecter_frame_index = (charecter_frame_index + 1) % CHARACTER_NUM_FRAMES

        # Blit the scaled character sprite
        current_frame = frames[direction][charecter_frame_index]
        scaled_width = current_frame.get_width() * SCALE_FACTOR
        scaled_height = current_frame.get_height() * SCALE_FACTOR
        scaled_frame = pygame.transform.scale(current_frame, (scaled_width, scaled_height))
        scaled_x = x - (scaled_width - current_frame.get_width()) // 2
        scaled_y = y - (scaled_height - current_frame.get_height()) // 2
        screen.blit(scaled_frame, (scaled_x, scaled_y))

        # Render instructions text with a white box behind it
        instructions_text = "Q or W to select character"
        instructions_surface = scrnfont.render(instructions_text, True, pygame.Color("black"))

        instructions_x = 25  # X-coordinate (pixels from the left)
        instructions_y = 460  # Y-coordinate (pixels from the top)

        # Draw a white box behind the instructions text
        text_rect = pygame.Rect(instructions_x - 5, instructions_y - 5, instructions_surface.get_width() + 10, instructions_surface.get_height() + 10)
        pygame.draw.rect(screen, pygame.Color("white"), text_rect)  # White background for the text

        # Draw the instructions text on top of the white box
        screen.blit(instructions_surface, (instructions_x, instructions_y))

        # Draw the buttons and check if clicked
        if draw_button("Start", 475, 250, pygame.Color("bisque4"), pygame.Color("chocolate4")):
            room = "room1"  # Proceed to the first room
        if draw_button("Work Cited", 475, 320, pygame.Color("lightblue"), pygame.Color("dodgerblue")):
            room = "work cited"  # Go to the work cited room
        if draw_button("Help", 475, 390, pygame.Color("lightgreen"), pygame.Color("green")):
            room = "help"  # Go to the help room

        for event in pygame.event.get(pygame.KEYDOWN):
            if event.key == pygame.K_q:
                character -= 1
                if character < 1:
                    character = 11
            elif event.key == pygame.K_w:
                character += 1
                if character > 11:
                    character = 1
            
    elif room == "work cited":
        screen.fill((0, 0, 255))  # Blue screen

        if pygame.event.get(pygame.MOUSEBUTTONDOWN):
            room = "start"  # Go back to the start when mouse is clicked
            
    elif room == "help":
        screen.fill((0, 255, 0))  # Green screen

        if pygame.event.get(pygame.MOUSEBUTTONDOWN):
            room = "start"  # Go back to the start when mouse is clicked
    
    elif room == "room1":
        screen.fill((255, 0, 0))  # Red screen

        if pygame.event.get(pygame.MOUSEBUTTONDOWN):
            room = "start"  # Go back to the start when mouse is clicked

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
    
    pygame.display.flip()
    clock.tick(30)

pygame.quit()
sys.exit()