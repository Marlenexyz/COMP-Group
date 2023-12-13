from hand_recognition import *
from frame_matcher import *
from pong import *
from menu import *
from setup import *

import cv2

# Hyperparameters ----------
video = 0
game_height = 400
game_width = 600

debug_height = 200
debug_width = 600

initial_paddle_pos_left = game_height // 2
initial_paddle_pos_right = game_height // 2
countdown = 3 # increase countdown

n_hand_recognition = 3

test_flag = True

if test_flag:
    countdown = 0

# --------------------------



def calculatePaddlePos(game_corners, index_finger_pos):
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
    global prev_time
    global fps
    
    # Initialize debug frame
    debug_frame = np.zeros((debug_height, debug_width, 3), dtype=np.uint8)
    
    # Calculate and display FPS on a new cv2 window
    if n_frames % n_hand_recognition == 0:
        curr_time = time.time()
        fps = n_hand_recognition / (curr_time - prev_time)
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

def hand_as_mouse():
    ## Start Hand als Maus
    ret, frame = cap.read()
    if ret == False:
        pass
            
    hand_recognition.run(frame)
    result = hand_recognition.getIndexFingerCoordRight()         ### Both?
    # result = hand_recognition.getIndexFingerCoordBoth()

    try:
        x, y = result   #[0]
        mainMenu.finger_as_mouse(x,y,hand_recognition.isTouchingIndexFingerAndThumb(None)) #None  
        # pygame.time.delay(1000)
    except:
        pass

    displayDebugInfo()

    
    cv2.imshow('Video Feed', frame)
    ##End Hand as Mouse
    
    
    
def predict_index_finger_pos(last_known_pos):
    """
    Predicts the next index finger position using a Kalman filter.
    """
    
    # Predict the new position of the index finger
    prediction = kalman_filter.predict()
    predicted_pos = prediction.squeeze().astype(int).tolist()

    # Update the Kalman filter with the last known position
    measurement = np.array(last_known_pos, dtype=np.float32).reshape(-1 , 1)
    kalman_filter.correct(measurement)

    return predicted_pos


def hand_as_mouse():
    ## Start Hand als Maus
    ret, frame = cap.read()
    if ret == False:
        pass
            
    hand_recognition.run(frame)
    result = hand_recognition.getIndexFingerCoordRight()         ### Both?
    # result = hand_recognition.getIndexFingerCoordBoth()

    try:
        x, y = result   #[0]
        mainMenu.finger_as_mouse(x,y,hand_recognition.isTouchingIndexFingerAndThumb(None)) #None  
        pygame.time.delay(1000)
    except:
        pass

    displayDebugInfo()

    
    cv2.imshow('Video Feed', frame)
    ##End Hand as Mouse



if __name__ == '__main__':
    
    

    # INITIALIZATION -----------------
    cap = cv2.VideoCapture(video)
    frame_matcher = FrameMatcher()
    hand_recognition = HandRecognition()
    mainMenu = Menu(game_height, game_width)
    pong = PongGame(game_height, game_width)
    
    kalman_filter = cv2.KalmanFilter(4, 2)
    kalman_filter.transitionMatrix = np.array([[1, 1],
                                               [0, 1]], dtype=np.float32)
    kalman_filter.measurementMatrix = np.eye(2, 2, dtype=np.float32)
    kalman_filter.processNoiseCov = 1e-3 * np.eye(2, 2, dtype=np.float32)
    kalman_filter.measurementNoiseCov = 1e-3 * np.eye(2, 2, dtype=np.float32)
    kalman_filter.statePost = np.array([[initial_paddle_pos_left], [initial_paddle_pos_right]], dtype=np.float32)
    kalman_filter.errorCovPost = np.ones((2, 2), dtype=np.float32)

    prev_time = time.time()
    n_frames = 0
    fps = 0
    index_finger_pos = [0, 0]

    has_run_once = False
    set_up_done = False

    if not test_flag:
        create_set_up_window(game_height, game_width)

    
    # MAIN loop ----------------------
    while True:
        n_frames += 1
        
        # get game status
        status = mainMenu.getStatus()
               

        if status == 'main':
            if not set_up_done:
                set_up_done = True
                
                if not test_flag:
                    pong.draw_only_corners()
                    game_corners = frame_matcher.calibrateCorners(cap)
                else:
                    game_corners = [(0, 0), (0, game_height), (game_width, 0), (game_width, game_height)]


            hand_as_mouse()
            
                
            mainMenu.update_menu()
        elif status == 'enterNames':
            mainMenu.update_menu()
            pong.setPlayerNameA(mainMenu.getPlayerNameA())
            pong.setPlayerNameB(mainMenu.getPlayerNameB())

        elif status == 'play':
            if not has_run_once:
                pong.run()

                ## Display Countdown on screen, after countdown ends game starts automatically
                while countdown > 0:
                    pygame.time.delay(1000)
                    pong.draw_countdown(countdown)
                    countdown -= 1

                pong.togglePause()
                # Setze die Flagge auf True, um zu kennzeichnen, dass die Funktion aufgerufen wurde    
                has_run_once = True


            if not pong.isGamePaused():
                
                ret, frame = cap.read()
                if ret == False:
                    continue
                
                # # run frame matcher for game corners
                # game_corners = frame_matcher.run(frame)
                
                # run hand recognition for index finger positions
                if n_frames % n_hand_recognition == 0:
                    hand_recognition.run(frame)
                    index_finger_pos = [hand_recognition.getIndexFingerPosLeft(), hand_recognition.getIndexFingerPosRight()]
                else:
                    index_finger_pos = predict_index_finger_pos(index_finger_pos)
                    
                # update paddles if index finger is in game frame
                calculatePaddlePos(game_corners, index_finger_pos)
                
                # change ball speed if v shape is recognized
                if hand_recognition.isVShape():
                    pong.setBallSpeed()
                
                # show frame
                cv2.imshow('Video Feed', frame)
                
                # display debug info
                displayDebugInfo()

                # run pong and update display
                pong.run()
                


            keys = pygame.key.get_pressed()
            if keys[pygame.K_p]:
                pong.togglePause()
                pygame.time.delay(100) # 100 Milliseconds Delay
            elif keys[pygame.K_f]:
                pong.togglePause()
                frame_matcher.measureAccuracy(cap)
                pong.togglePause()
            elif keys[pygame.K_h]:
                pong.togglePause()
                hand_recognition.measureRecall(cap)
                pong.togglePause()
            elif keys[pygame.K_c]:
                pong.togglePause()
                pong.draw_only_corners()
                frame_matcher.calibrateCorners(cap)
                pong.togglePause()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                    
        elif status == 'quit_pong':
            pong.quitGame()
            status = 'main'
