from hand_recognition import *
from FrameMatching import *
from pong import *

import cv2

# Hyperparameters ----------
video = 0
game_width = 400
game_height = 800

# --------------------------

if __name__ == '__main__':
    
    cap = cv2.VideoCapture(video)
    hand_recognition = HandRecognition()
    frame_matching = FrameMatching()
    pong = PongGame(game_width, game_height)
    running = True
    
    while running:
        
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
        ret, frame = cap.read()
        
        game_corners = frame_matching.run(frame)
        hand_recognition.run(frame)
        index_finger_pos = [hand_recognition.getIndexFingerCoordLeft, hand_recognition.getIndexFingerCoordRight]
        cv2.imshow('frame', frame)
        
        # check if left index finger was detected
        if index_finger_pos[0] is not None:
            # get left y values
            left_y_min, left_y_max = game_corners[0][1], game_corners[1][1]
            left_y_crt = index_finger_pos[0][1]
            # check if left index finger is in game frame
            if left_y_crt >= left_y_min and left_y_crt < left_y_max:
                left_y_new = (left_y_crt - left_y_min) / (left_y_max - left_y_min)
                pong.move_paddle_left(left_y_new * game_height)
                
        # check if right index finger was detected
        if index_finger_pos[1] is not None:
            # get right y values
            right_y_min, right_y_max = game_corners[2][1], game_corners[3][1]
            right_y_crt = index_finger_pos[1][1]
            # check if right index finger is in game frame
            if right_y_crt >= right_y_min and right_y_crt < right_y_max:
                right_y_new = (right_y_crt - right_y_min) / (right_y_max - right_y_min)
                pong.move_paddle_right(right_y_new * game_height)

        pong.run()

        # Update the display
        pygame.display.flip()
        
        time.sleep(0.005)
        
    # Release webcam and destroy windows
    cap.release()
    cv2.destroyAllWindows()

    # Quit the game
    pygame.quit()