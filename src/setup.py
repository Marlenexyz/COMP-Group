import pygame

def create_set_up_window(screen_height,screen_width):
    # Initialize the game
    pygame.init()

    # Set up the display
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Pong")

    # Set up the colors
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)

    # Set up the font with a larger size
    font_size = 72
    font = pygame.font.Font(None, font_size)

    # Main game loop
    running = True
    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    running = False

        # Fill the screen with black
        screen.fill(BLACK)

        # Render and display the text
        text = font.render("Pong Game", True, WHITE)
        text_rect = text.get_rect(center=(screen_width // 2, screen_height // 2))
        text2 = font.render("press Enter to continue", True, WHITE)
        text_rect2 = text2.get_rect(center=(screen_width // 2, screen_height // 2 + 150))
        screen.blit(text, text_rect)
        screen.blit(text2, text_rect2)

        # Update the display
        pygame.display.flip()

    # Quit the game
    # pygame.quit()

if __name__ == '__main__':
    create_set_up_window(600,800)
