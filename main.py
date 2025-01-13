import pygame, sys
from pygame.locals import QUIT
import math
pygame.init()

# Screen dimensions and frame rate
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
pygame.display.set_caption("Escape The Algorithm")
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

# Initialize variables
room = "start"
start = True
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
linecount = 0 # Used to add space between lines on help and works cited page.
SCALE_FACTOR = 8  # Scaling factor for the character Scale up the character size by 2x
time_cutscene = 0 # Used to time the cutscene

# Load assets once
start_background = pygame.image.load("assets/images/start_background.jpg").convert()
start_background = pygame.transform.scale(start_background, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
door_sheet = pygame.image.load("assets/images/start-door.png").convert_alpha()
door_sheet = pygame.transform.scale(door_sheet, (door_sheet.get_width() * 8, door_sheet.get_height() * 9))
workscited_background = pygame.image.load("assets/images/scroll.png").convert_alpha()
workscited_background = pygame.transform.scale(workscited_background, (SCREEN_WIDTH, SCREEN_HEIGHT - 80))
cutscene_background = pygame.image.load("assets/images/cut_scene-background.png").convert()
cutscene_background = pygame.transform.scale(cutscene_background, (SCREEN_WIDTH, SCREEN_HEIGHT))
nova = pygame.image.load("assets/characters/NOVA.png")
nova = pygame.transform.scale(nova, (200, 200))  # Resize to 200x200 pixels
original_spritesheet = pygame.image.load(f"assets/characters/{character}.png").convert_alpha()  # Load the spritesheet

# Ensure scaled sheet has enough space for all frames and directions
scaled_width = TARGET_FRAME_WIDTH * CHARACTER_NUM_FRAMES
scaled_height = TARGET_FRAME_HEIGHT * NUM_DIRECTIONS
spritesheet = pygame.transform.scale(original_spritesheet, (scaled_width, scaled_height))

# Load fonts
Titlefont = pygame.font.SysFont("Comic Sans", 25, bold=True)
Titlefont.set_underline(True)
Bodyfont = pygame.font.SysFont("arial", 15)
font = pygame.font.SysFont("monospace", 18)
novaFont = pygame.font.SysFont("monospace", 36, bold=True)
scrnfont = pygame.font.SysFont("monospace", 18, bold=True)

# Simple textbox for giving what key to use for something
def simple_text(text, x, y, colour="black", back_colour="white"):
    # Render instructions text with a white box behind it
    instructions_text = text
    instructions_surface = scrnfont.render(instructions_text, True, pygame.Color(colour))

    instructions_x = x + 5  # X-coordinate (pixels from the left)
    instructions_y = y + 5  # Y-coordinate (pixels from the top)

    # Draw a white box behind the instructions text
    text_rect = pygame.Rect(instructions_x - 5, instructions_y - 5, instructions_surface.get_width() + 10, instructions_surface.get_height() + 10)
    pygame.draw.rect(screen, pygame.Color(back_colour), text_rect)  # White background for the text

    # Draw the instructions text on top of the white box
    screen.blit(instructions_surface, (instructions_x, instructions_y))

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
def draw_textbox(text, rect_x = 20, rect_y = 50, ifBackground=True, usefont=font, max_width=SCREEN_WIDTH - 250, text_colour="white", rect_padding=10):

    words = text.split(" ")  # Split text into words
    lines = []
    current_line = ""

    for word in words:
        test_line = current_line + " " + word if current_line else word
        test_surface = usefont.render(test_line, True, pygame.Color(text_colour))

        if test_surface.get_width() <= max_width:
            current_line = test_line  # Add word to the current line
        else:
            lines.append(current_line)  # Line is too long, push current line to the lines list
            current_line = word  # Start a new line with the current word

    if current_line:  # Add the last line if there is one
        lines.append(current_line)

    text_height = len(lines) * usefont.get_height()

    rect_width = max_width + rect_padding * 2  # Width of the rectangle (considering padding)
    rect_height = text_height + rect_padding * 2  # Height of the rectangle (considering padding)

    if ifBackground:
        pygame.draw.rect(screen, pygame.Color("white"), (rect_x, rect_y, rect_width, rect_height))  # Outer box
        pygame.draw.rect(screen, pygame.Color("black"), (rect_x + 3, rect_y + 3, rect_width - 6, rect_height - 6))  # Inner white box (border effect)

    y_offset = rect_y + rect_padding  # Starting Y position, adjusted for padding
    for line in lines:
        txt_surface = usefont.render(line, True, pygame.Color(text_colour))
        screen.blit(txt_surface, (rect_x + rect_padding, y_offset))  # Blit each line with padding inside the rectangle
        y_offset += usefont.get_height()  # Move the Y position down for the next line

def start_character():
    original_spritesheet = pygame.image.load(f"assets/characters/{character}.png").convert_alpha()  # Load the spritesheet
    scaled_width = TARGET_FRAME_WIDTH * CHARACTER_NUM_FRAMES
    scaled_height = TARGET_FRAME_HEIGHT * NUM_DIRECTIONS
    spritesheet = pygame.transform.scale(original_spritesheet, (scaled_width, scaled_height))
    frames = extract_directional_frames(spritesheet, TARGET_FRAME_WIDTH, TARGET_FRAME_HEIGHT, CHARACTER_NUM_FRAMES, NUM_DIRECTIONS)
    return frames

# Function to draw buttons with text size
def draw_button(button_text, x, y, color, hover_color, width, height=50, textColour="white", text_size=36):
    button_rect = pygame.Rect(x, y, width, height)
    mouse_pos = pygame.mouse.get_pos()

    # Check for hover and click
    if button_rect.collidepoint(mouse_pos):
        pygame.draw.rect(screen, hover_color, button_rect)
        pygame.draw.rect(screen, pygame.Color("White"), button_rect, 3)
        if pygame.mouse.get_pressed()[0]:  # Left-click
            return True  # Button clicked
    else:
        pygame.draw.rect(screen, color, button_rect)

    # Create a font with the specified size
    font = pygame.font.SysFont("monospace", text_size, bold=True)
    
    # Render button text
    text_surface = font.render(button_text, True, pygame.Color(textColour))
    text_rect = text_surface.get_rect(center=button_rect.center)
    screen.blit(text_surface, text_rect)

    return False

def room_start():
    global start
    if not start:
        return  # Skip processing if `start` is False

    if pygame.mixer.music.get_busy():
        pygame.mixer.music.fadeout(1000)
    else:
        # Determine the music to load based on the room
        music_files = {
            "start": "assets/bgm/bgm-works_cited_help.mp3",
            "work cited": "assets/bgm/bgm-extra.mp3",
            "help": "assets/bgm/bgm-extra.mp3",
            "cutscene": "assets/bgm/bgm-cut_scene.mp3",
            "room1": "assets/bgm/bgm-room_one.mp3",
        }

        # Only load and play music if the room has a valid music file
        if room in music_files:
            new_music = music_files[room]
            pygame.mixer.music.load(new_music)
            pygame.mixer.music.set_volume(10)
            pygame.mixer.music.play(-1, 0.0, 5000)
        start = False

# Main game loop
running = True
while running:
    
    screen.fill((0, 0, 0))  # Clear screen
    room_start()
    direction = 0
    
    if room == "start":
        # Draw start_background
        screen.blit(start_background, (0, 0))
        screen.blit(start_background, (400, 0))
        screen.blit(start_background, (0, 300))
        screen.blit(start_background, (400, 300))

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

        simple_text("Q or W to change characters", 10, 455)

        # Draw the buttons and check if clicked
        if draw_button("Start", crop_rect.centerx-125, 250, pygame.Color("bisque4"), pygame.Color("chocolate4"), 250, 50):
            room = "cutscene"  # Proceed to the first room
            start = True
        if draw_button("Work Cited", crop_rect.centerx-125, 320, pygame.Color("lightblue"), pygame.Color("dodgerblue"), 250, 50):
            room = "work cited"  # Go to the work cited room
            start = True
        if draw_button("Help", crop_rect.centerx-125, 390, pygame.Color("lightgreen"), pygame.Color("green"), 250, 50):
            room = "help"  # Go to the help room
            start = True

        for event in pygame.event.get(pygame.KEYDOWN):
            if event.key == pygame.K_q:
                character -= 1
                if character < 1:
                    character = 10
            elif event.key == pygame.K_w:
                character += 1
                if character > 10:
                    character = 1
        
        frames = start_character()  # Load frames once more so we have it in future rooms and don't need to keep reloading

            
    elif room == "work cited":
        screen.blit(start_background, (0, 0))
        screen.blit(start_background, (400, 0))
        screen.blit(start_background, (0, 300))
        screen.blit(start_background, (400, 300))
        screen.blit(workscited_background, (0, 40))
        simple_text("ESC to go back", 10, 10)
        if draw_button("Back", 10, SCREEN_HEIGHT-40, pygame.Color("gray67"), pygame.Color("gray50"), 100, 30, "white", 30):
            room = "start"
            start = True

        workscited_text_surface = Titlefont.render("Works Cited", True, pygame.Color("black"))
        workscited_text_rect = workscited_text_surface.get_rect(centerx=workscited_background.get_rect().centerx, centery=153)
        screen.blit(workscited_text_surface, workscited_text_rect)
        
        workcited_bodytext = ["Quan, P. (2024, December 6). Day 59 - The Future of Computing and AI [In class lecture]. ICD2O8.3. https://docs.google.com/presentation/d/ 1mkFc_f315xHibJAdqXlhzLN1gnuJWgfL T99qqixDKjM/edit#slide=id.p",
                               " ", " ", " ",
                               "Sukumar R, Gambhir, V., & Seth, J. (2024). Investigating the Ethical Implications of Artificial Intelligence and Establishing Guidelines for Responsible AI Development. 1–6. https://doi.org/10.1109/ acroset62108.2024.10743915",
                               " ", " ", " ", " ",
                               "Richie, R. C. (2024). Basics of Artificial Intelligence (AI) Modeling. Journal of Insurance Medicine, 51(1), 35–40. https://doi.org/10.17849/ insm-51-1-35-40.1",
                               " ", " ",
                               "Jason V. Chavez, Jhordan T. Cuilan, Sali S. Mannan, et al. (2024). Discourse Analysis on the Ethical Dilemmas on the Use of AI in Academic Settings from ICT, Science, and Language Instructors. Forum for Linguistic Studies, 6(5), 349–363. https://doi.org/10.30564/fls.v6i5.6765"]
        linecount = 0
        for line in workcited_bodytext:
            draw_textbox(line, workscited_background.get_rect().x+175, 151+Bodyfont.get_height()*linecount, False, Bodyfont, workscited_background.get_rect().width-375, "black", 20)
            linecount += 1

        if pygame.event.get(pygame.KEYDOWN):
            if pygame.key.get_pressed()[pygame.K_ESCAPE]:
                room = "start"  # Go back to the start when escape is 
                start = True
            
    elif room == "help":
        screen.blit(start_background, (0, 0))
        screen.blit(start_background, (400, 0))
        screen.blit(start_background, (0, 300))
        screen.blit(start_background, (400, 300))
        screen.blit(workscited_background, (0, 40))
        simple_text("ESC to go back", 10, 10)
        if draw_button("Back", 10, SCREEN_HEIGHT-40, pygame.Color("gray67"), pygame.Color("gray50"), 100, 30, "white", 30):
            room = "start"
            start = True
        
        help_text_surface = Titlefont.render("Help", True, pygame.Color("black"))
        help_text_rect = help_text_surface.get_rect(centerx=workscited_background.get_rect().centerx, centery=155)
        screen.blit(help_text_surface, help_text_rect)

        help_bodytext = ["Game Mechanics:",
                            "Objective: Solve puzzles, learn about AI, and make ethical decisions to progress through the escape room.",
                            " ", " ", "Controls:", "Mouse/Trackpad:", "Click to interact with objects.", " ",
                            "Keyboard (if applicable):", "Arrow Keys and WASD: Move/Explore.", "Look to the top left to interact with highlighted objects.",
                            " ", "Hints:", "If you're stuck, NOVA will provide subtle hints.", "Look for glowing or highlighted objects—they often hold clues!"]
        linecount = 0
        for line in help_bodytext:
            draw_textbox(line, workscited_background.get_rect().x+175, 160+Bodyfont.get_height()*linecount, False, Bodyfont, workscited_background.get_rect().width-325, "black", 20)
            linecount += 1

        if pygame.event.get(pygame.KEYDOWN):
            if pygame.key.get_pressed()[pygame.K_ESCAPE]:
                room = "start"  # Go back to the start when escape is pressed
                start = True
    
    elif room == "cutscene":
        screen.blit(cutscene_background, (0, 0))
        simple_text("Space to skip cutscene.", 10, 10)
        if draw_button("Skip", 20, SCREEN_HEIGHT-60, "azure4", "gray24", 100, 30, "white", 20):
            room = "room1"
            start = True

        time_cutscene += clock.get_time()

        if time_cutscene < 10000:
            # Draw the text in room1
            draw_textbox("AI is taking over the world and has trapped you in its neural network", 
                        rect_x=200, rect_y=50, ifBackground=True, 
                        usefont=font, max_width=SCREEN_WIDTH - 300, 
                        text_colour="white", rect_padding=20)
            
            draw_textbox("Escape.", 
                        rect_x=200, rect_y=200, ifBackground=True, 
                        usefont=font, max_width=SCREEN_WIDTH - 700, 
                        text_colour="white", rect_padding=20)
            
            # Floating character logic
            floating_scale_factor = 2  # Smaller scaling factor for the floating character
            floating_amplitude = 20  # Height of the floating motion (in pixels)
            floating_wave_width = 0.001  # Smaller value widens the wave (phase progression slowed)
            rotation_speed = 0.005  # Speed of rotation (degrees per millisecond)
            rightward_speed = 0.05  # Speed of rightward movement

            # Calculate floating character position
            floating_y_offset = int(floating_amplitude * math.sin(pygame.time.get_ticks() * floating_wave_width))
            floating_x = 0 + int(pygame.time.get_ticks() * rightward_speed) % SCREEN_WIDTH  # Moves right over time
            floating_y = 320 + floating_y_offset  # Center position, adjusted for vertical movement

            # Get the scaled character frame
            current_frame = frames[0][0]  # Default frame (down, first animation frame)
            small_width = int(current_frame.get_width() * floating_scale_factor)
            small_height = int(current_frame.get_height() * floating_scale_factor)
            small_frame = pygame.transform.scale(current_frame, (small_width, small_height))

            # Calculate rotation angle
            angle = (pygame.time.get_ticks() * rotation_speed) % 360  # Rotate over time
            rotated_frame = pygame.transform.rotate(small_frame, angle)

            # Adjust position for rotated image (since rotation changes the size)
            rotated_rect = rotated_frame.get_rect(center=(floating_x, floating_y))

            # Draw the rotated character
            screen.blit(rotated_frame, rotated_rect.topleft)
            
            # Blit nova at the bottom-right corner
            nova_original = pygame.image.load("assets/characters/NOVA.png").convert_alpha()  # Load the nova image
            nova_scaled = pygame.transform.scale(nova_original, (200, 200))  # Scale the nova image to 200x200
            nova_x = 0  # Position x to align nova in the bottom-right
            nova_y = 50  # Position y to align nova in the bottom-right
            screen.blit(nova_scaled, (nova_x, nova_y))  # Blit nova image

        if time_cutscene > 10010 and time_cutscene < 14000:
            draw_textbox("WHAT! Who are you? How do I escape?!", 20, 100)

            current_frame = frames[0][0]
            SCALE_FACTOR = 4
            scaled_width = current_frame.get_width() * SCALE_FACTOR
            scaled_height = current_frame.get_height() * SCALE_FACTOR
            scaled_frame = pygame.transform.scale(current_frame, (scaled_width, scaled_height))
            screen.blit(scaled_frame, (550, -100))

        elif time_cutscene > 14010 and time_cutscene < 23000:
            draw_textbox("Good morning, Player. I am NOVA, your Artificial Intelligence guide. Welcome to the escape room. Your mission is to solve puzzles and challenges, all while learning about the wonders—and risks—of AI. Failure to succeed will leave you here... indefinitely.", 210, 100)
            screen.blit(nova, (0, 75))

        elif time_cutscene > 24500 and time_cutscene < 30000:
            draw_textbox("Wait... what? Is this some kind of joke?", 20, 100)
            screen.blit(scaled_frame, (550, -100))
        
        elif time_cutscene > 31000 and time_cutscene < 35000:
            draw_textbox("I assure you, this is no joke. Let us begin. Your first task awaits.", 210, 100)
            screen.blit(nova, (0, 25))
        
        elif time_cutscene > 35200:
            room = "room1"  # Proceed to the first room
            start = True
            time_cutscene = 0

        if pygame.event.get(pygame.KEYDOWN):
            if pygame.key.get_pressed()[pygame.K_SPACE]:
                room = "room1"  # Go to the first room when space is pressed
                start = True
                time_cutscene = 0
        
    elif room == "room1":
        screen.fill((255, 0, 0))

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
    
    pygame.display.flip()
    clock.tick(30)

pygame.quit()
sys.exit()