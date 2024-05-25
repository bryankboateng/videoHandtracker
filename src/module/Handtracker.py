import cv2
import mediapipe as mp
import time
import math

class Handtracker():
    def __init__(self) -> None:
        # Initialize MediaPipe hands and drawing utilities
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands()
        self.mpDraw = mp.solutions.drawing_utils
        # List of landmark IDs for fingertips
        self.tipIds = [4, 8, 12, 16, 20]

    def findHands(self, img, draw=True):
        """
        Detects hands in the input image and optionally draws landmarks.

        Args:
        img (np.array): Input image.
        draw (bool): Whether to draw hand landmarks on the image.

        Returns:
        np.array: Image with hand landmarks drawn if draw=True.
        """
        img = cv2.flip(img, 1)  # Flip the image horizontally
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Convert to RGB
        self.results = self.hands.process(imgRGB)  # Process the image to detect hands
        
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    # Draw hand landmarks on the image
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
        return img

    def findPosition(self, img, handNo=0, draw=True):
        """
        Finds the position of hand landmarks and returns the coordinates and bounding box.

        Args:
        img (np.array): Input image.
        handNo (int): Index of the hand to process.
        draw (bool): Whether to draw landmarks and bounding box on the image.

        Returns:
        tuple: List of landmark positions and bounding box.
        """
        xList = []
        yList = []
        bbox = []
        h, w, _ = img.shape  # Image dimensions
        self.lmList = []

        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for idx, lm in enumerate(myHand.landmark):
                # Calculate pixel coordinates of the landmark
                cx, cy = int(lm.x * w), int(lm.y * h)
                xList.append(cx)
                yList.append(cy)
                self.lmList.append([idx, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 5, (255, 0, 255), cv2.FILLED)  # Draw landmark

            # Calculate bounding box
            xmin, xmax = min(xList), max(xList)
            ymin, ymax = min(yList), max(yList)
            bbox = xmin, ymin, xmax, ymax
            if draw:
                cv2.rectangle(img, (bbox[0] - 20, bbox[1] - 20), (bbox[2] + 20, bbox[3] + 20), (0, 255, 0), 2)
        
        return self.lmList, bbox

    def fingersUp(self):
        """
        Determines which fingers are up based on landmark positions.

        Returns:
        list: Binary list indicating which fingers are up.
        """
        fingers = []  # List to store binary status of fingers (1 for up, 0 for down)

        # Check thumb
        if self.lmList[self.tipIds[0]][1] > self.lmList[self.tipIds[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        # Check other four fingers
        for idx in range(1, 5):
            if self.lmList[self.tipIds[idx]][2] < self.lmList[self.tipIds[idx] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
        
        return fingers

    def findDistance(self, p1, p2, img, draw=True):
        """
        Calculates the distance between two hand landmarks.

        Args:
        p1 (int): Index of the first landmark.
        p2 (int): Index of the second landmark.
        img (np.array): Input image.
        draw (bool): Whether to draw the distance on the image.

        Returns:
        tuple: Distance between landmarks, image with drawings, and coordinates of the points.
        """
        x1, y1 = self.lmList[p1][1], self.lmList[p1][2]  # Coordinates of the first point
        x2, y2 = self.lmList[p2][1], self.lmList[p2][2]  # Coordinates of the second point
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2  # Coordinates of the midpoint

        if draw:
            # Draw circles and line connecting the points
            cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), 15, (255, 0, 255), cv2.FILLED)
            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
            cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)

        length = math.hypot(x2 - x1, y2 - y1)  # Calculate Euclidean distance
        return length, img, [x1, y1, x2, y2, cx, cy]
    
def main():
    pTime = 0
    cap = cv2.VideoCapture(0)
    detector = Handtracker()
    while True:
        _, img = cap.read()
        img = detector.findHands(img)
        lmList = detector.findPosition(img)
        if len(lmList) != 0:
            print(lmList[4])
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3,
    (255, 0, 255), 3)
        cv2.imshow("Image", img)
        key = cv2.waitKey(1)
        if key == 27:
            break
            
if __name__ == "__main__":
        main()
    
    

