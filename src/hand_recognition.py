import cv2
import mediapipe as mp
import time
import numpy as np

class HandRecognition:

    detections = 0
    iterations = 0
    accuracy = 0
    measure = 0
    measure_alt = 0

    '''hand recognition class which uses mediapipe library to recognize hand landmarks and draw them on self.frame'''
    def __init__(self):
        # Initialize hand tracking module
        self.mp_hands = mp.solutions.hands.Hands()
    
    def run(self, frame):
        self.frame = frame
        frame_rgb = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)

        # Process self.frame with hand tracking module
        results = self.mp_hands.process(frame_rgb)
        
        #calculate accuracy
        if cv2.waitKey(1) & 0xFF == ord('k'):
            self.measure = 1
        if self.measure == 1:
            hand_recognition.measureAccuracy()
        if cv2.waitKey(1) & 0xFF == ord('l'):
            if self.measure == 0:
                self.measure = 0
            else:
                self.measure = 2
            # don't detect the key 'l' being pressed for 1 second
            
        if self.measure == 2:
            acc = hand_recognition.stopAccuracyMeasurement()
            print("Hands were recognized with an accuracy of " + str(acc))
            self.measure = 0
        if self.measure != self.measure_alt:
            if self.measure == 0:
                print("not measuring")
            elif self.measure == 1:
                print("measuring")
            elif self.measure == 2:
                print("stopped measuring")
            self.measure_alt = self.measure

        # Draw landmarks on self.frame
        self.index_finger_coordinates = []
        self.middle_finger_coordinates = []
        self.thumb_coordinates = []
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                for idx, landmark in enumerate(hand_landmarks.landmark):
                    if idx == mp.solutions.hands.HandLandmark.INDEX_FINGER_TIP:
                        self.index_finger_coordinates.append((int(landmark.x * self.frame.shape[1]), int(landmark.y * self.frame.shape[0])))
                        cv2.circle(self.frame, (int(landmark.x * self.frame.shape[1]), int(landmark.y * self.frame.shape[0])), 5, (0, 255, 0), -1)
                    if idx == mp.solutions.hands.HandLandmark.MIDDLE_FINGER_TIP:
                        self.middle_finger_coordinates.append((int(landmark.x * self.frame.shape[1]), int(landmark.y * self.frame.shape[0])))
                        cv2.circle(self.frame, (int(landmark.x * self.frame.shape[1]), int(landmark.y * self.frame.shape[0])), 5, (0, 255, 255), -1)
                    if idx == mp.solutions.hands.HandLandmark.THUMB_TIP:
                        self.thumb_coordinates.append((int(landmark.x * self.frame.shape[1]), int(landmark.y * self.frame.shape[0])))
                        cv2.circle(self.frame, (int(landmark.x * self.frame.shape[1]), int(landmark.y * self.frame.shape[0])), 5, (0, 255, 255), -1)  
        
        
    # define a function to measure how often a hand is detected
    def measureAccuracy(self):
     
        
        if len(self.index_finger_coordinates) > 0 or len(self.middle_finger_coordinates) > 0 or len(self.thumb_coordinates) > 0:
            self.detections += 1
        
        self.iterations += 1
        if cv2.waitKey(1) & 0xFF == ord('l'):
            self.measure = 2
        # end the while loop when a button is pressed
        # if cv2.waitKey(1) & 0xFF == ord('l'):
            
        #     accuracy = self.detections/self.iterations
        #     return accuracy
        # else:
        #     return None
    def stopAccuracyMeasurement(self):
        self.accuracy = self.detections/self.iterations
        return self.accuracy


    def storeIndexFingerCoordinates(self):
        # adjust this function to match the paddel y-coordinate to the finger tips
        # Get fingertip positions
        self.fingertip_pos_left = None
        self.fingertip_pos_right = None
        self.fingertip_coord_right = None
        self.fingertip_coord_left = None
        self.fingertip_coord_both = None
        fingertips_array = np.array(self.index_finger_coordinates)
        self.fingertip_coord_both = fingertips_array
        if fingertips_array.shape[0] >= 2:
            self.fingertip_pos_left = fingertips_array[np.argmin(fingertips_array[:,0]),1]
            self.fingertip_coord_left = fingertips_array[np.argmin(fingertips_array[:,0]),:]
            self.fingertip_pos_right = fingertips_array[np.argmax(fingertips_array[:,0]),1]
            self.fingertip_coord_right = fingertips_array[np.argmax(fingertips_array[:,0]),:]
        else: 
            if fingertips_array.shape[0] == 1:
                if fingertips_array[0,0] < 0.5*self.frame.shape[1]:
                    self.fingertip_pos_left = fingertips_array[0,1]
                    self.fingertip_coord_left = fingertips_array[0,:]
                else:
                    self.fingertip_pos_right = fingertips_array[0,1]
                    self.fingertip_coord_right = fingertips_array[0,:]
        
    # define function to return the coordinates of the middle finger

    def storeMiddleFingerCoordinates(self):
        self.middlefingertip_pos_left = None
        self.middlefingertip_pos_right = None
        self.middlefingertip_coord_right = None
        self.middlefingertip_coord_left = None
        self.middlefingertip_coord_both = None

        fingertips_array = np.array(self.middle_finger_coordinates)
        self.middlefingertip_coord_both = fingertips_array
        if fingertips_array.shape[0] >= 2:
            self.middlefingertip_pos_left = fingertips_array[np.argmin(fingertips_array[:,0]),1]
            self.middlefingertip_coord_left = fingertips_array[np.argmin(fingertips_array[:,0]),:]
            self.middlefingertip_coord_right = fingertips_array[np.argmax(fingertips_array[:,0]),:]
            self.middlefingertip_pos_right = fingertips_array[np.argmax(fingertips_array[:,0]),1]
        else:
            if fingertips_array.shape[0] == 1:
                if fingertips_array[0,0] < 0.5*self.frame.shape[1]:
                    self.middlefingertip_pos_left = fingertips_array[0,1]
                    self.middlefingertip_coord_left = fingertips_array[0,:]
                else:
                    self.middlefingertip_pos_right = fingertips_array[0,1]
                    self.middlefingertip_coord_right = fingertips_array[0,:]
        # Get the coordinates of middle fingers
        

    def storeThumbCoordinates(self):
        # adjust this function to match the paddel y-coordinate to the finger tips
        # Get fingertip positions
        self.thumbtip_coord_right = None
        self.thumbtip_coord_left = None
        self.thumbtip_coord_both = None

        fingertips_array = np.array(self.thumb_coordinates)
        self.thumbtip_coord_both = fingertips_array
        if fingertips_array.shape[0] >= 2:
            self.thumbtip_coord_left = fingertips_array[np.argmin(fingertips_array[:,0]),:]
            self.thumbtip_coord_right = fingertips_array[np.argmax(fingertips_array[:,0]),:]
        elif fingertips_array.shape[0] == 1:
                if fingertips_array[0,0] < 0.5 * self.frame.shape[1]:
                    self.thumbtip_coord_left = fingertips_array[0, :]
                else:
                    self.thumbtip_coord_right = fingertips_array[0,:]

        
    def getIndexFingerPosLeft(self):
        self.storeIndexFingerCoordinates()
        return self.fingertip_pos_left
    
    def getIndexFingerPosRight(self):
        self.storeIndexFingerCoordinates()
        return self.fingertip_pos_right
        
    def getMiddleFingerPosLeft(self):
        self.storeMiddleFingerCoordinates()
        return self.middlefingertip_pos_left
    
    def getMiddleFingerPosRight(self):
        self.storeMiddleFingerCoordinates()
        return self.middlefingertip_pos_right
    
    def getIndexFingerCoordLeft(self):
        self.storeIndexFingerCoordinates()
        return self.fingertip_coord_left
    
    def getIndexFingerCoordRight(self):
        self.storeIndexFingerCoordinates()
        return self.fingertip_coord_right
    
    def getIndexFingerCoordBoth(self):
        self.storeIndexFingerCoordinates()
        return self.fingertip_coord_both
    
    def getMiddleFingerCoordLeft(self):
        self.storeMiddleFingerCoordinates()
        return self.middlefingertip_coord_left
    
    def getMiddleFingerCoordRight(self):
        self.storeMiddleFingerCoordinates()
        return self.middlefingertip_coord_right
    
    def getMiddleFingerCoordBoth(self):
        self.storeMiddleFingerCoordinates()
        return self.middlefingertip_coord_both
    
    def getThumbCoordLeft(self):
        self.storeThumbCoordinates()
        return self.thumbtip_coord_left
    
    def getThumbCoordRight(self):
        self.storeThumbCoordinates()
        return self.thumbtip_coord_right
    
    def getThumbCoordBoth(self):
        self.storeThumbCoordinates()
        return self.thumbtip_coord_both

    # define a function to detect if index finger and thumb are touching
    def isTouchingIndexFingerAndThumb(self, side):
        """Check if the index finger and thumb are touching."""
        # Assuming index_finger_coordinates and thumb_coordinates are available
        # and each contains (x, y) tuples for the respective fingertip positions.
        
        # This threshold determines how close the two fingers can be to be considered touching
        TOUCH_THRESHOLD = 15
        
        # Function to calculate distance between two points
        def distance(point1, point2):
            return ((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2) ** 0.5
        index_finger_coordinates_left = self.getIndexFingerCoordLeft()
        thumb_coordinates_left = self.getThumbCoordLeft()
        index_finger_coordinates_right = self.getIndexFingerCoordRight()
        thumb_coordinates_right = self.getThumbCoordRight()
        index_finger_coordinates_both = self.getIndexFingerCoordBoth()
        thumb_coordinates_both = self.getThumbCoordBoth()
        # Calculate the distance between the index finger and thumb
        if side is None:
            if index_finger_coordinates_both is None or thumb_coordinates_both is None:
                return False
            else:
                distance_between_fingers = distance(index_finger_coordinates_both[0, :], thumb_coordinates_both[0, :])
        if side == "left":
            if index_finger_coordinates_left is None or thumb_coordinates_left is None:
                return False
            else:
                distance_between_fingers = distance(index_finger_coordinates_left, thumb_coordinates_left)
        elif side == "right":
            if index_finger_coordinates_right is None or thumb_coordinates_right is None:
                return False
            else:
                distance_between_fingers = distance(index_finger_coordinates_right, thumb_coordinates_right)
        
        # Check if the distance is less than the threshold
        if distance_between_fingers < TOUCH_THRESHOLD:
            return True
        else:
            return False
    def isVShape(self):
        """Check if the index finger and middle finger are held up in a V-shape."""
        # Assuming index_finger_coordinates and middle_finger_coordinates are available
        # and each contains (x, y) tuples for the respective fingertip positions.
        
        # This threshold determines how close the two fingers can be to be considered a V-shape
        V_SHAPE_THRESHOLD = 15
        
        # Function to calculate distance between two points
        def calculate_distance(point1, point2):
            return ((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2) ** 0.5
        
        # Get the coordinates for index and middle fingertips
        index_fingertip_right = self.getIndexFingerCoordRight() #if self.fingertip_pos_right else None
        middle_fingertip_right = self.getMiddleFingerCoordRight()  
        index_fingertip_left = self.getIndexFingerCoordLeft()
        middle_fingertip_left = self.getMiddleFingerCoordLeft()
        thumb_tip_left = self.getThumbCoordLeft()
        thumb_tip_right = self.getThumbCoordRight()

        # Check if both fingertips are detected
        if index_fingertip_right is not None and middle_fingertip_right is not None:
            # Calculate the distance between the fingertips
            distance = calculate_distance(index_fingertip_right, middle_fingertip_right)
            
            # Check if the distance between the fingertips is greater than the threshold
            if distance > V_SHAPE_THRESHOLD:
                # Check if the fingertips are at a similar height to form a V-shape
                if abs(index_fingertip_right[1] - middle_fingertip_right[1]) < V_SHAPE_THRESHOLD and (index_fingertip_right[1] - thumb_tip_right[1]) > V_SHAPE_THRESHOLD:
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
    cap = cv2.VideoCapture(0)
    hand_recognition = HandRecognition()
    while True:
        # Break loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
        ret, frame = cap.read()
        hand_recognition.run(frame)
        
        # Check for fingers touching
        if hand_recognition.isTouchingIndexFingerAndThumb('left'):
            cv2.putText(frame, "left fingers touching", (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        if hand_recognition.isTouchingIndexFingerAndThumb('right'):
            cv2.putText(frame, "right fingers touching", (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        # Check for V-Shape
        if hand_recognition.isVShape():
            cv2.putText(frame, "V-Shape", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        cv2.imshow('frame', frame)
        # if cv2.waitKey(1) & 0xFF == ord('k'):
        #     HandRecognition.measure = 1
        # if HandRecognition.measure == 1:
        #     hand_recognition.measureAccuracy()
        # if cv2.waitKey(1) & 0xFF == ord('l'):
        #     HandRecognition.measure = 2
        # if HandRecognition.measure == 2:
        #     acc = hand_recognition.stopAccuracyMeasurement()
        #     print(acc)
        #     HandRecognition.measure = 0
        # print (HandRecognition.measure)
    # Release webcam and destroy windows
    cap.release()
    cv2.destroyAllWindows()
    