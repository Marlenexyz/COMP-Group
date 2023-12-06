from typing import Any
import pygame
import random
import time
import numpy as np

class PongGame:
    def __init__(self):
        # Initialize the game
        pygame.init()

        # Set up the display
        self.screen_width = 800
        self.screen_height = 400
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Pong")

        # Set up the colors
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)

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
        self.ball_speed_x = 1
        self.ball_speed_y = 1
        self.ball_x = self.screen_width // 2
        self.ball_y = self.screen_height // 2

        # Set up the score
        self.player_a_score = 0
        self.player_b_score = 0
        self.font = pygame.font.Font(None, 36)
        self.score_text = self.font.render("Player A: {}     Player B: {}".format(self.player_a_score, self.player_b_score), True, self.WHITE)


    def _move_ball(self):
        self.ball_x += self.ball_speed_x
        self.ball_y += self.ball_speed_y

    def _check_collision_with_paddle(self):
        # Check for collisions with paddles
        if self.ball_x == self.player_a_paddle_x + self.paddle_width and self.player_a_paddle_y <= self.ball_y <= self.player_a_paddle_y + self.paddle_height:
            self.ball_speed_x *= -1
        if self.ball_x == self.player_b_paddle_x - self.paddle_width and self.player_b_paddle_y <= self.ball_y <= self.player_b_paddle_y + self.paddle_height:
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
        self.score_text = self.font.render("Player A: {}     Player B: {}".format(self.player_a_score, self.player_b_score), True, self.WHITE)

    def _draw_game(self):
        # Clear the screen
        self.screen.fill(self.BLACK)

        # Draw the paddles
        pygame.draw.rect(self.screen, self.WHITE, (self.player_a_paddle_x, self.player_a_paddle_y, self.paddle_width, self.paddle_height))
        pygame.draw.rect(self.screen, self.WHITE, (self.player_b_paddle_x, self.player_b_paddle_y, self.paddle_width, self.paddle_height))

        # Draw the ball
        pygame.draw.circle(self.screen, self.WHITE, (self.ball_x, self.ball_y), self.ball_radius)

        # Draw the score
        self.screen.blit(self.score_text, (self.screen_width // 2 - self.score_text.get_width() // 2, 10))
    
    def move_paddles(self,fingertips):
        # adjust this function to match the paddel y-coordinate to the finger tips
        # Get fingertip positions
        fingertips_array = np.array(fingertips)
        if fingertips_array.shape[0] == 2:
            
            fingertip_pos_left = fingertips_array[np.argmax(fingertips_array[:,0]),1]
            fingertip_pos_right = fingertips_array[np.argmin(fingertips_array[:,0]),1]

            # Match paddle y-coordinate to fingertip y-coordinate
            if fingertip_pos_left is not None:  # Ensure the fingertip was detected
                self.player_a_paddle_y = max(min(fingertip_pos_left, self.screen_height - self.paddle_height), 0)
            if fingertip_pos_right is not None:  # Ensure the fingertip was detected
                self.player_b_paddle_y = max(min(fingertip_pos_right, self.screen_height - self.paddle_height), 0)
        

    def _calibrate_corners(self):
        # Define corner points
        corners = [(0, 0), (self.screen_width, 0), (0, self.screen_height), (self.screen_width, self.screen_height)]

        # Draw and store the corners
        corner_rects = []
        for corner in corners:
            rect = pygame.Rect(corner[0] - 5, corner[1] - 5, 10, 10)  # Erstelle ein Rechteck um die Ecke
            pygame.draw.rect(self.screen, self.WHITE, rect)
            corner_rects.append(rect)

        pygame.display.flip()
        return corner_rects

    def run(self):       
        self._move_ball()
        self._check_collision_with_paddle()
        self._check_collision_with_wall()
        self._update_score()
        self._draw_game()
        self._calibrate_corners()

if __name__ == '__main__':
    # Game loop
    pong = PongGame()
    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pong.move_paddles()  
        pong.run()

        # Update the display
        pygame.display.flip()
        
        time.sleep(0.005)

    # Quit the game
    pygame.quit()