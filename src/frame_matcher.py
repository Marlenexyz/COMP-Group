import cv2
import numpy as np
import time



class FrameMatcher:
    def __init__(self):
        """
        Initialize frame matcher
        """
        
        # Define HSV lower and upper bounds
        self.lower_yellow = np.array([20, 100, 100])
        self.upper_yellow = np.array([30, 255, 255])

    def run(self, frame):
        """
        Run the frame matcher on the given frame. Returns the center points
        of the 4 biggest contours considering the color bounds. Returns None
        if no contours were found.
        """
        
        # Convert image to HSV color space
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Threshold the image to get only colors in range
        mask = cv2.inRange(hsv, self.lower_yellow, self.upper_yellow)
        
        # cv2.imshow('mask', mask)

        # Dilate the mask to merge adjacent regions
        kernel = np.ones((5, 5), np.uint8)
        mask_dilated = cv2.dilate(mask, kernel, iterations=1)
        
        # cv2.imshow('mask dilated', mask_dilated)

        # Find contours in the mask
        contours, _ = cv2.findContours(mask_dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # Find the 4 largest contours based on area
        contours = sorted(contours, key=cv2.contourArea, reverse=True)[:4]
        
        # return only if 4 corners were found
        if len(contours) < 4:
            return None

        # Get the center of each contour
        corners = []
        for contour in contours:
            M = cv2.moments(contour)
            cx = int(M['m10'] / M['m00'])
            cy = int(M['m01'] / M['m00'])
            corners.append((cx, cy))
            
        # Sort corners by upper left, lower left, upper right, lower right by using distance to (0,0)
        corners_sorted = sorted(corners, key=lambda corner: corner[0] ** 2 + corner[1] ** 2)  
            
        # Print corners onto frame
        for corner in corners_sorted:
            cv2.circle(frame, corner, 5, (0, 0, 255), -1)
            
        # cv2.imshow('corners', frame)
        
        return corners_sorted
    
    def calibrateCorners(self, cap):
        """
        Run the frame matcher over n_iter iterations and calculate the mean average corners.
        """
        
        n_iter = 100
        delay_time = 0.01
        
        print('Calibrating...')
        
        corners_list = []
        for i in range(n_iter):
            time.sleep(delay_time)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            ret, frame = cap.read()
            if ret == False:
                continue
        
            corners = self.run(frame)
            if corners is None:
                continue
            corners_list.append(corners)
            cv2.imshow('Calibrate', frame)
            
        # Calculate the average over all corners
        corners_avg = np.mean(np.array(corners_list), axis=0)
        corners_avg = list(map(tuple, corners_avg.astype(int)))
        print(f'    Corners calibrated: {corners_avg}')
        
        return corners_avg
            
            
    
    def measureAccuracy(self, cap):
        """
        Measure accuracy of frame matcher over n_iter iterations.
        """
        n_iter = 100
        min_angle = 80
        max_angle = 100
        
        print('Start measuring accuracy of frame matcher...')
        
        n_precise_matches = 0
        n_recalled_matches = 0
        for i in range(n_iter):
            # time.sleep(0.1)
            # if cv2.waitKey(1) & 0xFF == ord('q'):
            #     break
            
            print(f'Frame {i + 1}...')
            ret, frame = cap.read()
            if ret == False:
                print('    no frame captured...')
                continue
            
            # find the corners
            corners = self.run(frame)
            if corners is None:
                print('    no corners found...')
                continue
            print(f'    Corners: {corners}')
            # cv2.imshow('Measure Accuracy', frame)
            
            # calculate the angles
            angles = self._calculateAngles(corners)
            if angles is None:
                print('    no angles found...')
                continue
            print(f'    Angles: {angles}')
            
            # add 1 to n_recalled_matches if all angles found
            n_recalled_matches += 1
            
            # add 1 to n_precise_matches if all angles in range
            if all(angle >= min_angle and angle <= max_angle for angle in angles):
                print('    Good match!')
                n_precise_matches += 1
            else:
                print('    Bad match...')
                
        # calculate the accuracy
        precision = n_precise_matches / n_iter
        recall = n_recalled_matches / n_iter
        print(f'precision: {round(precision, 2)}, recall: {round(recall, 2)}')
        
        return precision, recall

    def _calculateAngles(self, corners):
        """
        Calculate angles between four corners in the following order:
        upper left, lower left, upper right, lower right.
        """
        
        if len(corners) != 4:
            return None

        # Define the corner points
        ul, ll, ur, lr = corners

        # Calculate the vectors
        vector_ul_ll = np.array([ll[0] - ul[0], ll[1] - ul[1]])
        vector_ll_lr = np.array([lr[0] - ll[0], lr[1] - ll[1]])
        vector_lr_ur = np.array([ur[0] - lr[0], ur[1] - lr[1]])
        vector_ur_ul = np.array([ul[0] - ur[0], ul[1] - ur[1]])

        # Define a function to calculate the angle between two vectors
        def angle_between(v1, v2):
            dot_product = np.dot(v1, v2)
            magnitude_v1 = np.sqrt(v1[0] ** 2 + v1[1] ** 2)
            magnitude_v2 = np.sqrt(v2[0] ** 2 + v2[1] ** 2)
            angle_rad = np.arccos(dot_product / (magnitude_v1 * magnitude_v2))
            angle_deg = np.degrees(angle_rad)
            return angle_deg

        # Calculate the angles between the vectors
        angle_ll = angle_between(vector_ul_ll, vector_ll_lr)
        angle_lr = angle_between(vector_ll_lr, vector_lr_ur)
        angle_ur = angle_between(vector_lr_ur, vector_ur_ul)
        angle_ul = angle_between(vector_ur_ul, vector_ul_ll)

        # Return the angles in degrees
        return [angle_ll, angle_lr, angle_ur, angle_ul]
        



if __name__ == '__main__':
    frame_matcher = FrameMatcher()
    # frame = cv2.imread('test_red_corners.jpg')
    # frame = cv2.resize(frame, None, fx=0.2, fy=0.2)
    # corners = frame_matcher.run(frame)
    # for corner in corners:
    #     cv2.circle(frame, corner, 5, (0, 0, 255), -1)
    # cv2.imshow('frame', frame)
    # print(corners)
    # # Wait for key press
    # cv2.waitKey(0)
    
    cap = cv2.VideoCapture(0)
    # frame_matcher.measureAccuracy(cap)
    corners = frame_matcher.calibrateCorners(cap)
    
    cap.release()
    cv2.destroyAllWindows()
    