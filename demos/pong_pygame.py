import pygame
import random
import time

# Initialize the game
pygame.init()

# Set up the display
screen_width = 800
screen_height = 400
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Pong")

# Set up the colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Set up the paddles
paddle_width = 10
paddle_height = 60
paddle_speed = 1
player_a_paddle_x = 50
player_a_paddle_y = (screen_height - paddle_height) // 2
player_b_paddle_x = screen_width - paddle_width - 50
player_b_paddle_y = (screen_height - paddle_height) // 2

# Set up the ball
ball_radius = 5
ball_speed_x = 1
ball_speed_y = 1
ball_x = screen_width // 2
ball_y = screen_height // 2

# Set up the score
player_a_score = 0
player_b_score = 0
font = pygame.font.Font(None, 36)
score_text = font.render("Player A: {}     Player B: {}".format(player_a_score, player_b_score), True, WHITE)

# Game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Move the paddles
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and player_a_paddle_y > 0:
        player_a_paddle_y -= paddle_speed
    if keys[pygame.K_s] and player_a_paddle_y < screen_height - paddle_height:
        player_a_paddle_y += paddle_speed
    if keys[pygame.K_UP] and player_b_paddle_y > 0:
        player_b_paddle_y -= paddle_speed
    if keys[pygame.K_DOWN] and player_b_paddle_y < screen_height - paddle_height:
        player_b_paddle_y += paddle_speed

    # Move the ball
    ball_x += ball_speed_x
    ball_y += ball_speed_y

    # Check for collisions with paddles
    if ball_x == player_a_paddle_x + paddle_width and player_a_paddle_y <= ball_y <= player_a_paddle_y + paddle_height:
        ball_speed_x *= -1
    if ball_x == player_b_paddle_x - paddle_width and player_b_paddle_y <= ball_y <= player_b_paddle_y + paddle_height:
        ball_speed_x *= -1

    # Check for collisions with walls
    if ball_y <= 0 or ball_y >= screen_height - ball_radius:
        ball_speed_y *= -1
    if ball_x <= 0:
        player_b_score += 1
        ball_x = screen_width // 2
        ball_y = screen_height // 2
    if ball_x >= screen_width - ball_radius:
        player_a_score += 1
        ball_x = screen_width // 2
        ball_y = screen_height // 2

    # Update the score text
    score_text = font.render("Player A: {}     Player B: {}".format(player_a_score, player_b_score), True, WHITE)

    # Clear the screen
    screen.fill(BLACK)

    # Draw the paddles
    pygame.draw.rect(screen, WHITE, (player_a_paddle_x, player_a_paddle_y, paddle_width, paddle_height))
    pygame.draw.rect(screen, WHITE, (player_b_paddle_x, player_b_paddle_y, paddle_width, paddle_height))

    # Draw the ball
    pygame.draw.circle(screen, WHITE, (ball_x, ball_y), ball_radius)

    # Draw the score
    screen.blit(score_text, (screen_width // 2 - score_text.get_width() // 2, 10))

    # Update the display
    pygame.display.flip()
    
    time.sleep(0.005)

# Quit the game
pygame.quit()
