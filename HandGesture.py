import cv2
import mediapipe as mp
import serial
import time
import numpy as np

# Initialize the mediapipe hands module
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_draw = mp.solutions.drawing_utils

# Initialize serial communication
# Replace 'COM3' with the correct port for your setup
# serial_port = serial.Serial('COM3', 9600, timeout=1)
time.sleep(2)  # Wait for the serial connection to initialize

# Function to detect gestures
def detect_gesture(hand_landmarks, prev_landmarks):
    gesture = "Unknown"

    # Thumb Up
    thumb_up = hand_landmarks[4].y < hand_landmarks[3].y and \
               all(hand_landmarks[i].y > hand_landmarks[i-2].y for i in [8, 12, 16, 20])

    # Thumb Down
    thumb_down = hand_landmarks[4].y > hand_landmarks[3].y and \
                 all(hand_landmarks[i].y > hand_landmarks[i-2].y for i in [8, 12, 16, 20])

    # OK Gesture
    ok_gesture = (abs(hand_landmarks[4].x - hand_landmarks[8].x) < 0.05 and
                  abs(hand_landmarks[4].y - hand_landmarks[8].y) < 0.05 and
                  all(hand_landmarks[i].y < hand_landmarks[i-2].y for i in [12, 16, 20]))

    # Rock Gesture
    rock_gesture = (hand_landmarks[8].y < hand_landmarks[6].y and
                    hand_landmarks[20].y < hand_landmarks[18].y and
                    hand_landmarks[12].y > hand_landmarks[10].y and
                    hand_landmarks[16].y > hand_landmarks[14].y)

    # Pointing Gesture
    pointing_gesture = (hand_landmarks[8].y < hand_landmarks[6].y and
                        all(hand_landmarks[i].y > hand_landmarks[i-2].y for i in [12, 16, 20]) and
                        hand_landmarks[4].y > hand_landmarks[3].y)

    # Scissors Gesture
    scissors_gesture = (hand_landmarks[8].y < hand_landmarks[6].y and
                        hand_landmarks[12].y < hand_landmarks[10].y and
                        all(hand_landmarks[i].y > hand_landmarks[i-2].y for i in [16, 20]))

    # Finger Center (f***) Gesture
    middle_finger = (hand_landmarks[12].y < hand_landmarks[10].y and
                     all(hand_landmarks[i].y > hand_landmarks[i-2].y for i in [8, 16, 20]))

    # Waving Gesture (requires previous frame)
    if prev_landmarks is not None:
        hand_movement = np.linalg.norm(np.array([hand_landmarks[0].x, hand_landmarks[0].y]) -
                                       np.array([prev_landmarks[0].x, prev_landmarks[0].y]))
        waving = hand_movement > 0.1
    else:
        waving = False

    # Peace Sign Gesture
    peace_sign = (hand_landmarks[8].y < hand_landmarks[6].y and
                  hand_landmarks[12].y < hand_landmarks[10].y and
                  all(hand_landmarks[i].y > hand_landmarks[i-2].y for i in [4, 16, 20]))

    # Fist Bump Gesture
    fist_bump = (hand_landmarks[8].y > hand_landmarks[6].y and
                 all(hand_landmarks[i].y < hand_landmarks[i-2].y for i in [4, 12, 16, 20]))

    # High Five Gesture
    high_five = (all(hand_landmarks[i].y < hand_landmarks[i-2].y for i in [4, 8, 12, 16, 20]))

    # Crossed Fingers Gesture
    crossed_fingers = (hand_landmarks[8].y < hand_landmarks[6].y and
                       hand_landmarks[12].y < hand_landmarks[10].y and
                       hand_landmarks[8].x < hand_landmarks[12].x and
                       hand_landmarks[12].x < hand_landmarks[8].x)

    if thumb_up:
        gesture = "Thumb Up"
    elif thumb_down:
        gesture = "Thumb Down"
    elif ok_gesture:
        gesture = "OK"
    elif rock_gesture:
        gesture = "Rock"
    elif pointing_gesture:
        gesture = "Pointing"
    elif scissors_gesture:
        gesture = "Scissors"
    elif middle_finger:
        gesture = "Middle Finger"
    elif waving:
        gesture = "Waving"
    elif peace_sign:
        gesture = "Peace Sign"
    elif fist_bump:
        gesture = "Fist Bump"
    elif high_five:
        gesture = "High Five"
    elif crossed_fingers:
        gesture = "Crossed Fingers"

    return gesture

# Open the webcam
cap = cv2.VideoCapture(0)
prev_landmarks = None

while True:
    success, img = cap.read()
    if not success:
        break

    # Convert the BGR image to RGB
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Process the RGB image to detect hands
    results = hands.process(img_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Detect gesture
            gesture = detect_gesture(hand_landmarks.landmark, prev_landmarks)
            prev_landmarks = hand_landmarks.landmark

            # Log the gesture to console
            print(f'Gesture detected: {gesture}')

            # Send the gesture via USB
            # serial_port.write(f'{gesture}\n'.encode())

            # Display the gesture on the image
            cv2.putText(img, f'Gesture: {gesture}', (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
    else:
        prev_landmarks = None

    # Show the image with hand landmarks
    cv2.imshow("Hand Gesture Recognition", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
# serial_port.close()
