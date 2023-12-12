import pygame
import time
import numpy as np

class PongGame:
    def __init__(self,screen_height,screen_width):
        # Initialize the game
        pygame.init()

        self.paused = True

        # Set up the display
        self.screen_height = screen_height
        self.screen_width = screen_width
        
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Pong")

        # Set up the colors
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.RED = (255, 0, 0)
        self.YELLOW = (255, 255, 0)
        
        # Set up the corners
        self.l_thickness = 15 * 2
        self.l_length = 50 * 2

        # Set up the paddles
        self.paddle_width = 10
        self.paddle_height = 60
        self.paddle_speed = 1
        self.player_a_paddle_x = 50
        self.player_a_paddle_y = (self.screen_height - self.paddle_height) // 2
        self.player_b_paddle_x = self.screen_width - self.paddle_width - 50
        self.player_b_paddle_y = (self.screen_height - self.paddle_height) // 2

        # Set up the ball
        self.ball_radius = 5

        self.initial_ball_speed = 3

        self.ball_speed_x = 3
        self.ball_speed_y = 3
        self.ball_x = self.screen_width // 2
        self.ball_y = self.screen_height // 2


        self.player_name_a = "Player A"
        self.player_name_b = "Player B"

        # Set up the score
        self.player_a_score = 0
        self.player_b_score = 0
        self.font = pygame.font.Font(None, 36)
        self.score_text = self.font.render("{}: {}     {}: {}".format(self.player_name_a, self.player_a_score, 
                                                                      self.player_name_b, self.player_b_score), True, self.BLACK)

        # Schreibe die Ball Geschwindigkeit
        self.ball_speed_text = self.font.render("Ball Speed: {}".format(self.ball_speed_x), True, self.BLACK)

    def setPlayerNameA(self,inputName):
        self.player_name_a = inputName
        self._update_score()

    def setPlayerNameB(self,inputName):
        self.player_name_b = inputName
        self._update_score()

    def togglePause(self):
        self.paused = not self.paused

    def isGamePaused(self):
        return self.paused

    # def setGamePaused(self,paused):
    #     self.paused = paused
    
    def _move_ball(self):
        self.ball_x += self.ball_speed_x
        self.ball_y += self.ball_speed_y

    def _check_collision_with_paddle(self):
        # Check for collisions with paddles
        if self.player_a_paddle_x <= self.ball_x <= self.player_a_paddle_x + self.paddle_width and self.player_a_paddle_y <= self.ball_y <= self.player_a_paddle_y + self.paddle_height:
            self.ball_speed_x *= -1
        if self.player_b_paddle_x >= self.ball_x >= self.player_b_paddle_x - self.paddle_width and self.player_b_paddle_y <= self.ball_y <= self.player_b_paddle_y + self.paddle_height:
            self.ball_speed_x *= -1

    def _check_collision_with_wall(self):
            # Check for collisions with walls
        if self.ball_y <= 0 or self.ball_y >= self.screen_height - self.ball_radius:
            self.ball_speed_y *= -1
        if self.ball_x <= 0:
            self.player_b_score += 1
            self.ball_x = self.screen_width // 2
            self.ball_y = self.screen_height // 2
        if self.ball_x >= self.screen_width - self.ball_radius:
            self.player_a_score += 1
            self.ball_x = self.screen_width // 2
            self.ball_y = self.screen_height // 2

    def _update_score(self):
        # Update the score text
        self.score_text = self.font.render("{}: {}     {}: {}".format(self.player_name_a, self.player_a_score, self.player_name_b,self.player_b_score), True, self.BLACK)


    def _draw_l_marker(self, x, y):
        # Vertical bar of the L
        pygame.draw.rect(self.screen, self.YELLOW, (x - self.l_thickness // 2, y - self.l_length // 2, self.l_thickness, self.l_length))
        # Horizontal bar of the L
        pygame.draw.rect(self.screen, self.YELLOW, (x - self.l_length // 2, y - self.l_thickness // 2, self.l_length, self.l_thickness))


    # def _draw_mouse(self, index_finger_x, index_finger_y):
    #     # Draw Finger as mouse
    #     pygame.draw.circle(self.screen, self.RED, (index_finger_x, index_finger_y), self.ball_radius)
    #     # Wenn der Circle über einem Button ist, und gepincht wird dann soll das als Klick gelten
    #     if index_finger_x is not None:
    #         pygame.draw.circle(self.screen, self.GREEN, (index_finger_x, index_finger_y), self.ball_radius)

    def finger_as_mouse(self, x, y, is_pinched):
        # Draw circle at the given coordinates
        pygame.draw.circle(self.screen, self.RED, (x, y), self.ball_radius)
        
        # Perform a click action if is_pinched is True
        if is_pinched:
            # Execute the click action (e.g., by simulating a mouse click event)
            pygame.mouse.set_pos(x, y)  # Move the mouse to the coordinates
            pygame.event.post(pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'button': 1, 'pos': (x, y)}))
            pygame.event.post(pygame.event.Event(pygame.MOUSEBUTTONUP, {'button': 1, 'pos': (x, y)}))

    def _draw_game(self):
        # Clear the screen
        self.screen.fill(self.WHITE)

        # Draw L-shaped marker function
        self._draw_l_marker(0, 0)
        self._draw_l_marker(self.screen_width, 0)
        self._draw_l_marker(0, self.screen_height)
        self._draw_l_marker(self.screen_width, self.screen_height)

        # Draw the paddles
        pygame.draw.rect(self.screen, self.BLACK, (self.player_a_paddle_x, self.player_a_paddle_y, self.paddle_width, self.paddle_height))
        pygame.draw.rect(self.screen, self.BLACK, (self.player_b_paddle_x, self.player_b_paddle_y, self.paddle_width, self.paddle_height))

        # Draw the ball
        pygame.draw.circle(self.screen, self.BLACK, (self.ball_x, self.ball_y), self.ball_radius)

        # Draw the score
        self.screen.blit(self.score_text, (self.screen_width // 2 - self.score_text.get_width() // 2, 10))
        # Draw current ball speed
        self.screen.blit(self.ball_speed_text, (self.screen_width // 2 - self.ball_speed_text.get_width() // 2, 50))

    def _draw_only_corners(self):
        # Clear the screen
        self.screen.fill(self.WHITE)

        # Draw L-shaped marker function
        self._draw_l_marker(0, 0)
        self._draw_l_marker(self.screen_width, 0)
        self._draw_l_marker(0, self.screen_height)
        self._draw_l_marker(self.screen_width, self.screen_height)

    def draw_countdown(self,countdown_value):
        self._draw_game()                               #to overwrite old counter value
        #increase the font size of the text
        self.font_countdown = pygame.font.Font(None, 100)
        countdown_text = self.font_countdown.render("{}".format(countdown_value), True, self.BLACK)
        self.screen.blit(countdown_text, (self.screen_width // 2 - countdown_text.get_width() // 2, self.screen_height // 2))
        pygame.display.flip()


    def move_paddle_left(self,fingertip_pos_left):
        if fingertip_pos_left is not None:  # Ensure the fingertip was detected
            fingertip_pos_left += (self.paddle_width // 2)
            self.player_a_paddle_y = max(min(fingertip_pos_left, self.screen_height - self.paddle_height), 0)

    def move_paddle_right(self,fingertip_pos_right):
        if fingertip_pos_right is not None:  # Ensure the fingertip was detected
            fingertip_pos_right += (self.paddle_width // 2)
            self.player_b_paddle_y = max(min(fingertip_pos_right, self.screen_height - self.paddle_height), 0)


        
    def move_paddles_by_keys(self):
        # Move the paddles
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and self.player_a_paddle_y > 0:
            self.player_a_paddle_y -= self.paddle_speed
        if keys[pygame.K_s] and self.player_a_paddle_y < self.screen_height - self.paddle_height:
            self.player_a_paddle_y += self.paddle_speed
        if keys[pygame.K_UP] and self.player_b_paddle_y > 0:
            self.player_b_paddle_y -= self.paddle_speed
        if keys[pygame.K_DOWN] and self.player_b_paddle_y < self.screen_height - self.paddle_height:
            self.player_b_paddle_y += self.paddle_speed

    def _calibrate_corners(self):
        # Define corner points
        corners = [(0, 0), (self.screen_width, 0), (0, self.screen_height), (self.screen_width, self.screen_height)]

        # Draw and store the corners
        corner_rects = []
        for corner in corners:
            rect = pygame.Rect(corner[0] - 5, corner[1] - 5, 10, 10)  # Erstelle ein Rechteck um die Ecke
            pygame.draw.rect(self.screen, self.YELLOW, rect)
            corner_rects.append(rect)

        pygame.display.flip()
        return corner_rects
    
    def setBallSpeed(self):
        value = 2
        if self.ball_speed_x < 0:
            self.ball_speed_x = -self.initial_ball_speed * value
        elif self.ball_speed_x > 0:
            self.ball_speed_x = self.initial_ball_speed * value
        if self.ball_speed_y < 0:
            self.ball_speed_y = -self.initial_ball_speed * value
        elif self.ball_speed_y > 0:
            self.ball_speed_y = self.initial_ball_speed * value


    def _update_ball_speed(self):
        self.ball_speed_text = self.font.render("Ball speed: " + str(self.ball_speed_x), True, self.BLACK)
        


    def run(self):       
        self._move_ball()
        self._check_collision_with_paddle()
        self._check_collision_with_wall()
        self._update_score()
        self._update_ball_speed()
        self._draw_game()
        self._calibrate_corners()
        

 

       


if __name__ == '__main__':
    # Game loop
    pong = PongGame(400,800)
    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pong.move_paddles_by_keys()  
        pong.run()

        # Update the display
        pygame.display.flip()
        
        time.sleep(0.005)

    # Quit the game
    pygame.quit()
