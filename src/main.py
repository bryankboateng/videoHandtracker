import cv2
import time
import argparse
import numpy as np
import subprocess
import osascript
from src.utils.control import brightness_control, volume_control
from src.module.Handtracker import Handtracker

def main(control: str) -> None:
    pTime = 0
    cap = cv2.VideoCapture(0)  # Open webcam
    detector = Handtracker()  # Initialize hand tracker
    refTime = time.time()
    distList: list[float] = []  # List to store distances for calibration

    # Calibration phase
    while True:
        _, img = cap.read()  # Capture frame from webcam
        img = detector.findHands(img)  # Detect hands in the frame
        lmList, _ = detector.findPosition(img)  # Get hand landmark positions
        
        if len(lmList) == 0:  # Skip if no hand is detected
            continue
        
        # Calculate distance between thumb and index finger
        distList.append(round(detector.findDistance(4, 8, img, draw=True)[0], 2))
        
        cTime = time.time()
        if (cTime - refTime) >= 10.0:  # Break after 10 seconds of calibration
            break
        
        # Calculate and display FPS
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
        cv2.imshow("Calibration Window", img)
        
        key = cv2.waitKey(1)
        if key == 27:  # Exit on pressing ESC
            break

    cap.release()  # Release webcam
    cv2.destroyAllWindows()

    # Calculate average distance for calibration
    avgLen = round(np.average(np.array(distList)), 2)
    print(avgLen)
    threshold = 0.4 * avgLen  # Set threshold based on average distance

    # Choose control method based on user input
    if control == 'b':
        control_method = brightness_control
    else:
        control_method = volume_control

    pTime = 0
    cap = cv2.VideoCapture(0)  # Reopen webcam for control phase
    while True:
        _, img = cap.read()  # Capture frame from webcam
        img = detector.findHands(img)  # Detect hands in the frame
        lmList, _ = detector.findPosition(img)  # Get hand landmark positions
        
        if len(lmList) == 0:  # Skip if no hand is detected
            continue
        
        # Adjust control based on distance between thumb and index finger
        control_method(detector.findDistance(4, 8, img, draw=True)[0], threshold)
        
        cTime = time.time()
        # Calculate and display FPS
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
        cv2.imshow("Control Window", img)
        
        key = cv2.waitKey(1)
        if key == 27:  # Exit on pressing ESC
            break

    cap.release()  # Release webcam
    cv2.destroyAllWindows()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-c", "--control", help="type of desired control: b for brightness, v for volume", default='', type=str
    )
    args = parser.parse_args()
    if args.control not in ['b', 'v']:  # Validate control input
        print("Control flag must be either b or v!")
    else:
        main(args.control)  # Run main function with specified control type

    




