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
        self.RED = (255, 0, 0)


        ## Button instances dependant on screen size
        button_width, button_height = 200, 50

        # Calculate x-coordinate for centering buttons
        button_x = (self.screen_width - button_width) / 2

        total_button_height = 4 * button_height
        space_between_buttons = (self.screen_height - total_button_height) / 5

        self.play_button = {"text": "Play", "rect": pygame.Rect(button_x, space_between_buttons, button_width, button_height)}
        self.options_button = {"text": "Options", "rect": pygame.Rect(button_x, space_between_buttons + (button_height + space_between_buttons), button_width, button_height)}
        self.enter_player_names_button = {"text": "Enter Names", "rect": pygame.Rect(button_x, space_between_buttons + 2 * (button_height + space_between_buttons), button_width, button_height)}
        self.quit_button = {"text": "Quit", "rect": pygame.Rect(button_x, space_between_buttons + 3 * (button_height + space_between_buttons), button_width, button_height)}
        self.video_button = {"text": "Video Settings", "rect": pygame.Rect(button_x, space_between_buttons + 4 * (button_height + space_between_buttons), button_width, button_height)}
        self.audio_button = {"text": "Audio Settings", "rect": pygame.Rect(button_x, space_between_buttons + 5 * (button_height + space_between_buttons), button_width, button_height)}
        self.keys_button = {"text": "Change Key Bindings", "rect": pygame.Rect(button_x, space_between_buttons + 6 * (button_height + space_between_buttons), button_width, button_height)}
        self.back_button = {"text": "Back", "rect": pygame.Rect(button_x, space_between_buttons + 7 * (button_height + space_between_buttons), button_width, button_height)}

        
        
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
            {"text": "Enter", "rect": pygame.Rect(screen_width // 10 + 2* offset + 9 * button_spacing, screen_height - 50, 150, button_height)},
        ]

        # Input field variables for entering player names
        self.input_active = False
        self.input_text = ""
        self.input_rect = pygame.Rect(self.screen_width // 2 - 100, 500, 200, 50)       #del?
        self.input_color_inactive = pygame.Color('lightskyblue3')
        self.input_color_active = pygame.Color('dodgerblue2')
        self.input_color = self.input_color_inactive
        self.input_active = False

        
        self.input_field = {"text": "", "rect": pygame.Rect(self.screen_height/2, 0.35 * self.screen_width, 200, 50)}
        # self.input_field_B = {"text": "", "rect": pygame.Rect(self.screen_height/2, 0.35 * self.screen_width, 200, 50)}
        # Zusätzlicher Text über dem input_field
        self.additional_text_A = {"text": "Enter player name:", "rect": pygame.Rect(screen_height/2, 0.30 * screen_width - 50, 200, 50)}

        self.selected_input_field = "input_field_A"

    def __del__(self):
        pygame.quit()
        
    def draw_keyboard(self):
        for button in self.keyboard_buttons:
            pygame.draw.rect(self.screen, (70, 70, 70), button["rect"])
            text_surface = self.font.render(button["text"], True, self.BLACK)
            text_rect = text_surface.get_rect(center=button["rect"].center)
            self.screen.blit(text_surface, text_rect)
            

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
    
    def toggle_input_active(self):
        self.input_active = not self.input_active

    def update_input_active(self, event):
        if self.menu_state == "enterNames":
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Überprüfe, ob die Maus im Eingabefeld liegt, um es zu aktivieren oder deaktivieren
                #Sollte eigentlich automatisch active sein
                if self.input_field["rect"].collidepoint(event.pos):
                    self.toggle_input_active()
                else:
                    self.input_active = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    # Enter-Taste wurde gedrückt, um die Eingabe zu bestätigen
                    print("Entered text:", self.input_field["text"])
                    self.menu_state = "main"  # Hier könntest du die Logik für die Textverarbeitung implementieren
                elif event.key == pygame.K_BACKSPACE:
                    # Backspace-Taste wurde gedrückt, um das letzte Zeichen zu entfernen
                    self.input_field["text"] = self.input_field["text"][:-1]
                elif event.key == pygame.K_ESCAPE:
                    # Escape-Taste wurde gedrückt, um die Eingabe zu deaktivieren
                    self.input_active = False
                else:
                    # Füge das gedrückte Zeichen zur Eingabe hinzu
                    self.input_field["text"] += event.unicode
    
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
    
    def draw_input_field(self, input_field, additional_text):
        # Zusätzlicher Text über dem input_field
        text_surface = self.font.render(additional_text["text"], True, self.BLACK)
        text_rect = text_surface.get_rect(center=additional_text["rect"].center)
        self.screen.blit(text_surface, text_rect)

        pygame.draw.rect(self.screen, (0, 0, 0), input_field["rect"])  # Weißes Rechteck für das Eingabefeld (255,255,255)
        pygame.draw.rect(self.screen, (0, 0, 0), input_field["rect"], 2)  # Schwarzer Rand um das Eingabefeld

        text_surface = self.font.render(input_field["text"], True, self.BLACK)
        text_rect = text_surface.get_rect(center=input_field["rect"].center)
        self.screen.blit(text_surface, text_rect)

    def update_menu(self):
        self.screen.fill((52, 78, 91))

        if self.menu_state == "main":
            self.draw_button(self.play_button)
            self.draw_button(self.options_button)
            self.draw_button(self.quit_button)
            self.draw_button(self.enter_player_names_button)

            if self.check_button_click(self.play_button):
                print("Play button clicked!")
                self.menu_state = "play"

            elif self.check_button_click(self.options_button):
                print("Options button clicked!")
                self.menu_state = "options"
    
            elif self.check_button_click(self.enter_player_names_button):
                self.menu_state = "enterNames"

            elif self.check_button_click(self.quit_button):
                pygame.quit()
                exit()
                
        elif self.menu_state == 'enterNames':
            self.draw_input_field(self.input_field, self.additional_text_A)
            self.draw_keyboard()

            # if self.input_active:
            #     # Logik zum Hinzufügen von Buchstaben zur input_text-Zeichenkette hier hinzufügen
            #     pass

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                        
                        self.add_letter_to_input_field(event)
                        
                elif event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                elif self.menu_state == "options":
                    self.draw_button(self.video_button)
                    self.draw_button(self.audio_button)
                    self.draw_button(self.keys_button)
                    # self.draw_button(self.enter_player_names_button)
                    self.draw_button(self.back_button)
                    if self.check_button_click(self.video_button):
                        print("Video Settings button clicked!")
                    elif self.check_button_click(self.audio_button):
                        print("Audio Settings button clicked!")
                    elif self.check_button_click(self.keys_button):
                        print("Change Key Bindings button clicked!")
                    elif self.check_button_click(self.back_button):
                        self.menu_state = "main"
              # Setze das Flag für Mausklicks zurück
            self.mouse_clicked = False
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.game_paused = not self.isGamePaused()
            elif event.type == pygame.QUIT:
                pygame.quit()
                exit()
        # for event in pygame.event.get():
        #     if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
        #         self.update_input_active(event)

        pygame.display.update()

    def add_letter_to_input_field(self,event):
        if self.keyboard_buttons[0]["rect"].collidepoint(event.pos):
            self.input_field["text"] += 'Q' 
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
            self.input_field["text"] += 'C'  # Fü
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

    def getStatus(self):
        return self.menu_state
    
    def getPlayerNameA(self):
        return self.playerNameA
    
    def getPlayerNameB(self):
        return self.playerNameB
    
    # def _draw_mouse(self, index_finger_x, index_finger_y):
    #     # Draw Finger as mouse
    #     pygame.draw.circle(self.screen, self.RED, (index_finger_x, index_finger_y), self.ball_radius)
    #     # Wenn der Circle über einem Button ist, und gepincht wird dann soll das als Klick gelten
    #     if index_finger_x is not None:
    #         pygame.draw.circle(self.screen, self.GREEN, (index_finger_x, index_finger_y), self.ball_radius)

    def finger_as_mouse(self, x, y, is_pinched):
        # Draw circle at the given coordinates
        mouse = pygame.draw.circle(self.screen, self.RED, (x, y), 15)
        # pygame.display.flip()
        pygame.display.update()
        
        
        # Perform a click action if is_pinched is True
        if is_pinched:
            self.check_pinch_button_click(x,y)
            # and self.hand_button_collision(self.play_button, x, y):
            # self.menu_state = "play"
            # pygame.display.update()

    def check_pinch_button_click(self,x,y):
        if self.hand_button_collision(self.play_button, x, y):
            self.menu_state = "play"
            pygame.display.update()

        

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