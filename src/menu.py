import pygame


class Menu:
    def __init__(self,screen_height,screen_width):
        pygame.init()

        self.screen_height = screen_height
        self.screen_width = screen_width
        
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Main Menu")

        # Game variables
        self.game_paused = False
        self.menu_state = "main"

        # Define fonts
        self.font = pygame.font.SysFont("arialblack", 40)

        # Define colours
        self.BLACK = (255, 255, 255)

        # Create button instances
        self.play_button = {"text": "Play", "rect": pygame.Rect(self.screen_height/2, 0.15 * self.screen_width, 200, 50)}
        self.options_button = {"text": "Options", "rect": pygame.Rect(self.screen_height/2, 0.3 * self.screen_width, 200, 50)}
        self.quit_button = {"text": "Quit", "rect": pygame.Rect(self.screen_height/2, 0.45*self.screen_width, 200, 50)}
        self.video_button = {"text": "Video Settings", "rect": pygame.Rect(self.screen_height/2, 75, 200, 50)}
        self.audio_button = {"text": "Audio Settings", "rect": pygame.Rect(self.screen_height/2, 200, 200, 50)}
        self.keys_button = {"text": "Change Key Bindings", "rect": pygame.Rect(self.screen_height/2, 325, 200, 50)}
        self.back_button = {"text": "Back", "rect": pygame.Rect(self.screen_height/2, 450, 200, 50)}

    def draw_button(self, button):
        pygame.draw.rect(self.screen, (70, 70, 70), button["rect"])
        text_surface = self.font.render(button["text"], True, self.BLACK)
        text_rect = text_surface.get_rect(center=button["rect"].center)
        self.screen.blit(text_surface, text_rect)

    def draw_text(self, text, x, y):
        text_surface = self.font.render(text, True, self.BLACK)
        text_rect = text_surface.get_rect(center=(x, y))
        self.screen.blit(text_surface, text_rect)


    def isGamePaused(self):
        return self.game_paused
    
    def getScreenWidth(self):
        return self.screen_width

if __name__ == '__main__':
    # Game loop
    mainMenu = Menu(600,800)
    #Main menu state = True
    run = True
    while run:
        mainMenu.screen.fill((52, 78, 91))

        if mainMenu.menu_state == "main":
            # Draw main menu
            mainMenu.draw_button(mainMenu.play_button)
            mainMenu.draw_button(mainMenu.options_button)
            mainMenu.draw_button(mainMenu.quit_button)
        elif mainMenu.menu_state == "options":
            # Draw the different options buttons
            mainMenu.draw_button(mainMenu.video_button)
            mainMenu.draw_button(mainMenu.audio_button)
            mainMenu.draw_button(mainMenu.keys_button)
            mainMenu.draw_button(mainMenu.back_button)
        # elif mainMenu.menu_state == 'paused':


        # # Check if the game is paused
        # if mainMenu.isGamePaused():
        #     # Check menu state
        #     if mainMenu.menu_state == "main":
        #         # Draw pause screen buttons
        #         mainMenu.draw_button(mainMenu.play_button)
        #         mainMenu.draw_button(mainMenu.options_button)
        #         mainMenu.draw_button(mainMenu.quit_button)
        #     # Check if the options menu is open
        #     elif mainMenu.menu_state == "options":
        #         # Draw the different options buttons
        #         mainMenu.draw_button(mainMenu.video_button)
        #         mainMenu.draw_button(mainMenu.audio_button)
        #         mainMenu.draw_button(mainMenu.keys_button)
        #         mainMenu.draw_button(mainMenu.back_button)
        # else:
            

        # # Event handler
        # for event in pygame.event.get():
        #     if event.type == pygame.KEYDOWN:
        #         if event.key == pygame.K_SPACE:
        #             game_paused = not mainMenu.isGamePaused()
        #     elif event.type == pygame.QUIT:
        #         run = False

        pygame.display.update()

    pygame.quit()
