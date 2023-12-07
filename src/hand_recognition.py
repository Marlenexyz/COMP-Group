import cv2
import mediapipe as mp
import time
import numpy as np

class HandRecognition:
    '''hand recognition class which uses mediapipe library to recognize hand landmarks and draw them on frame'''
    def __init__(self, video):
        # Initialize hand tracking module
        self.mp_hands = mp.solutions.hands.Hands()
        # Initialize webcam
        self.cap = cv2.VideoCapture(video)
        # Initialize variables for FPS calculation
        self.prev_time = 0
        self.curr_time = 0
        
    def __del__(self):
        # Release webcam and destroy windows
        self.cap.release()
        cv2.destroyAllWindows()
    
    def run(self):
        # Read frame from webcam
        ret, frame = self.cap.read()

        # Convert frame to RGB
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Process frame with hand tracking module
        results = self.mp_hands.process(frame_rgb)

        # Draw landmarks on frame
        self.index_finger_coordinates = []
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                for idx, landmark in enumerate(hand_landmarks.landmark):
                    if idx == mp.solutions.hands.HandLandmark.INDEX_FINGER_TIP:
                        self.index_finger_coordinates.append((int(landmark.x * frame.shape[1]), int(landmark.y * frame.shape[0])))
                        # Draw landmark on frame
                        cv2.circle(frame, (int(landmark.x * frame.shape[1]), int(landmark.y * frame.shape[0])), 5, (0, 255, 0), -1)                            
        # Calculate and display FPS
        self.curr_time = time.time()
        fps = 1 / (self.curr_time - self.prev_time)
        self.prev_time = self.curr_time
        cv2.putText(frame, f"FPS: {int(fps)}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # Show frame
        cv2.imshow('Hand Tracking', frame)
        
    def getIndexFingerCoordinates(self):
        # adjust this function to match the paddel y-coordinate to the finger tips
        # Get fingertip positions
        self.fingertip_pos_left = None
        self.fingertip_pos_right = None
        fingertips_array = np.array(self.index_finger_coordinates)
        if fingertips_array.shape[0] == 2:
            self.fingertip_pos_left = fingertips_array[np.argmax(fingertips_array[:,0]),1]
            self.fingertip_pos_right = fingertips_array[np.argmin(fingertips_array[:,0]),1]
        # return self.fingertip_pos_left, self.fingertip_pos_right
        
    # def getIndexFingerCoordinates_left(self):
    #     self.getIndexFingerCoordinates()
    #     return self.fingertip_pos_left
    
    # def getIndexFingerCoordinates_right(self):
    #     self.getIndexFingerCoordinates()
    #     return self.fingertip_pos_right
        
    def getIndexFingerPosLeft(self):
        self.getIndexFingerCoordinates()
        return self.fingertip_pos_left
    
    def getIndexFingerPosRight(self):
        self.getIndexFingerCoordinates()
        return self.fingertip_pos_right

if __name__ == '__main__':
    hand_recognition = HandRecognition(0)
    while True:
        # Break loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'): 
            break
        
        hand_recognition.run()
        print(hand_recognition.getIndexFingerCoordinates())
            
    del hand_recognition
    