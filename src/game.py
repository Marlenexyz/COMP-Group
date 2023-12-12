from hand_recognition import *
from frame_matching import *
from pong import *
from menu import *

import cv2

# Hyperparameters ----------
video = 0
game_height = 400
game_width = 600

debug_height = 200
debug_width = 600

# --------------------------



if __name__ == '__main__':
    mainMenu = Menu(game_height, game_width)
    cap = cv2.VideoCapture(video)
    hand_recognition = HandRecognition()
    frame_matching = FrameMatching()
    pong = PongGame(game_height, game_width)
    
    prev_time = time.time()
    running = True
    
    while running:
        status = mainMenu.getStatus()

        if status == 'main':
            mainMenu.update_menu()
        elif status == 'enterNames':
            mainMenu.update_menu()
            pong.setPlayerNameA(mainMenu.getPlayerNameA())
            pong.setPlayerNameB(mainMenu.getPlayerNameB())
            # pong.setMenuState('play')
        elif status == 'play':
            if not pong.isGamePaused():
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
                cv2.imshow('Video Feed', frame)
                    
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
                            pong.move_paddle_right(right_y_new * game_height)

                pong.run()

                # Update the display
                pygame.display.flip()
                
                # Initialize debug frame
                debug_frame = np.zeros((debug_height, debug_width, 3), dtype=np.uint8)
                
                # Calculate and display FPS on a new cv2 window
                curr_time = time.time()
                fps = 1 / (curr_time - prev_time)
                prev_time = curr_time
                fps_display = f"FPS: {int(fps)}"
                cv2.putText(debug_frame, fps_display, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                
                is_touching_index_finger_and_thumb_left = hand_recognition.isTouchingIndexFingerAndThumb('left')
                is_touching_index_finger_and_thumb_right = hand_recognition.isTouchingIndexFingerAndThumb('right')
                
                cv2.putText(debug_frame, 'Detected Gestures:', (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                touching_index_finger_and_thumb_left_display = f'    Left fingers touching: {is_touching_index_finger_and_thumb_left}'
                cv2.putText(debug_frame, touching_index_finger_and_thumb_left_display, (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                touching_index_finger_and_thumb_right_display = f'    Right fingers touching: {is_touching_index_finger_and_thumb_right}'
                cv2.putText(debug_frame, touching_index_finger_and_thumb_right_display, (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                
                # is_v_shape_left = hand_recognition.isVShape('left')
                # is_v_shape_right = hand_recognition.isVShape('right')
                
                cv2.imshow('Debug Info', debug_frame)


            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:
                pong.setGamePaused(True)
                #pong.togglePause()
            if keys[pygame.K_r]:
                pong.setGamePaused(False)


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                    
    
        #         elif event.type == KEYDOWN:
        #             if event.key == K_SPACE:
        #                 print("Leertaste wurde gedrückt!")
        #                 # pong.setGamePaused(not pong.isGamePaused())
        #                 pong.togglePause()
        elif status == 'quit_pong':
            pong.quitGame()
            status = 'main'

pygame.quit()
