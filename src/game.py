from hand_recognition import *
from pong import *
from menu import *


if __name__ == '__main__':
    mainMenu = Menu(400, 600)
    hand_recognition = HandRecognition(0)
    pong = PongGame(400,600)
    running = True
    status = mainMenu.getStatus()

    pause_pressed = False   #Flag to track if paused
    while running:
        if status == 'main':
            mainMenu.update_menu()

        elif status == 'play':
            hand_recognition.run()
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    if not pause_pressed:
                        # Toggle pause state on space press
                        pong.togglePause()
                        pause_pressed = True
                elif event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                    # Reset flag when space key is released
                    pause_pressed = False
            if not pong.isPaused():
                pong.move_paddle_left(hand_recognition.getIndexFingerPosLeft())
                pong.move_paddle_right(hand_recognition.getIndexFingerPosRight())

                pong.run()

                # Update the display
                pygame.display.flip()
                
            time.sleep(0.005)

        elif status == 'quit_pong':
            pong.quitGame()
            status = 'main'
        
        status = mainMenu.getStatus()
            
    del hand_recognition
    pygame.quit()