import pygame

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
nova = pygame.image.load("assets/characters/NOVA.png")

# Resize the nova image to a smaller size
nova = pygame.transform.scale(nova, (200, 200))  # Example: Resize to 200x200 pixels

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Textbox")
clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.blit(nova, (50, 10))  # Blit the resized image
    pygame.display.flip()
    clock.tick(30)  # Limit to 30 FPS

pygame.quit()