import cv2
import mediapipe as mp
import serial

# Set the serial port and baud rate for the Arduino
ser = serial.Serial('COM11', 9600)

# Initialize Mediapipe Hand tracking
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

# Initialize servo angles
servo_angle = 90

# Initialize hand tracking
with mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:
    # Open the webcam
    cap = cv2.VideoCapture(0)
    while cap.isOpened():
        # Read the webcam frame
        success, image = cap.read()
        if not success:
            break

        # Convert the frame to RGB
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Flip the image horizontally for a mirrored view
        image = cv2.flip(image, 1)

        # Set the image data to Mediapipe
        image.flags.writeable = False
        results = hands.process(image)

        # Convert the image back to BGR
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # Detect hand landmarks and draw them on the image
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Get the landmarks for index finger
                index_finger = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]

                # Get the x-coordinate of index finger
                index_x = int(index_finger.x * image.shape[1])

                # Map the x-coordinate to servo angle
                servo_angle = int((index_x / image.shape[1]) * 180)

                # Send the servo angle to Arduino via serial communication
                ser.write(bytes(str(servo_angle) + "\n", 'utf-8'))

                # Draw a circle on the index finger tip
                cv2.circle(image, (index_x, int(index_finger.y * image.shape[0])), 8, (0, 255, 0), -1)

        # Show the image with landmarks
        cv2.imshow('Hand Gesture Control', image)

        # Exit the program on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# Release the resources
cap.release()
cv2.destroyAllWindows()
