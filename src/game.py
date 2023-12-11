from hand_recognition import *
from FrameMatching import *
from pong import *
from menu import *

import cv2

# Hyperparameters ----------
video = 2
game_height = 400
game_width = 800

# --------------------------

if __name__ == '__main__':
    mainMenu = Menu(game_height, game_width)
    hand_recognition = HandRecognition(0)   

    # pause_pressed = False   #Flag to track if paused

    
    cap = cv2.VideoCapture(video)
    hand_recognition = HandRecognition()
    frame_matching = FrameMatching()
    pong = PongGame(game_height, game_width)
    running = True
    
    while running:
        status = mainMenu.getStatus()

        if status == 'main':
            mainMenu.update_menu()  
            

        elif status == 'enterNames':
            mainMenu.update_menu()          #Very important line
            pong.setPlayerNameA(mainMenu.getPlayerNameA())
            pong.setPlayerNameB(mainMenu.getPlayerNameB())
            
            # pong.setMenuState('play')



        elif status == 'play':
            # del mainMenu
            hand_recognition.run()
            # Handle events
            # for event in pygame.event.get():
            #     if event.type == pygame.QUIT:
            #         running = False
            #     elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            #         if not pause_pressed:
            #             # Toggle pause state on space press
            #             pong.togglePause()
            #             pause_pressed = True
            #     elif event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
            #         # Reset flag when space key is released
            #         pause_pressed = False
            # if not pong.isPaused():
            pong.move_paddle_left(hand_recognition.getIndexFingerPosLeft())
            pong.move_paddle_right(hand_recognition.getIndexFingerPosRight())
        
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
        ret, frame = cap.read()
        if ret == False:
            continue
        game_corners = frame_matching.run(frame)
        hand_recognition.run(frame)
        index_finger_pos = [hand_recognition.getIndexFingerPosLeft(), hand_recognition.getIndexFingerPosRight()]
        cv2.imshow('frame', frame)
            
        if game_corners is not None:
            # check if left index finger was detected
            if index_finger_pos[0] is not None:
                # get left y values
                left_y_min, left_y_max = game_corners[0][1], game_corners[1][1]
                left_y_crt = index_finger_pos[0]
                # check if left index finger is in game frame
                if left_y_crt >= left_y_min and left_y_crt < left_y_max:
                    left_y_new = (left_y_crt - left_y_min) / (left_y_max - left_y_min)
                    pong.move_paddle_left(left_y_new * game_height)
                    
            # check if right index finger was detected
            if index_finger_pos[1] is not None:
                # get right y values
                right_y_min, right_y_max = game_corners[2][1], game_corners[3][1]
                right_y_crt = index_finger_pos[1]

                # check if right index finger is in game frame
                if right_y_crt >= right_y_min and right_y_crt < right_y_max:
                    right_y_new = (right_y_crt - right_y_min) / (right_y_max - right_y_min)
                    print(right_y_new)
                    print(right_y_new * game_height)
                    pong.move_paddle_right(right_y_new * game_height)

            pong.run()

            # Update the display
            pygame.display.flip()
                
            time.sleep(0.005)

            for event in pygame.event.get():    #Ends hand_recognition when pong is closed
                if event.type == pygame.QUIT:
                    del hand_recognition
                    pygame.quit()
                    exit()
                    

        elif status == 'quit_pong':
            pong.quitGame()
            status = 'main'
            del hand_recognition


pygame.quit()