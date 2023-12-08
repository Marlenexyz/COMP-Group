from hand_recognition import *
from FrameMatching import *
from pong import *

import cv2

# Hyperparameters ----------
video = 2
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
        index_finger_pos = hand_recognition.run(frame)
        cv2.imshow('frame', frame)
        
        if game_corners is not None:
            # sort gamecorners by upper left, lower left, upper right, lower right
            game_corners_sorted = sorted(game_corners, key=lambda corner: corner[0] ** 2 + corner[1] ** 2)
        if index_finger_pos is not None:
            # sort index finger pos by x value
            index_finger_pos_sorted = sorted(index_finger_pos, key=lambda pos: pos[0])
        
        try:
            # get left y values
            left_y_min, left_y_max = game_corners_sorted[0][1], game_corners_sorted[1][1]
            left_y_crt = index_finger_pos_sorted[0][1]
            # get right y values
            right_y_min, right_y_max = game_corners_sorted[2][1], game_corners_sorted[3][1]
            right_y_crt = index_finger_pos_sorted[1][1]
        
            # check if left index finger is in game frame
            if left_y_crt >= left_y_min and left_y_crt < left_y_max:
                left_y_new = (left_y_crt - left_y_min) / (left_y_max - left_y_min)
            else:
                left_y_new = None
            # check if right index finger is in game frame
            if right_y_crt >= right_y_min and right_y_crt < right_y_max:
                right_y_new = (right_y_crt - right_y_min) / (right_y_max - right_y_min)
            else:
                right_y_new = None
            
            if left_y_new is not None:
                pong.move_paddle_left(left_y_new * game_height)
            if right_y_new is not None:
                pong.move_paddle_right(right_y_new * game_height)
        except:
            pass

        pong.run()

        # Update the display
        pygame.display.flip()
        
        time.sleep(0.005)
        
    
    # Release webcam and destroy windows
    cap.release()
    cv2.destroyAllWindows()
    
    del hand_recognition

    # Quit the game
    pygame.quit()