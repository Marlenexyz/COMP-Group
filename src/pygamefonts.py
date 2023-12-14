import pygame
import sys

# Initialisiere Pygame
pygame.init()

# Setze die Bildschirmgröße
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Font Example')

def display_example_sentences(screen):
    """Display an example sentence for each available font."""
    fonts = pygame.font.get_fonts()
    screen.fill((255, 255, 255))  # Weißer Hintergrund

    y = 0
    for font_name in fonts:
        font = pygame.font.SysFont(font_name, 20)
        text_surface = font.render(f"{font_name}: The quick brown fox jumps over the lazy dog", True, (0, 0, 0))
        screen.blit(text_surface, (0, y))
        y += 30  # Zum nächsten Zeile wechseln

    pygame.display.flip()

# Schleife für das Anzeigen des Fensters
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    display_example_sentences(screen)
    pygame.display.update()
