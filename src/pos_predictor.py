import cv2
import numpy as np

class PosPredictor:
    
    def __init__(self, initial_pos_left, initial_pos_right):
        
        self.kalman_filter_left = cv2.KalmanFilter(1, 1)
        self.kalman_filter_left.transitionMatrix = np.array([1], dtype=np.float32)
        self.kalman_filter_left.measurementMatrix = np.eye(1, 1, dtype=np.float32)
        self.kalman_filter_left.processNoiseCov = 1e-3 * np.eye(1, 1, dtype=np.float32)
        self.kalman_filter_left.measurementNoiseCov = 1e-3 * np.eye(1, 1, dtype=np.float32)
        self.kalman_filter_left.statePost = np.array([initial_pos_left], dtype=np.float32)
        self.kalman_filter_left.errorCovPost = np.ones((1, 1), dtype=np.float32)
        
        self.kalman_filter_right = cv2.KalmanFilter(1, 1)
        self.kalman_filter_right.transitionMatrix = np.array([1], dtype=np.float32)
        self.kalman_filter_right.measurementMatrix = np.eye(1, 1, dtype=np.float32)
        self.kalman_filter_right.processNoiseCov = 1e-3 * np.eye(1, 1, dtype=np.float32)
        self.kalman_filter_right.measurementNoiseCov = 1e-3 * np.eye(1, 1, dtype=np.float32)
        self.kalman_filter_right.statePost = np.array([initial_pos_right], dtype=np.float32)
        self.kalman_filter_right.errorCovPost = np.ones((1, 1), dtype=np.float32)
        
    def predictLeft(self):
        prediction = self.kalman_filter_left.predict()
        predicted_pos = prediction.squeeze().astype(int).tolist()
        return predicted_pos
    
    def predictRight(self):
        prediction = self.kalman_filter_right.predict()
        predicted_pos = prediction.squeeze().astype(int).tolist()
        return predicted_pos
    
    def correctLeft(self, last_pos):
        measurement = np.array([last_pos], dtype=np.float32).reshape(-1 , 1)
        self.kalman_filter_left.correct(measurement)
        
    def correctRight(self, last_pos):
        measurement = np.array([last_pos], dtype=np.float32).reshape(-1 , 1)
        self.kalman_filter_right.correct(measurement)
            