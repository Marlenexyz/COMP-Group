import cv2
import numpy as np

class FrameMatching:
    def __init__(self):
        pass

    def run(self, frame):
        
        # Convert image to HSV color space
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Define lower and upper bounds for red color
        lower_red1 = np.array([0, 100, 100])
        upper_red1 = np.array([5, 255, 255])
        lower_red2 = np.array([355, 100, 100])
        upper_red2 = np.array([360, 255, 255])

        # Threshold the image to get only red colors
        mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
        mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
        red_mask = cv2.bitwise_or(mask1, mask2)
        
        # cv2.imshow('red mask', red_mask)

        # Dilate the mask to merge adjacent red regions
        kernel = np.ones((5, 5), np.uint8)
        red_mask_dilated = cv2.dilate(red_mask, kernel, iterations=1)
        
        # cv2.imshow('red mask dilated', red_mask_dilated)

        # Find contours in the mask
        contours, _ = cv2.findContours(red_mask_dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # Find the four largest contours based on area
        contours = sorted(contours, key=cv2.contourArea, reverse=True)[:4]

        # List to hold the corners
        corners = []
        for contour in contours:
            
            M = cv2.moments(contour)
            cx = int(M['m10'] / M['m00'])
            cy = int(M['m01'] / M['m00'])

            corners.append((cx, cy))
            
        # sort corners by upper left, lower left, upper right, lower right by using distance to (0,0)
        corners_sorted = sorted(corners, key=lambda corner: corner[0] ** 2 + corner[1] ** 2)
            
        # Print corners onto frame
        for corner in corners_sorted:
            cv2.circle(frame, corner, 5, (0, 0, 255), -1)
        cv2.imshow('corners', frame)
        
        return corners_sorted



if __name__ == '__main__':
    detector = FrameMatching()
    frame = cv2.imread('test_red_corners.jpg')
    frame = cv2.resize(frame, None, fx=0.2, fy=0.2)
    corners = detector.run(frame)
    for corner in corners:
        cv2.circle(frame, corner, 5, (0, 0, 255), -1)
    cv2.imshow('frame', frame)
    print(corners)
    
    # Wait for key press
    cv2.waitKey(0)
