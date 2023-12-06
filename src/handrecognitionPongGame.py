from hand_recognition import *
from pong import *


if __name__ == '__main__':
    hand_recognition = HandRecognition(0)
    pong = PongGame()
    running = True
    while running:
        hand_recognition.run()
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pong.move_paddles(hand_recognition.getIndexFingerCoordinates())         #give arguments 
    
        pong.move_ball()
        
        pong.check_collision_with_paddle()
    
        pong.check_collision_with_wall()

        pong.update_score()

        pong.draw_game()
        pong.calibrate_corners()


        # Update the display
        pygame.display.flip()
        
        time.sleep(0.005)
        
            
    del hand_recognition

    # Quit the game
    pygame.quit()