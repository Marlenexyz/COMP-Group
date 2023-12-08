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
        
        self.middle_finger_coordinates = []
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                for idx, landmark in enumerate(hand_landmarks.landmark):
                    if idx == mp.solutions.hands.HandLandmark.MIDDLE_FINGER_TIP:
                        self.middle_finger_coordinates.append((int(landmark.x * frame.shape[1]), int(landmark.y * frame.shape[0])))
                        cv2.circle(frame, (int(landmark.x * frame.shape[1]), int(landmark.y * frame.shape[0])), 5, (0, 255, 255), -1)   
                        
        
        # Calculate and display FPS
        self.curr_time = time.time()
        fps = 1 / (self.curr_time - self.prev_time)
        self.prev_time = self.curr_time
        cv2.putText(frame, f"FPS: {int(fps)}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
       
        if self.isVShape(frame):
            cv2.putText(frame, "V-Shape", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        # Show frame
        cv2.imshow('Hand Tracking', frame)
        
    def getIndexFingerCoordinates(self):
        # adjust this function to match the paddel y-coordinate to the finger tips
        # Get fingertip positions
        self.fingertip_pos_left = None
        self.fingertip_pos_right = None
        self.fingertip_coord_right = None
        self.fingertip_coord_left = None
        fingertips_array = np.array(self.index_finger_coordinates)
        if fingertips_array.shape[0] == 2:
            self.fingertip_pos_left = fingertips_array[np.argmax(fingertips_array[:,0]),1]
            self.fingertip_coord_left = fingertips_array[np.argmax(fingertips_array[:,0]),:]
            self.fingertip_pos_right = fingertips_array[np.argmin(fingertips_array[:,0]),1]
            self.fingertip_coord_right = fingertips_array[np.argmin(fingertips_array[:,0]),:]
        
    # define function to return the coordinates of the middle finger

    def getMiddleFingerCoordinates(self):
        self.middlefingertip_pos_left = None
        self.middlefingertip_pos_right = None
        self.middlefingertip_coord_right = None
        self.middlefingertip_coord_left = None
        fingertips_array = np.array(self.middle_finger_coordinates)
        if fingertips_array.shape[0] == 2:
            self.middlefingertip_pos_left = fingertips_array[np.argmax(fingertips_array[:,0]),1]
            self.middlefingertip_coord_left = fingertips_array[np.argmax(fingertips_array[:,0]),:]
            self.middlefingertip_coord_right = fingertips_array[np.argmin(fingertips_array[:,0]),:]
            self.middlefingertip_pos_right = fingertips_array[np.argmin(fingertips_array[:,0]),1]
        # Get the coordinates of middle fingers
        

    def getIndexFingerPosLeft(self):
        self.getIndexFingerCoordinates()
        return self.fingertip_pos_left
    
    def getIndexFingerPosRight(self):
        self.getIndexFingerCoordinates()
        return self.fingertip_pos_right
        
    def getMiddleFingerPosLeft(self):
        self.getMiddleFingerCoordinates()
        return self.middlefingertip_pos_left
    
    def getMiddleFingerPosRight(self):
        self.getMiddleFingerCoordinates()
        return self.middlefingertip_pos_right
    
    def getIndexFingerCoordLeft(self):
        self.getIndexFingerCoordinates()
        return self.fingertip_coord_left
    
    def getIndexFingerCoordRight(self):
        self.getIndexFingerCoordinates()
        return self.fingertip_coord_right
    
    def getMiddleFingerCoordLeft(self):
        self.getMiddleFingerCoordinates()
        return self.middlefingertip_coord_left
    
    def getMiddleFingerCoordRight(self):
        self.getMiddleFingerCoordinates()
        return self.middlefingertip_coord_right
    
    #define function to return if two fingers are held up in a peace sign
    def isPeaceSign(self):
        if self.fingertip_pos_left is not None and self.fingertip_pos_right is not None:
            return self.fingertip_pos_left > self.fingertip_pos_right
        else:
            return False
    def isVShape(self, frame):
        """Check if the index finger and middle finger are held up in a V-shape."""
        # Assuming index_finger_coordinates and middle_finger_coordinates are available
        # and each contains (x, y) tuples for the respective fingertip positions.
        
        # This threshold determines how close the two fingers can be to be considered a V-shape
        V_SHAPE_THRESHOLD = 30
        
        # Function to calculate distance between two points
        def calculate_distance(point1, point2):
            return ((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2) ** 0.5
        
        # Get the coordinates for index and middle fingertips
        index_fingertip_right = self.getIndexFingerCoordRight() #if self.fingertip_pos_right else None
        middle_fingertip_right = self.getMiddleFingerCoordRight()  # Replace with actual method to get middle_finger_coordinates
        index_fingertip_left = self.getIndexFingerCoordLeft()
        middle_fingertip_left = self.getMiddleFingerCoordLeft()

        # Check if both fingertips are detected
        if index_fingertip_right is not None and middle_fingertip_right is not None:
            # Calculate the distance between the fingertips
            distance = calculate_distance(index_fingertip_right, middle_fingertip_right)
            
            # Check if the distance between the fingertips is greater than the threshold
            if distance > V_SHAPE_THRESHOLD:
                # Check if the fingertips are at a similar height to form a V-shape
                if abs(index_fingertip_right[1] - middle_fingertip_right[1]) < V_SHAPE_THRESHOLD:
                    # if v shape is detected, draw a v-shape on the image 
                    # cv2.line(self.frame, index_fingertip_right, middle_fingertip_right, (0, 255, 0), 2)
                    return True
        
        # Check if both fingertips are detected
        if index_fingertip_left is not None and middle_fingertip_left is not None:
            # Calculate the distance between the fingertips
            distance = calculate_distance(index_fingertip_left, middle_fingertip_left)
            
            # Check if the distance between the fingertips is greater than the threshold
            if distance > V_SHAPE_THRESHOLD:
                # Check if the fingertips are at a similar height to form a V-shape
                if abs(index_fingertip_left[1] - middle_fingertip_left[1]) < V_SHAPE_THRESHOLD:
                    # if v shape is detected, draw a v-shape on the image 
                    # cv2.line(self.frame, index_fingertip_left, middle_fingertip_left, (0, 255, 0), 2)
                    return True
        
        return False

if __name__ == '__main__':
    hand_recognition = HandRecognition(0)
    while True:
        # Break loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'): 
            break
        
        hand_recognition.run()
        print(hand_recognition.getIndexFingerCoordinates())
            
    del hand_recognition
    