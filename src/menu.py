import pygame


class Menu:
    def __init__(self,screen_height,screen_width):
        pygame.init()

        self.screen_height = screen_height
        self.screen_width = screen_width
        
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Pong")

        # Game variables
        self.game_paused = False
        self.menu_state = "setup"

        self.setIndexFingerPos(0, 0)

        # Define fonts
        self.font = pygame.font.SysFont("arialblack", 40)

        # Define colours
        self.WHITE = (255, 255, 255)
        self.RED = (255, 0, 0)
        self.BLACK = (0, 0, 0)

        ## Button instances dependant on screen size
        button_width, button_height = 200, 50

        # Calculate x-coordinate for centering buttons
        button_x = (self.screen_width - button_width) / 2

        total_button_height = 3 * button_height
        space_between_buttons = (self.screen_height - total_button_height) / 4

        self.play_button = {"text": "Play", "rect": pygame.Rect(button_x, space_between_buttons, button_width, button_height)}
        self.enter_player_names_button = {"text": "Names", "rect": pygame.Rect(button_x, space_between_buttons + 1 * (button_height + space_between_buttons), button_width, button_height)}
        self.quit_button = {"text": "Quit", "rect": pygame.Rect(button_x, space_between_buttons + 2 * (button_height + space_between_buttons), button_width, button_height)}


        self.playerNameA = "Player A"
        self.playerNameB = "Player B"
   
        # Virtuelle Tastaturbuttons
        button_width, button_height = 40, 40
        button_spacing = 50

        offset = 15

        # Create keyboard button instances
        self.keyboard_buttons = [
            {"text": "Q", "rect": pygame.Rect(screen_width // 10, screen_height - 150, button_width, button_height)},
            {"text": "W", "rect": pygame.Rect(screen_width // 10 + button_spacing, screen_height - 150, button_width, button_height)},
            {"text": "E", "rect": pygame.Rect(screen_width // 10 + 2 * button_spacing, screen_height - 150, button_width, button_height)},
            {"text": "R", "rect": pygame.Rect(screen_width // 10 + 3 * button_spacing, screen_height - 150, button_width, button_height)},
            {"text": "T", "rect": pygame.Rect(screen_width // 10 + 4 * button_spacing, screen_height - 150, button_width, button_height)},
            {"text": "Z", "rect": pygame.Rect(screen_width // 10 + 5 * button_spacing, screen_height - 150, button_width, button_height)},
            {"text": "U", "rect": pygame.Rect(screen_width // 10 + 6 * button_spacing, screen_height - 150, button_width, button_height)},
            {"text": "I", "rect": pygame.Rect(screen_width // 10 + 7 * button_spacing, screen_height - 150, button_width, button_height)},
            {"text": "O", "rect": pygame.Rect(screen_width // 10 + 8 * button_spacing, screen_height - 150, button_width, button_height)},
            {"text": "P", "rect": pygame.Rect(screen_width // 10 + 9 * button_spacing, screen_height - 150, button_width, button_height)},
            {"text": "A", "rect": pygame.Rect(screen_width // 10 + offset, screen_height - 100, button_width, button_height)},
            {"text": "S", "rect": pygame.Rect(screen_width // 10 + offset + button_spacing, screen_height - 100, button_width, button_height)},
            {"text": "D", "rect": pygame.Rect(screen_width // 10 + offset + 2 * button_spacing, screen_height - 100, button_width, button_height)},
            {"text": "F", "rect": pygame.Rect(screen_width // 10 + offset + 3 * button_spacing, screen_height - 100, button_width, button_height)},
            {"text": "G", "rect": pygame.Rect(screen_width // 10 + offset + 4 * button_spacing, screen_height - 100, button_width, button_height)},
            {"text": "H", "rect": pygame.Rect(screen_width // 10 + offset + 5 * button_spacing, screen_height - 100, button_width, button_height)},
            {"text": "J", "rect": pygame.Rect(screen_width // 10 + offset + 6 * button_spacing, screen_height - 100, button_width, button_height)},
            {"text": "K", "rect": pygame.Rect(screen_width // 10 + offset + 7 * button_spacing, screen_height - 100, button_width, button_height)},
            {"text": "L", "rect": pygame.Rect(screen_width // 10 + offset + 8 * button_spacing, screen_height - 100, button_width, button_height)},
            {"text": "Y", "rect": pygame.Rect(screen_width // 10 + 2* offset, screen_height - 50, button_width, button_height)},
            {"text": "X", "rect": pygame.Rect(screen_width // 10 + 2* offset + button_spacing, screen_height - 50, button_width, button_height)},
            {"text": "C", "rect": pygame.Rect(screen_width // 10 + 2* offset + 2 * button_spacing, screen_height - 50, button_width, button_height)},
            {"text": "V", "rect": pygame.Rect(screen_width // 10 + 2* offset + 3 * button_spacing, screen_height - 50, button_width, button_height)},
            {"text": "B", "rect": pygame.Rect(screen_width // 10 + 2* offset + 4 * button_spacing, screen_height - 50, button_width, button_height)},
            {"text": "N", "rect": pygame.Rect(screen_width // 10 + 2* offset + 5 * button_spacing, screen_height - 50, button_width, button_height)},
            {"text": "M", "rect": pygame.Rect(screen_width // 10 + 2* offset + 6 * button_spacing, screen_height - 50, button_width, button_height)},
            {"text": "Enter", "rect": pygame.Rect(screen_width // 10 + 2* offset + 7 * button_spacing, screen_height - 50, 150, button_height)},
        ]

        # Input field variables for entering player names
        self.input_active = False
        self.input_text = ""
        self.input_rect = pygame.Rect(self.screen_width // 2 - 100, 500, 200, 50)       #del?
        # self.input_color_inactive = pygame.Color('lightskyblue3')
        self.input_color_inactive = pygame.Color(0,0,0)
        self.input_color_active = pygame.Color('dodgerblue2')
        self.input_color = self.input_color_inactive
        self.input_active = False

        
        self.input_field = {"text": "", "rect": pygame.Rect(self.screen_height/2, 0.25 * self.screen_width, 200, 50)}
        # Zusätzlicher Text über dem input_field
        self.additional_text = {"text": "Enter player name:", "rect": pygame.Rect(screen_height/2, 0.15 * screen_width - 50, 200, 50)}

        self.selected_input_field = "input_field_A"

        self.pinch_click = False
        
    def create_set_up_window(self):

        # Set up the font with a larger size
        font_size = 72
        font = pygame.font.Font(None, font_size)
        font_small = pygame.font.Font(None, font_size // 2)
        
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.menu_state = 'main'

        # Fill the screen with black
        self.screen.fill(self.BLACK)

        # Render and display the text
        text = font.render("Pong Game", True, self.WHITE)
        text_rect = text.get_rect(center=(self.screen_width // 2, self.screen_height // 2))
        text2 = font_small.render("press Enter to continue", True, self.WHITE)
        text_rect2 = text2.get_rect(center=(self.screen_width // 2, self.screen_height // 2 + 150))
        self.screen.blit(text, text_rect)
        self.screen.blit(text2, text_rect2)

        # Update the display
        pygame.display.flip()

    def __del__(self):
        pygame.quit()
        
    def draw_keyboard(self):
        for button in self.keyboard_buttons:
            pygame.draw.rect(self.screen, self.BLACK, button["rect"])
            pygame.draw.rect(self.screen, self.WHITE, button["rect"], 2)
            text_surface = self.font.render(button["text"], True, self.WHITE)
            text_rect = text_surface.get_rect(center=button["rect"].center)
            self.screen.blit(text_surface, text_rect)
            

    def draw_button(self, button):
        pygame.draw.rect(self.screen, self.BLACK, button["rect"])
        pygame.draw.rect(self.screen, self.WHITE, button["rect"], 2)    # 2 Bixel Breite ums Feld
        text_surface = self.font.render(button["text"], True, self.WHITE)
        text_rect = text_surface.get_rect(center=button["rect"].center)
        self.screen.blit(text_surface, text_rect)

    def draw_text(self, text, x, y):
        text_surface = self.font.render(text, True, self.WHITE)
        text_rect = text_surface.get_rect(center=(x, y))
        self.screen.blit(text_surface, text_rect)


    def isGamePaused(self):
        return self.game_paused
    
    def getScreenWidth(self):
        return self.screen_width
    
    def toggle_input_active(self):
        self.input_active = not self.input_active    
 
    
    def draw_input_field(self, input_field, additional_text):
        # Zusätzlicher Text über dem input_field
        text_surface = self.font.render(additional_text["text"], True, self.WHITE)
        text_rect = text_surface.get_rect(center=additional_text["rect"].center)
        self.screen.blit(text_surface, text_rect)

        pygame.draw.rect(self.screen, self.BLACK, input_field["rect"])  # Schwarzes Rechteck für das Eingabefeld 
        pygame.draw.rect(self.screen, self.WHITE, input_field["rect"], 2)  # Weißer Rand um das Eingabefeld

        text_surface = self.font.render(input_field["text"], True, self.WHITE)
        text_rect = text_surface.get_rect(center=input_field["rect"].center)
        self.screen.blit(text_surface, text_rect)

    def update_menu(self):
        self.screen.fill(self.BLACK)

        if self.menu_state == "main":
            self.draw_button(self.play_button)
            self.draw_button(self.quit_button)
            self.draw_button(self.enter_player_names_button)

            # if self.check_pinch_button_click(self.play_button):
            if self.check_button_click(self.play_button) or self.check_pinch_button_click(self.play_button):
                print("Play button clicked!")
                self.menu_state = "play"
    
            elif self.check_button_click(self.enter_player_names_button) or self.check_pinch_button_click(self.enter_player_names_button):
                self.menu_state = "enterNames"

            elif self.check_button_click(self.quit_button) or self.check_pinch_button_click(self.quit_button):
                pygame.quit()
                exit()
                
        elif self.menu_state == 'enterNames':
            self.draw_input_field(self.input_field, self.additional_text)
            self.draw_keyboard()

            self.add_letter_to_input_field()
            self.add_letter_to_input_field_via_pinch()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:   
                    pygame.quit()
                    exit()

              # Setze das Flag für Mausklicks zurück
            # self.mouse_clicked = False
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.game_paused = not self.isGamePaused()
            elif event.type == pygame.QUIT:
                pygame.quit()
                exit()
        self.draw_mouse()           # Zeichne den Finger als Mouse
        pygame.display.update()


    def add_letter_to_input_field(self):
        for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.keyboard_buttons[1]["rect"].collidepoint(event.pos):
                        self.input_field["text"] += 'W'  # Füge den Buchstaben 'W' zum input_field hinzu
                    if self.keyboard_buttons[2]["rect"].collidepoint(event.pos):
                        self.input_field["text"] += 'E'  # Füge den Buchstaben 'E' zum input_field hinzu
                    if self.keyboard_buttons[3]["rect"].collidepoint(event.pos):
                        self.input_field["text"] += 'R'  # Füge den Buchstaben 'R' zum input_field hinzu
                    if self.keyboard_buttons[4]["rect"].collidepoint(event.pos):
                        self.input_field["text"] += 'T'  # Füge den Buchstaben 'T' zum input_field hinzu
                    if self.keyboard_buttons[5]["rect"].collidepoint(event.pos):
                        self.input_field["text"] += 'Z'  # Füge den Buchstaben 'Z' zum input_field hinzu
                    if self.keyboard_buttons[6]["rect"].collidepoint(event.pos):
                        self.input_field["text"] += 'U'  # Füge den Buchstaben 'U' zum input_field hinzu
                    if self.keyboard_buttons[7]["rect"].collidepoint(event.pos):
                        self.input_field["text"] += 'I'  # Füge den Buchstaben 'I' zum input_field hinzu
                    if self.keyboard_buttons[8]["rect"].collidepoint(event.pos):
                        self.input_field["text"] += 'O'  # Füge den Buchstaben 'O' zum input_field hinzu
                    if self.keyboard_buttons[9]["rect"].collidepoint(event.pos):
                        self.input_field["text"] += 'P'  # Füge den Buchstaben 'P' zum input_field hinzu
                    if self.keyboard_buttons[10]["rect"].collidepoint(event.pos):
                        self.input_field["text"] += 'A'  # Füge den Buchstaben 'A' zum input_field hinzu
                    if self.keyboard_buttons[11]["rect"].collidepoint(event.pos):
                        self.input_field["text"] += 'S'  # Füge den Buchstaben 'S' zum input_field hinzu
                    if self.keyboard_buttons[12]["rect"].collidepoint(event.pos):
                        self.input_field["text"] += 'D'  # Füge den Buchstaben 'D' zum input_field hinzu
                    if self.keyboard_buttons[13]["rect"].collidepoint(event.pos):
                        self.input_field["text"] += 'F'  # Füge den Buchstaben 'F' zum input_field hinzu
                    if self.keyboard_buttons[14]["rect"].collidepoint(event.pos):
                        self.input_field["text"] += 'G'  # Füge den Buchstaben 'G' zum input_field hinzu
                    if self.keyboard_buttons[15]["rect"].collidepoint(event.pos):
                        self.input_field["text"] += 'H'  # Füge den Buchstaben 'H' zum input_field hinzu
                    if self.keyboard_buttons[16]["rect"].collidepoint(event.pos):
                        self.input_field["text"] += 'J'  # Füge den Buchstaben 'J' zum input_field hinzu
                    if self.keyboard_buttons[17]["rect"].collidepoint(event.pos):
                        self.input_field["text"] += 'K'  # Füge den Buchstaben 'K' zum input_field hinzu
                    if self.keyboard_buttons[18]["rect"].collidepoint(event.pos):
                        self.input_field["text"] += 'L'  # Füge den Buchstaben 'L' zum input_field hinzu
                    if self.keyboard_buttons[19]["rect"].collidepoint(event.pos):
                        self.input_field["text"] += 'Z'  # Füge den Buchstaben 'Z' zum input_field hinzu
                    if self.keyboard_buttons[20]["rect"].collidepoint(event.pos):
                        self.input_field["text"] += 'X'  # Füge den Buchstaben 'X' zum input_field hinzu
                    if self.keyboard_buttons[21]["rect"].collidepoint(event.pos):
                        self.input_field["text"] += 'C'  # Füge den Buchstaben 'C' zum input_field hinzu
                    if self.keyboard_buttons[22]["rect"].collidepoint(event.pos):
                        self.input_field["text"] += 'V'  # Füge den Buchstaben 'V' zum input_field hinzu
                    if self.keyboard_buttons[23]["rect"].collidepoint(event.pos):
                        self.input_field["text"] += 'B'  # Füge den Buchstaben 'B' zum input_field hinzu
                    if self.keyboard_buttons[24]["rect"].collidepoint(event.pos):
                        self.input_field["text"] += 'N'  # Füge den Buchstaben 'N' zum input_field hinzu
                    if self.keyboard_buttons[25]["rect"].collidepoint(event.pos):
                        self.input_field["text"] += 'M'  # Füge den Buchstaben 'M' zum input_field hinzu
                    if self.keyboard_buttons[26]["rect"].collidepoint(event.pos):
                        if self.selected_input_field == "input_field_A":
                            self.playerNameA = self.input_field["text"]
                            # self.input_
                            self.input_field["text"] = ''
                            self.selected_input_field = "input_field_B"     #Switch to input_field_B
                            # self.selected_input_field = self.input_field_B
                        elif self.selected_input_field == "input_field_B":
                            self.playerNameB = self.input_field["text"]
                            self.menu_state = "main"

    def add_letter_to_input_field_via_pinch(self):
        if self.check_pinch_button_click(self.keyboard_buttons[1]):
            self.input_field["text"] += 'W'  # Füge den Buchstaben 'W' zum input_field hinzu
        if self.check_pinch_button_click(self.keyboard_buttons[2]):
            self.input_field["text"] += 'E'  # Füge den Buchstaben 'E' zum input_field hinzu
        if self.check_pinch_button_click(self.keyboard_buttons[3]):
            self.input_field["text"] += 'R'  # Füge den Buchstaben 'R' zum input_field hinzu
        if self.check_pinch_button_click(self.keyboard_buttons[4]):
            self.input_field["text"] += 'T'  # Füge den Buchstaben 'T' zum input_field hinzu
        if self.check_pinch_button_click(self.keyboard_buttons[5]):
            self.input_field["text"] += 'Z'  # Füge den Buchstaben 'Z' zum input_field hinzu
        if self.check_pinch_button_click(self.keyboard_buttons[6]):
            self.input_field["text"] += 'U'  # Füge den Buchstaben 'U' zum input_field hinzu
        if self.check_pinch_button_click(self.keyboard_buttons[7]):
            self.input_field["text"] += 'I'  # Füge den Buchstaben 'I' zum input_field hinzu
        if self.check_pinch_button_click(self.keyboard_buttons[8]):
            self.input_field["text"] += 'O'  # Füge den Buchstaben 'O' zum input_field hinzu
        if self.check_pinch_button_click(self.keyboard_buttons[9]):
            self.input_field["text"] += 'P'  # Füge den Buchstaben 'P' zum input_field hinzu
        if self.check_pinch_button_click(self.keyboard_buttons[10]):
            self.input_field["text"] += 'A'  # Füge den Buchstaben 'A' zum input_field hinzu
        if self.check_pinch_button_click(self.keyboard_buttons[11]):
            self.input_field["text"] += 'S'  # Füge den Buchstaben 'S' zum input_field hinzu
        if self.check_pinch_button_click(self.keyboard_buttons[12]):
            self.input_field["text"] += 'D'  # Füge den Buchstaben 'D' zum input_field hinzu
        if self.check_pinch_button_click(self.keyboard_buttons[13]):
            self.input_field["text"] += 'F'  # Füge den Buchstaben 'F' zum input_field hinzu
        if self.check_pinch_button_click(self.keyboard_buttons[14]):
            self.input_field["text"] += 'G'  # Füge den Buchstaben 'G' zum input_field hinzu
        if self.check_pinch_button_click(self.keyboard_buttons[15]):
            self.input_field["text"] += 'H'  # Füge den Buchstaben 'H' zum input_field hinzu
        if self.check_pinch_button_click(self.keyboard_buttons[16]):
            self.input_field["text"] += 'J'  # Füge den Buchstaben 'J' zum input_field hinzu
        if self.check_pinch_button_click(self.keyboard_buttons[17]):
            self.input_field["text"] += 'K'  # Füge den Buchstaben 'K' zum input_field hinzu
        if self.check_pinch_button_click(self.keyboard_buttons[18]):
            self.input_field["text"] += 'L'  # Füge den Buchstaben 'L' zum input_field hinzu
        if self.check_pinch_button_click(self.keyboard_buttons[19]):
            self.input_field["text"] += 'Z'  # Füge den Buchstaben 'Z' zum input_field hinzu
        if self.check_pinch_button_click(self.keyboard_buttons[20]):
            self.input_field["text"] += 'X'  # Füge den Buchstaben 'X' zum input_field hinzu
        if self.check_pinch_button_click(self.keyboard_buttons[21]):
            self.input_field["text"] += 'C'  # Füge den Buchstaben 'C' zum input_field hinzu
        if self.check_pinch_button_click(self.keyboard_buttons[22]):
            self.input_field["text"] += 'V'  # Füge den Buchstaben 'V' zum input_field hinzu
        if self.check_pinch_button_click(self.keyboard_buttons[23]):
            self.input_field["text"] += 'B'  # Füge den Buchstaben 'B' zum input_field hinzu
        if self.check_pinch_button_click(self.keyboard_buttons[24]):
            self.input_field["text"] += 'N'  # Füge den Buchstaben 'N' zum input_field hinzu
        if self.check_pinch_button_click(self.keyboard_buttons[25]):
            self.input_field["text"] += 'M'  # Füge den Buchstaben 'M' zum input_field hinzu
        if self.check_pinch_button_click(self.keyboard_buttons[26]):
            if self.selected_input_field == "input_field_A":
                self.playerNameA = self.input_field["text"]
                # self.input_
                self.input_field["text"] = ''
                self.selected_input_field = "input_field_B"     #Switch to input_field_B
                # self.selected_input_field = self.input_field_B
            elif self.selected_input_field == "input_field_B":
                self.playerNameB = self.input_field["text"]
                self.menu_state = "main"

    def getStatus(self):
        return self.menu_state
    
    def getPlayerNameA(self):
        return self.playerNameA
    
    def getPlayerNameB(self):
        return self.playerNameB
    
    def setIndexFingerPos(self, x, y):
        self.IndexFingerPos = (x, y)

    def getIndexFingerPos(self):
        return self.IndexFingerPos

    def setIsPinched(self, is_pinched):
        self.isPinched = is_pinched

    def getIsPinched(self):
        return self.isPinched
    
    def finger_as_mouse(self, x, y, is_pinched):
        # Draw circle at the given coordinates
        self.mouse = pygame.draw.circle(self.screen, self.RED, (x, y), 15)
        # pygame.display.flip()     #malt alles
        pygame.display.update()     # malt nur änderungen
        self.setIndexFingerPos(x, y)
        self.setIsPinched(is_pinched)
        

    def draw_mouse(self):          
        self.mouse = pygame.draw.circle(self.screen, self.RED, (self.IndexFingerPos[0], self.IndexFingerPos[1]), 15)
        pygame.display.update()

    def check_pinch_button_click(self,button):
        x,y = self.getIndexFingerPos()
        if self.hand_button_collision(button, x, y) and self.getIsPinched():        # If Collision and Pinched True
            return True
        else:
            return False
        

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

    def hand_button_collision(self,button,x,y):
        self.get_button_position(button)
        if button["rect"].collidepoint(x,y):            #Gibt zurück ob x,y, innerhalb button rect liegt
            return True
        

    def get_button_position(self,button):          
        'returns top left corner of button'
        return button["rect"].topleft


if __name__ == '__main__':
    mainMenu = Menu(600, 800)
    run = True
    while run:
        mainMenu.update_menu()