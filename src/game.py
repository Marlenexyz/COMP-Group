from hand_recognition import *
from frame_matcher import *
from pos_predictor import *
from pong import *
from menu import *
from setup import *

import cv2

# Hyperparameters ----------
video = 2
game_height = 400
game_width = 600

debug_height = 200
debug_width = 600

initial_paddle_pos_left = game_height // 2
initial_paddle_pos_right = game_height // 2
countdown = 3 # increase countdown

test_flag = False

if test_flag:
    countdown = 0
    video = 0

# --------------------------



def calculatePaddlePos(game_corners, index_finger_pos):
    """
    Calculate the correct y position of the paddle from the index finger position
    and game corners.
    """
    
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



def displayDebugInfo():
    """
    Show debug information like FPS and gesture detections.
    """
    
    global prev_time
    
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



def hand_as_mouse(frame):
    """
    Use the hand as a mouse for the game. Presses are realized by pinching the index finger
    and the thumb.
    """
    
    ret, frame = cap.read()
    if ret == False:
        return
            
    hand_recognition.run(frame)
    result = hand_recognition.getIndexFingerCoordRight()
    if result is not None and game_corners is not None:
        x, y = frame_matcher.mapCoords(result, game_corners)

        if x is not None and y is not None:
            mainMenu.finger_as_mouse(x, y, hand_recognition.isTouchingIndexFingerAndThumb())


# --------------- MAIN ---------------
if __name__ == '__main__':

    # MAIN INIT ----------------------
    cap = cv2.VideoCapture(video)
    frame_matcher = FrameMatcher(game_height, game_width)
    hand_recognition = HandRecognition()
    pos_predictor = PosPredictor(initial_paddle_pos_left, initial_paddle_pos_right)
    mainMenu = Menu(game_height, game_width)
    pong = PongGame(game_height, game_width)

    prev_time = time.time()
    index_finger_pos = [initial_paddle_pos_left // 2, initial_paddle_pos_right // 2]

    has_run_once = False
    set_up_done = False
    
    # MAIN LOOP ----------------------
    while True:
        
        # get new frame
        ret, frame = cap.read()
        if ret == False:
            continue
        
        # get game status
        status = mainMenu.getStatus()
        
        # START GAME ---------------------
        if status == 'setup':
            mainMenu.create_set_up_window()

        # GAME MENU ---------------------
        elif status == 'main':
            
            # calibrate corners once after setup screen
            if not set_up_done:
                set_up_done = True
                
                if not test_flag:
                    pong.draw_only_corners()
                    game_corners = frame_matcher.calibrateCorners(cap)
                else:
                    game_corners = [(0, 0), (0, game_height), (game_width, 0), (game_width, game_height)]

            # draw main menu and mouse position
            mainMenu.update_menu()
            hand_as_mouse(frame)
                
        # ENTER NAMES ---------------------
        elif status == 'enterNames':
            
            # draw main menu and mouse position
            mainMenu.update_menu()
            hand_as_mouse(frame)
            
            # set player names
            pong.setPlayerNameA(mainMenu.getPlayerNameA())
            pong.setPlayerNameB(mainMenu.getPlayerNameB())

        # PONG GAME ---------------------
        elif status == 'play':
            if not has_run_once:
                pong.run()

                # Display Countdown on screen, after countdown ends game starts automatically
                while countdown > 0:
                    pong.draw_countdown(countdown)
                    pygame.time.delay(1000)
                    countdown -= 1

                pong.togglePause()
                # Setze die Flagge auf True, um zu kennzeichnen, dass die Funktion aufgerufen wurde    
                has_run_once = True

            # update game if not paused
            if not pong.isGamePaused():
                
                # run hand recognition for index finger positions
                hand_recognition.run(frame)
                index_finger_pos = [hand_recognition.getIndexFingerPosLeft(), hand_recognition.getIndexFingerPosRight()]
                
                # predict positions if index finger was not detected
                if index_finger_pos[0] is None:
                    index_finger_pos[0] = pos_predictor.predictLeft()
                pos_predictor.correctLeft(index_finger_pos[0])
                if index_finger_pos[1] is None:
                    index_finger_pos[1] = pos_predictor.predictRight()
                pos_predictor.correctRight(index_finger_pos[1])
                    
                # update paddles if index finger is in game frame
                calculatePaddlePos(game_corners, index_finger_pos)
                
                # change ball speed if v shape is recognized
                if hand_recognition.isVShape():
                    pong.setBallSpeed()
                
                # run pong and update display
                pong.run()

            # check for keyboard inputs
            keys = pygame.key.get_pressed()
            if keys[pygame.K_p]:
                pong.togglePause()
                pygame.time.delay(100) # 100 Milliseconds Delay
            elif keys[pygame.K_f]:
                pong.togglePause()
                pong.draw_only_corners()
                frame_matcher.measureAccuracy(cap)
                pong.togglePause()
            elif keys[pygame.K_h]:
                pong.togglePause()
                hand_recognition.measureRecall(cap)
                pong.togglePause()
            elif keys[pygame.K_c]:
                pong.togglePause()
                pong.draw_only_corners()
                game_corners = frame_matcher.calibrateCorners(cap)
                pong.togglePause()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                 
        # QUIT GAME ---------------------   
        elif status == 'quit_pong':
            pong.quitGame()
            status = 'main'
            
        # show debug information
        displayDebugInfo()
        
        # show the live video
        cv2.imshow('Video Feed', frame)
