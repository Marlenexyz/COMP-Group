import cv2
import mediapipe as mp
import time
import numpy as np
from scipy.spatial.distance import cdist, pdist, squareform

class HandRecognition:
    '''hand recognition class which uses mediapipe library to recognize hand landmarks and draw them on self.frame'''
    def __init__(self):
        # Initialize hand tracking module
        self.mp_hands = mp.solutions.hands.Hands()
        self.detections = 0
        self.iterations = 0
        self.vdetections = 0
        self.viterations = 0
        self.pinchdetections = 0
        self.pinchiterations = 0
        self.recall = 0
        self.vrecall = 0
        self.measure = 0
        self.measure_alt = 0
        self.vmeasure = 0
        self.vmeasure_alt = 0
        self.index_finger_coordinates = []
        self.middle_finger_coordinates = []
        self.thumb_coordinates = []
        # This threshold determines how close the two fingers can be to be considered a V-shape
        self.V_SHAPE_THRESHOLD = 12

    def run(self, frame):
        self.frame = frame
        frame_rgb = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)

        # Process self.frame with hand tracking module
        results = self.mp_hands.process(frame_rgb)

        #calculate accuracy
        # if cv2.waitKey(1) & 0xFF == ord('k'):
        #     self.measure = 1
        # if self.measure == 1:
        #     hand_recognition.measureRecall()
        # if cv2.waitKey(1) & 0xFF == ord('l'):
        #     if self.measure == 0:
        #         self.measure = 0
        #     else:
        #         self.measure = 2
        # if self.measure == 2:
        #     # acc = hand_recognition.stopAccuracyMeasurement()
        #     print("Hands were recognized with a recall of " + str(self.recall))
        #     self.measure = 0
        # if self.measure != self.measure_alt:
        #     if self.measure == 0:
        #         print("not measuring")
        #     elif self.measure == 1:
        #         print("measuring")
        #     elif self.measure == 2:
        #         print("stopped measuring")
        #     self.measure_alt = self.measure

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
    def measureRecall(self,capt):
        #capt = cv2.VideoCapture(0)
        while self.iterations <=100:
            ret, measureframe = capt.read()
            frame_rgb2 = cv2.cvtColor(measureframe, cv2.COLOR_BGR2RGB)

            # Process self.frame with hand tracking module
            results = self.mp_hands.process(frame_rgb2)
            cv2.imshow('Hand Tracking Precision', measureframe)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            if results.multi_hand_landmarks:  
                self.detections += 1   
            # if len(self.index_finger_coordinates) > 0 or len(self.middle_finger_coordinates) > 0 or len(self.thumb_coordinates) > 0:
            #     self.detections += 1
            self.iterations += 1
            # sleep for 10 ms
            time.sleep(0.1)
            #if self.iterations == 100:
        self.measure = 2
        self.recall = self.detections / self.iterations
        self.iterations = 1
        self.detections = 1
        print ("Hands were recognized with a recall of " + str(self.recall))
        return self.recall
            # if cv2.waitKey(1) & 0xFF == ord('l'):
            #     self.measure = 2
        # end the while loop when a button is pressed
        # if cv2.waitKey(1) & 0xFF == ord('l'):
            
        #     recall = self.detections/self.iterations
        #     return recall
        # else:
        #     return None
    def stopRecallMeasurement(self):
        self.recall = self.detections/self.iterations
        return self.recall
    def measureVShapeRecall(self):
        if len(self.isVShape):
            self.vdetections += 1
        
        self.viterations += 1
        if self.viterations == 100:
            self.vmeasure = 2
            self.vrecall = self.vdetections / self.viterations
            self.viterations = 1
            self.vdetections = 2
            return self.vrecall
        if cv2.waitKey(1) & 0xFF == ord('l'):
            self.vmeasure = 2
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
    def isTouchingIndexFingerAndThumb(self, side='both'):
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
        if side == 'both':
            if len(index_finger_coordinates_both) == 0 or len(thumb_coordinates_both) == 0: # or index_finger_coordinates_both is None or thumb_coordinates_both is None:
                return False
            else:
                #distance_between_fingers = distance(index_finger_coordinates_both[0, :], thumb_coordinates_both[0, :])
                distances = cdist(index_finger_coordinates_both, thumb_coordinates_both)
                distance_between_fingers = np.min(distances)
        elif side == "left":
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
    def isVShape(self, side ='both'):
        """Check if the index finger and middle finger are held up in a V-shape."""
        # Assuming index_finger_coordinates and middle_finger_coordinates are available
        # and each contains (x, y) tuples for the respective fingertip positions.
            
        # Function to calculate distance between two points
        def calculate_distance(point1, point2):
            return ((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2) ** 0.5
        
        # Get the coordinates for index and middle fingertips
        index_fingertip_right = self.getIndexFingerCoordRight() #if self.fingertip_pos_right else None
        middle_fingertip_right = self.getMiddleFingerCoordRight()  
        index_fingertip_left = self.getIndexFingerCoordLeft()
        middle_fingertip_left = self.getMiddleFingerCoordLeft()
        index_fingertip_both = self.getIndexFingerCoordBoth()
        middle_fingertip_both = self.getMiddleFingerCoordBoth()
        thumb_tip_left = self.getThumbCoordLeft()
        thumb_tip_right = self.getThumbCoordRight()
        thumb_tip_both = self.getThumbCoordBoth()

        # Check if both fingertips are detected
        if side == 'both':
            if len(index_fingertip_both) > 0 and len(middle_fingertip_both) > 0 and len(thumb_tip_both) > 0: # and index_fingertip_both is not None and middle_fingertip_both is not None and thumb_tip_both is not None:
                # distance = calculate_distance(index_fingertip_both[0, :], middle_fingertip_both[0, :])
                # calculate the distance betweeen all the points in index_fingertip_both and all the points in middle_fingertip_both
                distances_middle = cdist(index_fingertip_both, middle_fingertip_both)
                distances_thumb = cdist(index_fingertip_both, thumb_tip_both)

                # Find the closest middle finger point and thumb point to each index finger point
                closest_middle_points = np.argmin(distances_middle, axis=1)
                closest_thumb_points = np.argmin(distances_thumb, axis=1)

                # Check if the distance is above the threshold
                for i in range(len(index_fingertip_both)):
                    index_point = index_fingertip_both[i]
                    closest_middle_point = middle_fingertip_both[closest_middle_points[i]]
                    closest_thumb_point = thumb_tip_both[closest_thumb_points[i]]
                    distance_middle = distances_middle[i, closest_middle_points[i]]
                    distance_thumb = distances_thumb[i, closest_thumb_points[i]]
    
                    if distance_middle > self.V_SHAPE_THRESHOLD and distance_thumb > self.V_SHAPE_THRESHOLD:
                        if abs(index_point[1] - closest_middle_point[1]) < self.V_SHAPE_THRESHOLD and (closest_thumb_point[1] - index_point[1]) > (self.V_SHAPE_THRESHOLD):
                            return True
                    
        elif side == 'right':
            if index_fingertip_right is not None and middle_fingertip_right is not None and thumb_tip_right is not None:
                # Calculate the distance between the fingertips
                distance = calculate_distance(index_fingertip_right, middle_fingertip_right)
                
                # Check if the distance between the fingertips is greater than the threshold
                if distance > self.V_SHAPE_THRESHOLD:
                    # Check if the fingertips are at a similar height to form a V-shape
                    if abs(index_fingertip_right[1] - middle_fingertip_right[1]) < self.V_SHAPE_THRESHOLD and (thumb_tip_right[1] - index_fingertip_right[1]) > (self.V_SHAPE_THRESHOLD):
                        # if v shape is detected, draw a v-shape on the image 
                        # cv2.line(self.frame, index_fingertip_right, middle_fingertip_right, (0, 255, 0), 2)
                        return True
        elif side == 'left':
            # Check if both fingertips are detected
            if index_fingertip_left is not None and middle_fingertip_left is not None and thumb_tip_left is not None:
                # Calculate the distance between the fingertips
                distance = calculate_distance(index_fingertip_left, middle_fingertip_left)
                
                # Check if the distance between the fingertips is greater than the threshold
                if distance > self.V_SHAPE_THRESHOLD:
                    # Check if the fingertips are at a similar height to form a V-shape
                    if abs(index_fingertip_left[1] - middle_fingertip_left[1]) < self.V_SHAPE_THRESHOLD and (thumb_tip_left[1] - index_fingertip_left[1]) > (self.V_SHAPE_THRESHOLD):
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
        if cv2.waitKey(1 & 0xFF) == ord('k'):
            hand_recognition.measureRecall(cap)
        
        ret, frame = cap.read()
        hand_recognition.run(frame)
        
        # Check for fingers touching
        if hand_recognition.isTouchingIndexFingerAndThumb('left'):
            cv2.putText(frame, "left fingers touching", (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        if hand_recognition.isTouchingIndexFingerAndThumb('right'):
            cv2.putText(frame, "right fingers touching", (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        if hand_recognition.isTouchingIndexFingerAndThumb():
            cv2.putText(frame, "any fingers touching", (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        # Check for V-Shape
        if hand_recognition.isVShape():
            cv2.putText(frame, "V-Shape", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        cv2.imshow('frame', frame)
    # Release webcam and destroy windows
    cap.release()
    cv2.destroyAllWindows()
    