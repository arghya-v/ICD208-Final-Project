import pygame
import sys

# Initialize pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600

# Load and resize the image
nova = pygame.image.load("character/characters/NOVA.png")
nova = pygame.transform.scale(nova, (200, 200))  # Resize to 200x200 pixels

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Textbox Example")
clock = pygame.time.Clock()

# Load a monospace font
font = pygame.font.SysFont("monospace", 18)
novaFont = pygame.font.SysFont("monospace", 36, bold=True)
# Pre-written text
text = (
    "Good morning, Player. I am NOVA, your Artificial Intelligence guide. "
    "Welcome to the escape room. Your mission is to solve puzzles and challenges, "
    "all while learning about the wonders—and risks—of AI. Failure to succeed will "
    "leave you here... indefinitely."
)

# Text for the name under the image
nova_name = "NOVA"


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
    pygame.draw.rect(screen, pygame.Color("black"),
                     (rect_x + 3, rect_y + 3, rect_width - 6, rect_height - 6))  # Inner white box (border effect)

    # Render each line and blit it to the screen
    y_offset = rect_y + rect_padding  # Starting Y position, adjusted for padding
    for line in lines:
        txt_surface = font.render(line, True, pygame.Color("white"))
        screen.blit(txt_surface, (rect_x + rect_padding, y_offset))  # Blit each line with padding inside the rectangle
        y_offset += font.get_height()  # Move the Y position down for the next line


# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the screen with black
    screen.fill((0, 0, 0))

    # Blit the resized image
    screen.blit(nova, (600, 30))

    # Render and blit NOVA's name under the image
    nova_text_surface = novaFont.render(nova_name, True, pygame.Color("white"))
    nova_text_x = 600 + (200 - nova_text_surface.get_width()) // 2  # Center the name under the image
    nova_text_y = 200  # Position below the image with a small gap
    screen.blit(nova_text_surface, (nova_text_x, nova_text_y))

    # Draw the static text with wrapping and the rectangle
    draw_textbox(text)

    # Update the display
    pygame.display.flip()
    clock.tick(30)  # Limit to 30 FPS

# Quit pygame
pygame.quit()
sys.exit()