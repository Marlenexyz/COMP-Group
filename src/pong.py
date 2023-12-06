import pygame
import random
import time

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


    def move_ball(self):
        self.ball_x += self.ball_speed_x
        self.ball_y += self.ball_speed_y

    def check_collision_with_paddle(self):
        # Check for collisions with paddles
        if self.ball_x == self.player_a_paddle_x + self.paddle_width and self.player_a_paddle_y <= self.ball_y <= self.player_a_paddle_y + self.paddle_height:
            self.ball_speed_x *= -1
        if self.ball_x == self.player_b_paddle_x - self.paddle_width and self.player_b_paddle_y <= self.ball_y <= self.player_b_paddle_y + self.paddle_height:
            self.ball_speed_x *= -1

    def check_collision_with_wall(self):
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

    def update_score(self):
        # Update the score text
        self.score_text = self.font.render("Player A: {}     Player B: {}".format(self.player_a_score, self.player_b_score), True, self.WHITE)

    def draw_game(self):
        # Clear the screen
        self.screen.fill(self.BLACK)

        # Draw the paddles
        pygame.draw.rect(self.screen, self.WHITE, (self.player_a_paddle_x, self.player_a_paddle_y, self.paddle_width, self.paddle_height))
        pygame.draw.rect(self.screen, self.WHITE, (self.player_b_paddle_x, self.player_b_paddle_y, self.paddle_width, self.paddle_height))

        # Draw the ball
        pygame.draw.circle(self.screen, self.WHITE, (self.ball_x, self.ball_y), self.ball_radius)

        # Draw the score
        self.screen.blit(self.score_text, (self.screen_width // 2 - self.score_text.get_width() // 2, 10))
    
    def move_paddles(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and self.player_a_paddle_y > 0:
            self.player_a_paddle_y -= self.paddle_speed
        if keys[pygame.K_s] and self.player_a_paddle_y < self.screen_height - self.paddle_height:
            self.player_a_paddle_y += self.paddle_speed
        if keys[pygame.K_UP] and self.player_b_paddle_y > 0:
            self.player_b_paddle_y -= self.paddle_speed
        if keys[pygame.K_DOWN] and self.player_b_paddle_y < self.screen_height - self.paddle_height:
            self.player_b_paddle_y += self.paddle_speed

    def calibrate_corners(self):
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



    
# Game loop
pong = PongGame()
running = True
while running:
    
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pong.move_paddles()         #give arguments 
 
    pong.move_ball()
    
    pong.check_collision_with_paddle()
   
    pong.check_collision_with_wall()

    pong.update_score()

    pong.draw_game()
    pong.calibrate_corners()


    # Update the display
    pygame.display.flip()
    
    time.sleep(0.005)

# Quit the game
pygame.quit()
