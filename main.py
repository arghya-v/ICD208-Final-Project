import pygame, sys, math, time
from pygame.locals import QUIT
pygame.init()

# Screen dimensions and frame rate
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
pygame.display.set_caption("Escape The Algorithm")
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

# Load assets once
start_background = pygame.image.load("assets/images/start_background.jpg").convert()
start_background = pygame.transform.scale(start_background, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
door_sheet = pygame.image.load("assets/images/start-door.png").convert_alpha()
door_sheet = pygame.transform.scale(door_sheet, (door_sheet.get_width() * 8, door_sheet.get_height() * 9))
door_sheet_scaled = pygame.transform.scale(door_sheet, (door_sheet.get_width() // 4, door_sheet.get_height() // 4))
workscited_background = pygame.image.load("assets/images/scroll.png").convert_alpha()
workscited_background = pygame.transform.scale(workscited_background, (SCREEN_WIDTH, SCREEN_HEIGHT - 80))
cutscene_background = pygame.image.load("assets/images/cut_scene-background.png").convert()
cutscene_background = pygame.transform.scale(cutscene_background, (SCREEN_WIDTH, SCREEN_HEIGHT))
room1_background = pygame.image.load("assets/images/room_one-background.png").convert()
room1_background = pygame.transform.scale(room1_background, (room1_background.get_width()/6, SCREEN_HEIGHT))
nova = pygame.image.load("assets/characters/NOVA.png")
nova = pygame.transform.scale(nova, (200, 200))  # Resize to 200x200 pixels
original_spritesheet = pygame.image.load(f"assets/characters/1.png").convert_alpha()  # Load the spritesheet
book_inside = pygame.image.load("assets/images/room_one-book_inside.png").convert_alpha()
book_inside = pygame.transform.scale(book_inside, (SCREEN_WIDTH, SCREEN_HEIGHT))
pedistal = pygame.image.load("assets/images/room_one-pedistal.png").convert_alpha()
pedistal = pygame.transform.scale(pedistal, (SCREEN_WIDTH / 8, SCREEN_HEIGHT / 3))
book = pygame.image.load("assets/images/room_one-book.png").convert_alpha()
book = pygame.transform.scale(book, (SCREEN_WIDTH / 8.3, SCREEN_HEIGHT / 8.3))
key = pygame.image.load("assets/images/key.png").convert_alpha()
key = pygame.transform.scale(key, ((SCREEN_WIDTH * 0.7)/1.75, SCREEN_HEIGHT * 0.7))
room2_background = pygame.image.load("assets/images/room_two-background.png").convert()
computer = pygame.image.load("assets/images/room2computer.png").convert_alpha()
room3 = pygame.image.load("assets/images/room_three-background.png")
room3main = pygame.image.load('assets/images/room_three-inner_background.png')
suv = pygame.image.load('assets/images/room_three-suv.png')
truck = pygame.image.load('assets/images/room_three-truck.png')
box = pygame.image.load('assets/images/boxes.png')
motor = pygame.image.load('assets/images/room_three-motorcycle.png')
image_one = pygame.image.load('assets/images/room_two-people/1.png').convert()
image_two = pygame.image.load('assets/images/room_two-people/2.png').convert()
image_three = pygame.image.load('assets/images/room_two-people/3.png').convert()
image_four = pygame.image.load('assets/images/room_two-people/4.png').convert()
image_five = pygame.image.load('assets/images/room_two-people/5.png').convert()
image_six = pygame.image.load('assets/images/room_two-people/6.png').convert()
image_seven = pygame.image.load('assets/images/room_two-people/7.png').convert()
image_eight = pygame.image.load('assets/images/room_two-people/8.png').convert()
image_one = pygame.transform.scale(image_one, (600, 400))
image_two = pygame.transform.scale(image_two, (600, 400))
image_three = pygame.transform.scale(image_three, (600, 400))
image_four = pygame.transform.scale(image_four, (600, 400))
image_five = pygame.transform.scale(image_five, (600, 400))
image_six = pygame.transform.scale(image_six, (600, 400))
image_seven = pygame.transform.scale(image_seven, (600, 400))
image_eight = pygame.transform.scale(image_eight, (600, 400))

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
x, y = 10, 590  # Starting position | Initial sprite position and state:
direction = 3  # Default direction (DOWN)
charecter_frame_index = 0  # Current frame
charecter_frame_timer = 0  # Timer for frame updates
linecount = 0 # Used to add space between lines on help and works cited page.
SCALE_FACTOR = 8  # Scaling factor for the character Scale up the character size by 2x
time_cutscene = 0 # Used to time the cutscene
SPEED = 5
room1_completed = 0
qOne_done = False
qTwo_done = False
qThree_done = False
book_page = 0
computer_page = 0
computer_wrong = False
haskey = False
room2_completed = False

# Ensure scaled sheet has enough space for all frames and directions
scaled_width = TARGET_FRAME_WIDTH * CHARACTER_NUM_FRAMES
scaled_height = TARGET_FRAME_HEIGHT * NUM_DIRECTIONS
spritesheet = pygame.transform.scale(original_spritesheet, (scaled_width, scaled_height))

# Load fonts
Titlefont = pygame.font.SysFont("Comic Sans", 25, bold=True)
Titlefont.set_underline(True)
extraTitlefont = pygame.font.SysFont("Comic Sans", 40, bold=True)
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
    global start, x, y, start_frame_index, haskey, room2_completed
    if not start:
        return  # Skip processing if `start` is False

    if pygame.mixer.music.get_busy():
        pygame.mixer.music.fadeout(200) # set to 1000ms after we have fade for cleaner fade_out
    if not pygame.mixer.get_busy():
        # Determine the music to load based on the room
        music_files = {
            "start": "assets/bgm/bgm-works_cited_help.mp3",
            "work cited": "assets/bgm/bgm-extra.mp3",
            "help": "assets/bgm/bgm-extra.mp3",
            "cutscene": "assets/bgm/bgm-cut_scene.mp3",
            "room1": "assets/bgm/bgm-room_one.mp3",
            "book": "assets/bgm/bgm-room_one.mp3",
            "room2": "assets/bgm/bgm-room_two.mp3",
            "computer": "assets/bgm/bgm-room_two.mp3",
            "room3": "assets/bgm/bgm-room_three.mp3",
        }

        # Only load and play music if the room has a valid music file
        if room in music_files:
            new_music = music_files[room]
            pygame.mixer.music.load(new_music)
            pygame.mixer.music.set_volume(10)
            pygame.mixer.music.play(-1, 0.0, 4000) # set to 6000ms for cleaner fade after we have fade to black set up
        
        start = False
    if room == "cutscene":
        start_frame_index = 0
        haskey = False
    if room == "room1":
        x, y = -50, SCREEN_HEIGHT - 190
        haskey = False
        room2_completed = False
    elif room == "room2":
        x, y = 0, SCREEN_HEIGHT - 190
        haskey = False

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
            room = "room2"  # Proceed to the first room
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
        screen.blit(room1_background, (0,0))
        if not haskey:
            simple_text("WASD/Arrow keys to move.", 20, 20)
        if haskey:
            simple_text("Click on the door to use the key.", 20, 20)
            if y < 410:
                simple_text("Use key.", 485, 250)
            
            start_frame_index = 0
            # Door animation logic
            door_sheet_scaled = pygame.transform.scale(door_sheet, (door_sheet.get_width() // 4, door_sheet.get_height() // 4))
            door_frame_width = door_sheet_scaled.get_width() // START_NUM_FRAMES
            door_frame_height = door_sheet_scaled.get_height()
            door_pos = (470, 290)  # Adjust to position the door in Room 1

            # Calculate the crop rect for the current frame
            crop_rect = pygame.Rect(
                start_frame_index * door_frame_width, 0, 
                door_frame_width, door_frame_height
            )

            # Extract the current frame
            current_door_frame = door_sheet_scaled.subsurface(crop_rect)

            # Draw the current frame
            screen.blit(current_door_frame, door_pos)

            # Check if the mouse is over the door
            mouse_pos = pygame.mouse.get_pos()
            door_rect = pygame.Rect(door_pos[0], door_pos[1], door_frame_width, door_frame_height)

            if pygame.mouse.get_pressed()[0]:  # Check for left mouse button click
                if door_rect.collidepoint(mouse_pos):
                    if haskey:
                        room = "room2"  # Go to the second room when the door is clicked
                        start = True
                        room_start()
            
        ROOM1_X_MIN = -100
        ROOM1_X_MAX = SCREEN_WIDTH-pedistal.get_width()-170
        ROOM1_Y_MAX = SCREEN_HEIGHT - 190
        if x > 380 and x < 490:
            ROOM1_Y_MIN = 270
        else:
            ROOM1_Y_MIN = 390
        if  y >= 270 and y < 390:
            ROOM1_X_MIN = 381
            ROOM1_X_MAX = 489

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
        
        # Clamp position within boundaries
        x = max(ROOM1_X_MIN, min(x, ROOM1_X_MAX))
        y = max(ROOM1_Y_MIN, min(y, ROOM1_Y_MAX))
        
        # Update frame based on timer
        charecter_frame_timer += clock.get_time()
        if charecter_frame_timer > FRAME_RATE:
            charecter_frame_index = (charecter_frame_index + 1) % CHARACTER_NUM_FRAMES
            charecter_frame_timer = 0

        current_frame = frames[direction][charecter_frame_index]
        SCALE_FACTOR = 2.5
        scaled_width = current_frame.get_width() * SCALE_FACTOR
        scaled_height = current_frame.get_height() * SCALE_FACTOR
        scaled_frame = pygame.transform.scale(current_frame, (scaled_width, scaled_height))
        screen.blit(scaled_frame, (x, y))

        screen.blit(pedistal, (SCREEN_WIDTH-pedistal.get_width()-50, SCREEN_HEIGHT-pedistal.get_height()))
        screen.blit(book, (SCREEN_WIDTH-pedistal.get_width()-50, SCREEN_HEIGHT-pedistal.get_height()-book.get_height()+20))
        if x > SCREEN_WIDTH-pedistal.get_width()-300 and y > 390:
            simple_text("E to open book.", SCREEN_WIDTH-pedistal.get_width()-90, (SCREEN_HEIGHT-pedistal.get_height())-book.get_height()-20)
            if pygame.key.get_pressed()[pygame.K_e]:
                room = "book"
                start = False
        
    if room == "book":
        screen.blit(room1_background, (0, 0))
        screen.blit(book_inside, (0, 0))

        if book_page == 2 and room1_completed == 3:
            simple_text("ESC to go back, Click key to collect, QW to chnage pages", 10, 0)
        else:
            simple_text("ESC to go back, QW to chnage pages", 10, 0)
        if draw_button("Back", 10, SCREEN_HEIGHT-40, pygame.Color("gray67"), pygame.Color("gray50"), 100, 30, "white", 30):
            room = "room1"
            start = False

        if draw_button("Next Page", 600, 535, pygame.Color("gray67"), pygame.Color("gray50"), 100, 20, "white", 15):
            book_page += 1
            if book_page > 1:
                book_page = 1
        if draw_button("Previous Page", 100, 530, pygame.Color("gray67"), pygame.Color("gray50"), 100, 20, "white", 12):
            book_page -= 1
            if book_page < 0:
                book_page = 0

        if book_page == 0:
            book_text_surface = Titlefont.render("AI 101:", True, pygame.Color("black"))
            book_text_rect = book_text_surface.get_rect(centerx=245, centery=50)
            screen.blit(book_text_surface, book_text_rect)
            book_text_surface = Titlefont.render("A Beginner’s Guide", True, pygame.Color("black"))
            book_text_rect = book_text_surface.get_rect(centerx=245, centery=50+Titlefont.get_height())
            screen.blit(book_text_surface, book_text_rect)

            book_text_surface = font.render("Remember to read carefully.", True, pygame.Color("black"))
            book_text_rect = book_text_surface.get_rect(centerx=800-235, centery=50)
            screen.blit(book_text_surface, book_text_rect)
            book_text_surface = font.render("You will need this later.", True, pygame.Color("black"))
            book_text_rect = book_text_surface.get_rect(centerx=800-235, centery=50+font.get_height())
            screen.blit(book_text_surface, book_text_rect)

            book_bodytext = ["What is AI?",
                                "Artificial Intelligence (AI) is like giving computers the ability to think and solve problems, just like humans. AI helps machines recognize patterns, make decisions, and even talk to us, like when you ask a virtual assistant for help. To make AI work, scientists use huge amounts of data and special computer tools like GPUs (graphics processing units) that process information really quickly. AI can learn new things by practicing over and over, just like we do when we study for a test!"]
            linecount = 0
            for line in book_bodytext:
                draw_textbox(line, book_inside.get_rect().x+75, 100+Bodyfont.get_height()*linecount, False, Bodyfont, 250, "black", 60)
                linecount += 1
            
            book_bodytext = ["How AI Works", " ",
                                "AI is inspired by how our brains work. Inside our brains, we have billions of tiny cells called neurons that pass messages to each other. Scientists created artificial neurons to help computers learn in a similar way. These neurons work together in networks, helping AI figure out things like recognizing your face in photos or recommending a new video game you might like. All this happens using powerful hardware and lots of data to train the AI to think.",
                                " ", " ", " ", " ", " ", " ", " ", " ", " ", " ",
                                "Why AI Matters", " ",
                                "AI is super helpful, but it’s important to use it responsibly. If we don’t use enough good, fair data to teach an AI, it might make mistakes, like being unfair or making bad predictions. Sometimes, AI has to solve tricky problems, like deciding how a self-driving car should react in a dangerous situation. These are called ethical dilemmas, and they show why we need to think carefully about how we use AI. By learning about AI now, you can help shape a future where it makes life better for everyone!"]
            linecount = 0
            for line in book_bodytext:
                draw_textbox(line, book_inside.get_rect().x+350, 30+Bodyfont.get_height()*linecount, False, Bodyfont, 300, "black", 60)
                linecount += 1

        if book_page == 1:
            if qOne_done:
                draw_textbox("AI can solve problems and learn new things by practicing, just like humans.", 100, 50, False, font, 250, "darkgreen")
                if draw_button("True", 120, 150, pygame.Color("darkgreen"), pygame.Color("gray50"), 110, 25, "white", 20):
                    a = 0
            else:
                draw_textbox("AI can solve problems and learn new things by practicing, just like humans.", 100, 50, False, font, 250, "black")
                if draw_button("True", 120, 150, pygame.Color("gray67"), pygame.Color("gray50"), 110, 25, "white", 20):
                    qOne_done = True
                    room1_completed += 1
                elif draw_button("False", 240, 150, pygame.Color("gray67"), pygame.Color("gray50"), 110, 25, "white", 20):
                    if draw_button("False", 240, 150, pygame.Color("red"), pygame.Color("red"), 110, 25, "white", 20):
                        a= 0
                    draw_textbox("AI can solve problems and learn new things by practicing, just like humans.", 100, 50, False, font, 250, "red")
                    pygame.display.update()
                    pygame.time.wait(1000)
            
            if qTwo_done:
                draw_textbox("What part of the human brain inspired AI?", 100, 200, False, font, 250, "darkgreen")
                if draw_button("Neurons", 290, 260, pygame.Color("darkgreen"), pygame.Color("gray50"), 80, 20, "white", 15):
                    a = 0
            else:
                draw_textbox("What part of the human brain inspired AI?", 100, 200, False, font, 250, "black")
                if draw_button("Muscles", 110, 260, pygame.Color("gray67"), pygame.Color("gray50"), 80, 20, "white", 15):
                    if draw_button("Muscles", 110, 260, pygame.Color("red"), pygame.Color("red"), 80, 20, "white", 15):
                        a = 0
                    draw_textbox("What part of the human brain inspired AI?", 100, 200, False, font, 250, "red")
                    pygame.display.update()
                    pygame.time.wait(1000)
                elif draw_button("Bones", 200, 260, pygame.Color("gray67"), pygame.Color("gray50"), 80, 20, "white", 15):
                    if draw_button("Bones", 200, 260, pygame.Color("red"), pygame.Color("red"), 80, 20, "white", 15):
                        a = 0
                    draw_textbox("What part of the human brain inspired AI?", 100, 200, False, font, 250, "red")
                    pygame.display.update()
                    pygame.time.wait(1000)
                elif draw_button("Neurons", 290, 260, pygame.Color("gray67"), pygame.Color("gray50"), 80, 20, "white", 15):
                    qTwo_done = True
                    room1_completed += 1
                
            
            if qThree_done:
                draw_textbox("Which of the following are ethical dilemmas that AI might face?", 100, 300, False, font, 250, "darkgreen")
                if draw_button("Self-driving car reacts in an accident", 110, 420, pygame.Color("darkgreen"), pygame.Color("gray50"), 260, 30, "white", 11):
                    a = 0
            else:
                draw_textbox("Which of the following are ethical dilemmas that AI might face?", 100, 300, False, font, 250, "black")
                if draw_button("Recognizing patterns in data", 110, 380, pygame.Color("gray67"), pygame.Color("gray50"), 260, 30, "white", 15):
                    if draw_button("Recognizing patterns in data", 110, 380, pygame.Color("red"), pygame.Color("red"), 260, 30, "white", 15):
                        a = 0
                    draw_textbox("Which of the following are ethical dilemmas that AI might face?", 100, 300, False, font, 250, "red")
                    pygame.display.update()
                    pygame.time.wait(1000)
                elif draw_button("Self-driving car reacts in an accident", 110, 420, pygame.Color("gray67"), pygame.Color("gray50"), 260, 30, "white", 11):
                    qThree_done = True
                    room1_completed += 1
                elif draw_button("Picking your cereal for you.", 110, 460, pygame.Color("gray67"), pygame.Color("gray50"), 260, 30, "white", 15):
                    if draw_button("Picking your cereal for you.", 110, 460, pygame.Color("red"), pygame.Color("red"), 260, 30, "white", 15):
                        a = 0
                    draw_textbox("Which of the following are ethical dilemmas that AI might face?", 100, 300, False, font, 250, "red")
                    pygame.display.update()
                    pygame.time.wait(1000)
            


            if room1_completed == 3 and not haskey:
                key_rect = pygame.Rect(400, 100, key.get_width(), key.get_height())
                screen.blit(key, (400, 100))

                if key_rect.collidepoint(pygame.mouse.get_pos()):
                    if pygame.event.get(pygame.MOUSEBUTTONDOWN):
                        haskey = True

        if pygame.event.get(pygame.KEYDOWN):
            if pygame.key.get_pressed()[pygame.K_ESCAPE]:
                room = "room1"  # Go back to the start when escape is
                start = False
            elif pygame.key.get_pressed()[pygame.K_q]:
                book_page -= 1
                if book_page < 0:
                    book_page = 0
            elif pygame.key.get_pressed()[pygame.K_w]:
                book_page += 1
                if book_page > 1:
                    book_page = 1
        
    # Room 2 logic
    elif room == "room2":
        scaledrm2 = pygame.transform.scale(room2_background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        scaledpc = pygame.transform.scale(computer, (200, 200))
        screen.blit(scaledrm2, (0, 0))
        screen.blit(scaledpc, (400, 325))
        if room2_completed:
            if not haskey:
                key = pygame.transform.scale(key, (30, 50))
                screen.blit(key, (320, 300))
                simple_text("Click the key to collect.", 20, 20)

                key_rect = pygame.Rect(320, 300, key.get_width(), key.get_height())

                if key_rect.collidepoint(pygame.mouse.get_pos()):
                    if pygame.event.get(pygame.MOUSEBUTTONDOWN):
                        haskey = True
            # Door animation logic
            start_frame_index = 0
            door_sheet_scaled = pygame.transform.scale(door_sheet, (door_sheet.get_width() // 4, door_sheet.get_height() // 4))
            door_frame_width = door_sheet_scaled.get_width() // START_NUM_FRAMES
            door_frame_height = door_sheet_scaled.get_height()
            door_pos = (175, 320)  # Adjust to position the door in Room 2

            # Calculate the crop rect for the current frame
            crop_rect = pygame.Rect(
                start_frame_index * door_frame_width, 0, 
                door_frame_width, door_frame_height
            )

            # Extract the current frame
            current_door_frame = door_sheet_scaled.subsurface(crop_rect)

            # Draw the current frame
            screen.blit(current_door_frame, door_pos)

            # Check if the mouse is over the door
            mouse_pos = pygame.mouse.get_pos()
            door_rect = pygame.Rect(door_pos[0], door_pos[1], door_frame_width, door_frame_height)

            if pygame.mouse.get_pressed()[0]:  # Check for left mouse button click
                if door_rect.collidepoint(mouse_pos):
                    if haskey and room2_completed:
                        room = "room3"  # Go to the third room when the door is clicked
                        start = True
                        room_start()
        if haskey and room2_completed:
            simple_text("Click on the door to use the key.", 20, 20)

        # Define boundaries for Room 2
        ROOM2_X_MIN = 0
        ROOM2_X_MAX = SCREEN_WIDTH - 200 
        ROOM2_Y_MIN = SCREEN_HEIGHT - 290
        ROOM2_Y_MAX = SCREEN_HEIGHT - 90  

        
        keys = pygame.key.get_pressed()

        # Move horizontally and vertically based on keys pressed
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

        # Apply clamping after movement
        if x < ROOM2_X_MIN:
            x = ROOM2_X_MIN
        elif x > ROOM2_X_MAX:
            x = ROOM2_X_MAX

        if y < ROOM2_Y_MIN:
            y = ROOM2_Y_MIN
        elif y > ROOM2_Y_MAX:
            y = ROOM2_Y_MAX

        charecter_frame_timer += clock.get_time()
        if charecter_frame_timer > FRAME_RATE:
            charecter_frame_index = (charecter_frame_index + 1) % CHARACTER_NUM_FRAMES
            charecter_frame_timer = 0

        # Ensure current_frame is not None
        current_frame = frames[direction][charecter_frame_index]
        SCALE_FACTOR = 2.5
        scaled_width = current_frame.get_width() * SCALE_FACTOR
        scaled_height = current_frame.get_height() * SCALE_FACTOR
        scaled_frame = pygame.transform.scale(current_frame, (scaled_width, scaled_height))
        screen.blit(scaled_frame, (x, y))

        # Calculate distance between character and computer
        computer_center_x = 400 + 100  
        computer_center_y = 325 + 100  
        character_center_x = x + (scaled_width // 2)
        character_center_y = y + (scaled_height // 2)

        distance = ((computer_center_x - character_center_x) ** 2 + 
                    (computer_center_y - character_center_y) ** 2) ** 0.5

        # Check if the character is close to the computer
        INTERACT_DISTANCE = 60  # Adjust based on desired range
        if distance < INTERACT_DISTANCE:
            simple_text("Press E to interact", 520, 300)
        if keys[pygame.K_e] and distance < INTERACT_DISTANCE:
            room = "computer"  
            start = False

    elif room == "computer":
        screen.fill((0, 0, 255))
        if draw_button("Back", 20, 25, "azure4", "gray24", 100, 30, "white", 20):
            room = "room2"  # Go back to room2
            room2_completed = True

        if computer_page == 0:
            draw_textbox("Welcome to the computer. Here you can add data to the data set.", 250, 100, True, font, 300, "White")
            draw_textbox("You can also discard data from the data set.", 250, 250, True, font, 300, "White")
            draw_textbox("Make sure the data is diverse and represents everyone.", 250, 400, True, font, 300, "White")
            pygame.display.update()
            pygame.time.wait(10)
            pygame.time.wait(2000)
            computer_page += 1
        
        if computer_page == 1:
            screen.blit(image_one, (100, 100))
            if draw_button("Add to data set.", 50, 550, "aquamarine4", "aquamarine3", 300, 35, "white", 20):
                computer_page = 2
        
            if draw_button("Discard from data.", 450, 550, "brown4", "brown3", 300, 35, "white", 20):
                room = "inncorrect"

        if computer_page == 2:
            screen.blit(image_two, (100, 100))
            if draw_button("Add to data set.", 50, 550, "aquamarine4", "aquamarine3", 300, 35, "white", 20):
                computer_page += 1

            if draw_button("Discard from data.", 450, 550, "brown4", "brown3", 300, 35, "white", 20):
                room = "inncorrect"

        """
        if draw_button("Add to data set.", 50, 550, "aquamarine4", "aquamarine3", 300, 35, "white", 20):
            computer_page += 1
        
        if draw_button("Discard from data.", 450, 550, "brown4", "brown3", 300, 35, "white", 20):
            room = "inncorrect"
        """        

    elif room == "inncorrect":
        screen.fill((0, 0, 0))
        draw_textbox("Incorrect. Try again.", 200, 150, False, extraTitlefont, 500, "red")
        pygame.display.update()
        pygame.time.wait(10)
        pygame.time.wait(2000)
        room = "room2"
        start = False
    
    elif room == "room3":
        scaled3 = pygame.transform.scale(room3, (SCREEN_WIDTH, SCREEN_HEIGHT))
        mainbg = pygame.transform.scale(room3main, (SCREEN_WIDTH,SCREEN_HEIGHT))
        scaledsuv = pygame.transform.scale(suv, (300,300) )
        scaledtruck = pygame.transform.scale(truck, (800,800))
        screen.blit(mainbg, (0,0))
        screen.blit(scaledsuv, (100,220))
        screen.blit(scaledtruck, (180,-30))
        screen.blit(motor,(220,220))
        screen.blit(box, (600,200))
        screen.blit(box, (550,250))
        screen.blit(scaled3, (0,0))

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
    
    pygame.display.flip()
    clock.tick(30)

pygame.quit()

sys.exit()