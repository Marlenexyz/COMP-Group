import cv2
import mediapipe as mp
import time

# Initialize hand tracking module
mp_hands = mp.solutions.hands.Hands()

# Initialize webcam
cap = cv2.VideoCapture(0)

# Initialize variables for FPS calculation
prev_time = 0
curr_time = 0

while True:
    # Read frame from webcam
    ret, frame = cap.read()

    # Convert frame to RGB
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process frame with hand tracking module
    results = mp_hands.process(frame_rgb)

    # Draw landmarks on frame
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            for idx, landmark in enumerate(hand_landmarks.landmark):
                # Draw landmark on frame
                cv2.circle(frame, (int(landmark.x * frame.shape[1]), int(landmark.y * frame.shape[0])), 5, (0, 255, 0), -1)

    # Calculate and display FPS
    curr_time = time.time()
    fps = 1 / (curr_time - prev_time)
    prev_time = curr_time
    cv2.putText(frame, f"FPS: {int(fps)}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Show frame
    cv2.imshow('Hand Tracking', frame)

    # Break loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release webcam and destroy windows
cap.release()
cv2.destroyAllWindows()