
HandTracker Project

Overview

The HandTracker project is a Python-based application that utilizes OpenCV and MediaPipe to detect and track hand movements through a webcam. It calculates distances between specific hand landmarks (e.g., thumb and index finger) and can control screen brightness or volume based on hand gestures.

Features

Real-time hand detection and tracking using a webcam.
Calculation of the distance between specified hand landmarks.
Control of screen brightness and system volume using hand gestures.
Displays the frames with detected landmarks and FPS for real-time feedback.

Requirements

Python 3.x
OpenCV
MediaPipe
numpy
osascript (for macOS volume control)
brightness command-line tool for macOS brightness control

Installation

Clone the repository:
git clone https://github.com/yourusername/handtracker.git
cd handtracker

Install required Python packages:
pip install -r requirements.txt

Install the brightness package:
It was found that installing the brightness package with Homebrew resulted in a display bug where the brightness scalar could not be accessed. This was fixed by building from source.

git clone https://github.com/nriley/brightness.git
cd brightness
make
sudo make install
Usage
Run the main script:

Usage

Run the main script:
python main.py -c [b|v]
-c b: Control screen brightness.
-c v: Control system volume.
Follow the on-screen instructions to perform the calibration and control operations.

Project Structure

src/module/Handtracker.py: Contains the Handtracker class for hand detection and tracking.
tests/bright_test.py: Functions for getting and setting screen brightness using the brightness command-line tool.
tests/volume_test.py: Functions for getting and setting system volume.
main.py: Main script to run the hand tracking and control functionality.