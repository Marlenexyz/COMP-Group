from hand_recognition import *
from pong import *
from menu import *


if __name__ == '__main__':
    mainMenu = Menu(400, 600)
    hand_recognition = HandRecognition(0)
    pong = PongGame(400,600)
    running = True
    status = mainMenu.getStatus()
    while running:
        if status == 'main':
            mainMenu.update_menu()

        if status == 'play':
            hand_recognition.run()
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            pong.move_paddle_left(hand_recognition.getIndexFingerPosLeft())
            pong.move_paddle_right(hand_recognition.getIndexFingerPosRight())

            pong.run()

            # Update the display
            pygame.display.flip()
            
            time.sleep(0.005)
        
            
    del hand_recognition

    # Quit the game
    pygame.quit()