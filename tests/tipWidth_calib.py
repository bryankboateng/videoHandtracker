from src.module.Handtracker import Handtracker
import cv2
import time
import numpy as np

def main():
    """
    Main function to capture video from the webcam, detect hand landmarks,
    calculate the distance between thumb and index finger, and compute the average distance.
    """
    pTime = 0  # Previous time for FPS calculation
    cap = cv2.VideoCapture(0)  # Initialize video capture from the default webcam
    detector = Handtracker()  # Initialize the hand tracker
    refTime = time.time()  # Reference time for duration tracking
    distList: list[float] = []  # List to store distances between thumb and index finger

    while True:
        _, img = cap.read()  # Capture a frame from the webcam
        img = detector.findHands(img)  # Detect hands and draw landmarks on the frame
        lmList, _ = detector.findPosition(img)  # Get landmark positions

        if len(lmList) == 0:
            continue  # Skip to the next frame if no landmarks are detected

        # Calculate the distance between the thumb (landmark 4) and index finger (landmark 8)
        distList.append(round(detector.findDistance(4, 8, img, draw=True)[0], 2))
        
        cTime = time.time()  # Current time
        if (cTime - refTime) >= 5.0:
            break  # Exit the loop after 5 seconds

        # Calculate and display FPS on the frame
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
        
        cv2.imshow("Image", img)  # Display the frame
        key = cv2.waitKey(1)  # Wait for 1 ms for a key press
        if key == 27:  # Exit if 'Esc' key is pressed
            break

    # Calculate and print the average distance between thumb and index finger
    avgLen = np.average(np.array(distList))
    print(f"The average length between thumb and index site is {avgLen:.2f}")

if __name__ == "__main__":
    main()  # Run the main function
