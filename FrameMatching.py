import cv2
import numpy as np

class RedRectangleDetector:
    def __init__(self):
        pass

    def find_red_corners(self, frame):
        # Convert image to HSV color space
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Define lower and upper bounds for red color
        lower_red1 = np.array([0, 120, 70])
        upper_red1 = np.array([10, 255, 255])
        lower_red2 = np.array([170, 120, 70])
        upper_red2 = np.array([180, 255, 255])

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

        # List to hold the corners of the rectangle
        rectangle_corners = []

        # Find the bounding boxes for the largest contoursfor contour in contours:
        for contour in contours:
            approx = cv2.approxPolyDP(contour, 0.01* cv2.arcLength(contour, True), True)
            cv2.drawContours(frame, [approx], 0, (0, 0, 0), 5)
            x = approx.ravel()[0]
            y = approx.ravel()[1] - 5
            if len(approx) == 3:
                cv2.putText( frame, "Triangle", (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0) )
            elif len(approx) == 4 :
                x, y , w, h = cv2.boundingRect(approx)
                aspectRatio = float(w)/h
                print(aspectRatio)
                if aspectRatio >= 0.95 and aspectRatio < 1.05:
                    cv2.putText(frame, "square", (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0))

                else:
                    cv2.putText(frame, "rectangle", (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0))

            elif len(approx) == 5 :
                cv2.putText(frame, "pentagon", (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0))
            elif len(approx) == 10 :
                cv2.putText(frame, "star", (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0))
            else:
                cv2.putText(frame, "circle", (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0))

        return rectangle_corners

if __name__ == '__main__':
    while True:
        detector = RedRectangleDetector()
        cap = cv2.VideoCapture('https://192.168.1.76:8080/video')
        ret, frame = cap.read()
        corners = detector.find_red_corners(frame)
        cv2.imshow('frame', frame)
        print(corners)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()
    
