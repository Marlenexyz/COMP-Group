import pygame
import time
import numpy as np
import random
from confetti import *



class PongGame:
    def __init__(self,screen_height,screen_width):
        # Initialize the game
        pygame.init()

        self.confetti_particles = []
        
        # Load background music
        pygame.mixer.music.load("music.mp3")

        # Play the background music on a loop
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.5)
        
        # Load sound effects
        self.bounce_sound = pygame.mixer.Sound("bounce.wav")
        self.death_sound = pygame.mixer.Sound("deathray.wav")

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
        self.GRAY = (150, 150, 150)
        
        # Set up the corners
        self.l_thickness = 15 * 2
        self.l_length = 50 * 2

        # Set up the paddles
        self.paddle_width = 12
        self.paddle_height_a = 60
        self.paddle_height_b = 60
        self.initial_paddle_height_a = self.paddle_height_a
        self.initial_paddle_height_b = self.paddle_height_b


        self.paddle_speed = 3 # only used for keyboard inputs
        self.paddle_increase = 60 # value added to paddle height


        
        self.player_a_paddle_x = 50
        self.player_a_paddle_y = (self.screen_height - self.paddle_height_a) // 2
        self.player_b_paddle_x = self.screen_width - self.paddle_width - 50
        self.player_b_paddle_y = (self.screen_height - self.paddle_height_b) // 2

        self.paddle_rect_a = pygame.Rect(self.player_a_paddle_x, self.player_a_paddle_y, self.paddle_width, self.paddle_height_a)
        self.paddle_rect_b = pygame.Rect(self.player_b_paddle_x, self.player_b_paddle_y, self.paddle_width, self.paddle_height_b)

        # Set up the barrier
        self.barrier_width = 12
        self.barrier_height = 90
        self.player_a_barrier_x = None
        self.player_a_barrier_y = None
        self.player_b_barrier_x = None
        self.player_b_barrier_y = None
        
        self.player_a_barrier_rect = pygame.Rect(0, 0, self.barrier_width, self.barrier_height)
        self.player_b_barrier_rect = pygame.Rect(0, 0, self.barrier_width, self.barrier_height)
        
        # Set up the ball
        self.ball_radius = 6

        self.ball_speed_x = 3
        self.ball_speed_y = 3
        self.initial_ball_speed_x  = self.ball_speed_x
        self.initial_ball_speed_y = self.ball_speed_y

        self.ball_increase = 2 # value multiplied with ball speed
        self.ball_x = self.screen_width // 2
        self.ball_y = self.screen_height // 2

        self.ball_rect = pygame.Rect(self.ball_x, self.ball_y, self.ball_radius * 2, self.ball_radius * 2)
        
        # Set up the players
        self.player_name_a = "Player A"
        self.player_name_b = "Player B"
        self.player_ball_speed_active_a = False
        self.player_ball_speed_active_b = False
        self.player_paddle_increase_active_a = False
        self.player_paddle_increase_active_b = False
        self.player_barrier_active_a = False
        self.player_barrier_active_b = False
        self.max_timeout = 500
        self.player_timeout_ball_speed_a = self.max_timeout
        self.player_timeout_ball_speed_b = self.max_timeout
        self.player_timeout_paddle_increase_a = self.max_timeout
        self.player_timeout_paddle_increase_b = self.max_timeout
        self.player_timeout_barrier_a = self.max_timeout
        self.player_timeout_barrier_b = self.max_timeout

        # Set up the score
        self.player_a_score = 0
        self.player_b_score = 0
        self.font = pygame.font.Font(None, 36)

        self.win_score = 10 ## increase to 10
        self.game_won = False
        
        self.collision_detected = False
        self.collision_timeout = 0
        self.collision_timeout_max = 5

    def _generate_confetti(self):
        confetti_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        confetti_particle = Confetti(random.randint(0, self.screen_width), random.randint(0, self.screen_height), confetti_color)
        self.confetti_particles.append(confetti_particle)

    def _update_confetti(self):
        for particle in self.confetti_particles:
            particle.move()

    def draw_confetti(self):
        self._generate_confetti()
        self._update_confetti()
        for particle in self.confetti_particles:
            pygame.draw.circle(self.screen, particle.color, (int(particle.x), int(particle.y)), 5)
        pygame.display.flip()



    def setPlayerNameA(self, inputName):
        self.player_name_a = inputName
        self._update_score()

    def setPlayerNameB(self, inputName):
        self.player_name_b = inputName
        self._update_score()

    def togglePause(self):
        self.paused = not self.paused

    def isGamePaused(self):
        return self.paused
    
    def _move_ball(self):
        self.ball_x += self.ball_speed_x
        self.ball_y += self.ball_speed_y
        self.ball_rect = pygame.Rect(self.ball_x, self.ball_y, self.ball_radius * 2, self.ball_radius * 2)

    def _check_collision_with_paddle(self):
        # Check for collisions with paddles
        if self.paddle_rect_a.colliderect(self.ball_rect):
            self.ball_speed_x *= -1
            self.bounce_sound.play()
            self.collision_timeout = self.collision_timeout_max
            return True
        if self.paddle_rect_b.colliderect(self.ball_rect):
            self.ball_speed_x *= -1
            self.bounce_sound.play()
            self.collision_timeout = self.collision_timeout_max
            return True
        return False
            
    def _check_collision_with_barrier(self):
        # Check for collisions with barriers
        if self.player_barrier_active_a:
            if self.player_a_barrier_x is not None and self.player_a_barrier_y is not None:
                if self.player_a_barrier_rect.colliderect(self.ball_rect):
                    self.ball_speed_x *= -1
                    self.bounce_sound.play()
                    self.collision_timeout = self.collision_timeout_max
                    return True
        if self.player_barrier_active_b:
            if self.player_b_barrier_x is not None and self.player_b_barrier_y is not None:
                if self.player_b_barrier_rect.colliderect(self.ball_rect):
                    self.ball_speed_x *= -1
                    self.bounce_sound.play()
                    self.collision_timeout = self.collision_timeout_max
                    return True
        return False

    def _check_collision_with_wall(self):
            # Check for collisions with walls
        if self.ball_y <= 0 or self.ball_y >= self.screen_height - self.ball_radius:
            self.ball_speed_y *= -1
            self.bounce_sound.play()
        if self.ball_x <= 0:
            self.player_b_score += 1
            self.death_sound.play()
            self.reset_ball()
        if self.ball_x >= self.screen_width - self.ball_radius:
            self.player_a_score += 1
            self.death_sound.play()
            self.reset_ball()

    def _update_score(self):
        # Update the score text
        self.score_text = self.font.render("{}: {}     {}: {}".format(self.player_name_a, self.player_a_score, self.player_name_b,self.player_b_score), True, self.BLACK)

    def _draw_l_marker(self, x, y):
        # Vertical bar of the L
        pygame.draw.rect(self.screen, self.RED, (x - self.l_thickness // 2, y - self.l_length // 2, self.l_thickness, self.l_length))
        # Horizontal bar of the L
        pygame.draw.rect(self.screen, self.RED, (x - self.l_length // 2, y - self.l_thickness // 2, self.l_length, self.l_thickness))

    def _draw_game(self):
        # Clear the screen
        self.screen.fill(self.WHITE)

        # Draw the paddles
        self.paddle_rect_a = pygame.Rect(self.player_a_paddle_x, self.player_a_paddle_y, self.paddle_width, self.paddle_height_a)
        self.paddle_rect_b = pygame.Rect(self.player_b_paddle_x, self.player_b_paddle_y, self.paddle_width, self.paddle_height_b)

        pygame.draw.rect(self.screen, self.BLACK, self.paddle_rect_a)
        pygame.draw.rect(self.screen, self.BLACK, self.paddle_rect_b)

        # Draw barriers
        if self.player_barrier_active_a:
            self.player_a_barrier_rect = pygame.draw.rect(self.screen, self.RED, (self.player_a_barrier_x, self.player_a_barrier_y, self.barrier_width, self.barrier_height))
        if self.player_barrier_active_b:
            self.player_b_barrier_rect = pygame.draw.rect(self.screen, self.RED, (self.player_b_barrier_x, self.player_b_barrier_y, self.barrier_width, self.barrier_height))

        # Draw the ball
        self.ball_rect = pygame.Rect(self.ball_x, self.ball_y, self.ball_radius * 2, self.ball_radius * 2)
        pygame.draw.circle(self.screen, self.BLACK, (self.ball_x + self.ball_radius, self.ball_y + self.ball_radius), self.ball_radius)

        # Draw the score
        self.screen.blit(self.score_text, (self.screen_width // 2 - self.score_text.get_width() // 2, 10))
        # Draw current ball speed for debug
        # self.screen.blit(self.ball_speed_text, (self.screen_width // 2 - self.ball_speed_text.get_width() // 2, 50))

        # Draw powerups
        self.vshape_powerup_a_text = self.font.render("2".format(), True, 
                                                      self.GRAY if self.player_timeout_ball_speed_a != self.max_timeout else self.BLACK)
        self.vshape_powerup_b_text = self.font.render("2".format(), True, 
                                                      self.GRAY if self.player_timeout_ball_speed_b != self.max_timeout else self.BLACK)
        self.pinch_powerup_a_text = self.font.render("P".format(), True, 
                                                     self.GRAY if self.player_timeout_paddle_increase_a != self.max_timeout else self.BLACK)
        self.pinch_powerup_b_text = self.font.render("P".format(), True, 
                                                     self.GRAY if self.player_timeout_paddle_increase_b != self.max_timeout else self.BLACK)
        self.fist_powerup_a_text = self.font.render("B".format(), True, 
                                                    self.GRAY if self.player_timeout_barrier_a != self.max_timeout else self.BLACK)
        self.fist_powerup_b_text = self.font.render("B".format(), True, 
                                                    self.GRAY if self.player_timeout_barrier_b != self.max_timeout else self.BLACK)

        
        self.screen.blit(self.vshape_powerup_a_text, (25, 0.01 * self.screen_height))
        self.screen.blit(self.vshape_powerup_b_text, (self.screen_width - self.paddle_width - 25, 0.01 * self.screen_height))
        self.screen.blit(self.pinch_powerup_a_text, (25, 0.06 * self.screen_height))
        self.screen.blit(self.pinch_powerup_b_text, (self.screen_width - self.paddle_width - 25, 0.06 * self.screen_height))
        self.screen.blit(self.fist_powerup_a_text, (25, 0.11 * self.screen_height))
        self.screen.blit(self.fist_powerup_b_text, (self.screen_width - self.paddle_width - 25, 0.11 * self.screen_height))



    def draw_only_corners(self):
        # Clear the screen
        self.screen.fill(self.WHITE)

        # Draw L-shaped marker function
        self._draw_l_marker(0, 0)
        self._draw_l_marker(self.screen_width, 0)
        self._draw_l_marker(0, self.screen_height)
        self._draw_l_marker(self.screen_width, self.screen_height)
        
        pygame.display.flip()

    def draw_countdown(self,countdown_value):
        self._draw_game() # to overwrite old counter value
        # increase the font size of the text
        self.font_countdown = pygame.font.Font(None, 100)
        countdown_text = self.font_countdown.render("{}".format(countdown_value), True, self.BLACK)
        self.screen.blit(countdown_text, (self.screen_width // 2 - countdown_text.get_width() // 2, self.screen_height // 2))
        pygame.display.flip()

    def reset_ball(self):
        self.ball_x = self.screen_width // 2        # - self.ball.width // 2
        self.ball_y = self.screen_height // 2       # - self.ball.height // 2
        self.ball_speed_x *= random.choice([-1, 1])
        self.ball_speed_y *= random.choice([-1, 1])

    def move_paddle_left(self, fingertip_pos_left):
        if fingertip_pos_left is not None:  # Ensure the fingertip was detected
            fingertip_pos_left += (self.paddle_width // 2)
            self.player_a_paddle_y = max(min(fingertip_pos_left, self.screen_height - self.paddle_height_a), 0)

    def move_paddle_right(self, fingertip_pos_right):
        if fingertip_pos_right is not None:  # Ensure the fingertip was detected
            fingertip_pos_right += (self.paddle_width // 2)
            self.player_b_paddle_y = max(min(fingertip_pos_right, self.screen_height - self.paddle_height_b), 0)
        
    def move_paddles_by_keys(self):
        # Move the paddles
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and self.player_a_paddle_y > 0:
            self.player_a_paddle_y -= self.paddle_speed
        if keys[pygame.K_s] and self.player_a_paddle_y < self.screen_height - self.paddle_height_a:
            self.player_a_paddle_y += self.paddle_speed
        if keys[pygame.K_UP] and self.player_b_paddle_y > 0:
            self.player_b_paddle_y -= self.paddle_speed
        if keys[pygame.K_DOWN] and self.player_b_paddle_y < self.screen_height - self.paddle_height_b:
            self.player_b_paddle_y += self.paddle_speed
            
    def increase_paddle_length(self, player):
        if player == 'left' and self.player_timeout_paddle_increase_a == self.max_timeout:
            self.player_paddle_increase_active_a = True
            self.paddle_height_a += self.paddle_increase
        elif player == 'right' and self.player_timeout_paddle_increase_b == self.max_timeout:
            self.player_paddle_increase_active_b = True
            self.paddle_height_b += self.paddle_increase
    
    def increase_ball_speed(self, player):
        if player == 'left' and self.player_timeout_ball_speed_a == self.max_timeout:
            self.player_ball_speed_active_a = True
            self.ball_speed_x *= self.ball_increase
            self.ball_speed_y *= self.ball_increase
        if player == 'right' and self.player_timeout_ball_speed_b == self.max_timeout:
            self.player_ball_speed_active_b = True
            self.ball_speed_x *= self.ball_increase
            self.ball_speed_y *= self.ball_increase
        
        # self._update_ball_speed()
        
    def set_barrier(self, player, pos):
        if pos[0] > self.screen_width or pos[1] > self.screen_height:
            return
        if player == 'left' and self.player_timeout_barrier_a == self.max_timeout:
            self.player_barrier_active_a = True
            self.player_a_barrier_x, self.player_a_barrier_y = pos[0] - self.barrier_width, pos[1] - self.barrier_height
        if player == 'right' and self.player_timeout_barrier_b == self.max_timeout:
            self.player_barrier_active_b = True
            self.player_b_barrier_x, self.player_b_barrier_y = pos[0] - self.barrier_width, pos[1] - self.barrier_height

    # def _update_ball_speed(self):
    #     self.ball_speed_text = self.font.render("Ball speed: " + str(abs(self.ball_speed_x)), True, self.BLACK)
        
    def _check_timeouts(self):
        if self.player_ball_speed_active_a:
            self.player_timeout_ball_speed_a -= 1
        if self.player_ball_speed_active_b:
            self.player_timeout_ball_speed_b -= 1
        if self.player_paddle_increase_active_a:
            self.player_timeout_paddle_increase_a -= 1
        if self.player_paddle_increase_active_b:
            self.player_timeout_paddle_increase_b -= 1
        if self.player_barrier_active_a:
            self.player_timeout_barrier_a -= 1
        if self.player_barrier_active_b:
            self.player_timeout_barrier_b -= 1
            
        if self.player_ball_speed_active_a and self.player_timeout_ball_speed_a == 0:
            self.player_ball_speed_active_a = False
            self.ball_speed_x /= self.ball_increase
            self.ball_speed_y /= self.ball_increase
        if self.player_ball_speed_active_b and self.player_timeout_ball_speed_b == 0:
            self.player_ball_speed_active_b = False
            self.ball_speed_x /= self.ball_increase
            self.ball_speed_y /= self.ball_increase
        if self.player_paddle_increase_active_a and self.player_timeout_paddle_increase_a == 0:
            self.player_paddle_increase_active_a = False
            self.paddle_height_a -= self.paddle_increase
        if self.player_paddle_increase_active_b and self.player_timeout_paddle_increase_b == 0:
            self.player_paddle_increase_active_b = False
            self.paddle_height_b -= self.paddle_increase
        if self.player_barrier_active_a and self.player_timeout_barrier_a == 0:
            self.player_barrier_active_a = False
        if self.player_barrier_active_b and self.player_timeout_barrier_b == 0:
            self.player_barrier_active_b = False

    def _check_win_condition(self):
        if self.player_a_score == self.win_score or self.player_b_score == self.win_score:
            self.paused = True
            self.draw_victory_screen()
    
    def draw_victory_screen(self):
        self.game_won = True
        self.font_big = pygame.font.Font(None, 72)
        if self.player_a_score == self.win_score:
            self.victory_text = self.font_big.render("{} wins!".format(self.player_name_a), True, self.BLACK)
        elif self.player_b_score == self.win_score:
            self.victory_text = self.font_big.render("{} wins!".format(self.player_name_b), True, self.BLACK)

        self.draw_confetti()
        self.screen.blit(self.victory_text, (self.screen_width / 2 - self.victory_text.get_width() / 2, self.screen_height / 2 - self.victory_text.get_height() / 2))
        # pygame.display.flip()

    def getGameWon(self):
        return self.game_won
    
        
    def reset_powerup_timeouts(self):
        self.player_timeout_ball_speed_a = self.max_timeout
        self.player_timeout_ball_speed_b = self.max_timeout
        self.player_timeout_paddle_increase_a = self.max_timeout
        self.player_timeout_paddle_increase_b = self.max_timeout
        self.player_timeout_barrier_a = self.max_timeout
        self.player_timeout_barrier_b = self.max_timeout

    def reset_ball_speed(self):
        self.ball_speed_x = self.initial_ball_speed_x
        self.ball_speed_y = self.initial_ball_speed_y

    def reset_paddles(self):
        self.paddle_height_a = self.initial_paddle_height_a
        self.paddle_height_b = self.initial_paddle_height_b

    def reset_powerups(self):
        self.player_ball_speed_active_a = False
        self.player_ball_speed_active_b = False
        self.player_paddle_increase_active_a = False
        self.player_paddle_increase_active_b = False
        self.player_barrier_active_a = False
        self.player_barrier_active_b = False
        

    def resetGame(self):
        self.reset_ball()
        self.reset_paddles()
        self.reset_ball_speed()
        self.reset_powerups()
        self.paused = False
        self.game_won = False
        self.player_a_score = 0
        self.player_b_score = 0
        self.reset_powerup_timeouts()



    def run(self):       
        self._move_ball()
        if not self.collision_detected:
            self.collision_detected = self._check_collision_with_paddle()
        if not self.collision_detected:
            self.collision_detected = self._check_collision_with_barrier()
        else:
            if self.collision_timeout != 0:
                self.collision_timeout -= 1
            else:
                self.collision_detected = False
        self._check_collision_with_wall()
        self._update_score()
        # self._update_ball_speed()
        self._draw_game()
        self._check_timeouts()
        self._check_win_condition()
        pygame.display.flip()





if __name__ == '__main__':
    # Game loop
    pong = PongGame(400, 800)
    frame = 0
    while True:
        frame += 1
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        
        if frame % 60 == 0:
            pong.increase_paddle_length('left')
            pong.increase_ball_speed('left')
        if frame % 120 == 0:
            pong.increase_paddle_length('right')
            # pong.increase_ball_speed('right')
        if frame % 180 == 0:
            pong.set_barrier('left', (100, 100))
            pong.set_barrier('right', (600, 300))

        pong.move_paddles_by_keys()  
        pong.run()
        
        time.sleep(0.02)

