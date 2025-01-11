import pygame
import sys

# Initialize pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Game with Transition")
clock = pygame.time.Clock()

# Load and resize assets for introduction
nova = pygame.image.load("assets/characters/NOVA.png")
nova = pygame.transform.scale(nova, (200, 200))  # Resize to 200x200 pixels
font = pygame.font.SysFont("monospace", 18)
novaFont = pygame.font.SysFont("monospace", 36, bold=True)
buttonFont = pygame.font.SysFont("monospace", 24)

# Intro text
text = (
    "Good morning, Player. I am NOVA, your Artificial Intelligence guide. "
    "Welcome to the escape room. Your mission is to solve puzzles and challenges, "
    "all while learning about the wonders—and risks—of AI. Failure to succeed will "
    "leave you here... indefinitely."
)
nova_name = "NOVA"

# Button properties
button_text = "Continue"
button_width, button_height = 200, 50
button_x = (SCREEN_WIDTH - button_width) // 2
button_y = SCREEN_HEIGHT - button_height - 30  # 30px padding from the bottom

# Gameplay setup (scratchpad functionality)
FRAME_WIDTH, FRAME_HEIGHT = 128, 128
TARGET_FRAME_WIDTH, TARGET_FRAME_HEIGHT = 80, 80
NUM_FRAMES = 4
NUM_DIRECTIONS = 4
FRAME_RATE = 300  # Milliseconds per frame
SPEED = 5

original_spritesheet = pygame.image.load("assets/characters/2.png").convert_alpha()
scaled_width = TARGET_FRAME_WIDTH * NUM_FRAMES
scaled_height = TARGET_FRAME_HEIGHT * NUM_DIRECTIONS
spritesheet = pygame.transform.scale(original_spritesheet, (scaled_width, scaled_height))


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

x, y = 100, 300  # Starting position
direction = 0
frame_index = 0
frame_timer = 0

# Game states
STATE_INTRO = "intro"
STATE_GAMEPLAY = "gameplay"
game_state = STATE_INTRO


# Function to draw text box
def draw_textbox(text):
    max_width = SCREEN_WIDTH - 250
    words = text.split(" ")
    lines = []
    current_line = ""

    for word in words:
        test_line = current_line + " " + word if current_line else word
        test_surface = font.render(test_line, True, pygame.Color("white"))
        if test_surface.get_width() <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word
    if current_line:
        lines.append(current_line)

    text_height = len(lines) * font.get_height()
    rect_padding = 10
    rect_x = 20
    rect_y = 50
    rect_width = max_width + rect_padding * 2
    rect_height = text_height + rect_padding * 2

    pygame.draw.rect(screen, pygame.Color("white"), (rect_x, rect_y, rect_width, rect_height))
    pygame.draw.rect(screen, pygame.Color("black"),
                     (rect_x + 3, rect_y + 3, rect_width - 6, rect_height - 6))

    y_offset = rect_y + rect_padding
    for line in lines:
        txt_surface = font.render(line, True, pygame.Color("white"))
        screen.blit(txt_surface, (rect_x + rect_padding, y_offset))
        y_offset += font.get_height()


# Function to draw the button
def draw_button():
    pygame.draw.rect(screen, pygame.Color("white"), (button_x, button_y, button_width, button_height), border_radius=5)
    pygame.draw.rect(screen, pygame.Color("black"), (button_x + 2, button_y + 2, button_width - 4, button_height - 4),
                     border_radius=5)
    button_surface = buttonFont.render(button_text, True, pygame.Color("white"))
    button_text_x = button_x + (button_width - button_surface.get_width()) // 2
    button_text_y = button_y + (button_height - button_surface.get_height()) // 2
    screen.blit(button_surface, (button_text_x, button_text_y))


# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif game_state == STATE_INTRO and event.type == pygame.MOUSEBUTTONDOWN:
            if button_x <= event.pos[0] <= button_x + button_width and button_y <= event.pos[1] <= button_y + button_height:
                game_state = STATE_GAMEPLAY

    # Intro state
    if game_state == STATE_INTRO:
        screen.fill((0, 0, 0))
        screen.blit(nova, (600, 30))
        nova_text_surface = novaFont.render(nova_name, True, pygame.Color("white"))
        nova_text_x = 600 + (200 - nova_text_surface.get_width()) // 2
        nova_text_y = 200
        screen.blit(nova_text_surface, (nova_text_x, nova_text_y))
        draw_textbox(text)
        draw_button()

    # Gameplay state
    elif game_state == STATE_GAMEPLAY:
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

        frame_timer += clock.get_time()
        if frame_timer > FRAME_RATE:
            frame_index = (frame_index + 1) % NUM_FRAMES
            frame_timer = 0

        screen.fill((30, 30, 30))
        screen.blit(frames[direction][frame_index], (x, y))

    # Update the display
    pygame.display.flip()
    clock.tick(30)

pygame.quit()
sys.exit()
