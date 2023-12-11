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
    
    def check_button_click(self, button):
        mouse_pos = pygame.mouse.get_pos()
        if button["rect"].collidepoint(mouse_pos):
            mouse_click = pygame.mouse.get_pressed()
            if mouse_click[0] and not button["clicked"]:  # Left mouse button clicked and button not already clicked
                button["clicked"] = True
                return True
            elif not mouse_click[0]:
                button["clicked"] = False  # Reset the clicked status when the mouse button is released
        return False

    def update_menu(self):
        self.screen.fill((52, 78, 91))

        if self.menu_state == "main":
            self.draw_button(self.play_button)
            self.draw_button(self.options_button)
            self.draw_button(self.quit_button)

            if self.check_button_click(self.play_button):
                print("Play button clicked!")
                self.menu_state = "play"

            elif self.check_button_click(self.options_button):
                print("Options button clicked!")
                self.menu_state = "options"
            elif self.check_button_click(self.quit_button):
                pygame.quit()
                exit()

        elif self.menu_state == "options":
            self.draw_button(self.video_button)
            self.draw_button(self.audio_button)
            self.draw_button(self.keys_button)
            self.draw_button(self.back_button)

            if self.check_button_click(self.video_button):
                print("Video Settings button clicked!")
            elif self.check_button_click(self.audio_button):
                print("Audio Settings button clicked!")
            elif self.check_button_click(self.keys_button):
                print("Change Key Bindings button clicked!")
            elif self.check_button_click(self.back_button):
                self.menu_state = "main"

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.game_paused = not self.isGamePaused()
            elif event.type == pygame.QUIT:
                pygame.quit()
                exit()

        pygame.display.update()

    def getStatus(self):
        return self.menu_state


if __name__ == '__main__':
    mainMenu = Menu(600, 800)
    run = True
    while run:
        mainMenu.update_menu()