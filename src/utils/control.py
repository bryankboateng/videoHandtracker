import subprocess
import osascript
from tests.bright_test import get_brightness, set_brightness
from tests.volume_test import get_volume, set_volume

# Adjusts screen brightness based on given input and threshold
def brightness_control(value, threshold):
    """
    Adjusts the screen brightness based on the detected input value and a threshold.

    Args:
    value (float): The detected input value (e.g., distance between landmarks).
    threshold (float): The threshold value to determine if the brightness should be increased or decreased.
    """
    curr_brightness = get_brightness()
    if value > threshold:
        if curr_brightness <= 0.9:
            set_brightness(curr_brightness + 0.1)
        else:
            set_brightness(1.0)
    else:
        if curr_brightness >= 0.1:
            set_brightness(curr_brightness - 0.1)
        else:
            set_brightness(0.0)

# Adjusts volume based on given input and threshold        
def volume_control(value, threshold):
    """
    Adjusts the system volume based on the detected input value and a threshold.

    Args:
    value (float): The detected input value (e.g., distance between landmarks).
    threshold (float): The threshold value to determine if the volume should be increased or decreased.
    """
    curr_vol = get_volume()
    if value > threshold:
        if curr_vol <= 90:
            curr_vol = float(curr_vol + 10) / 100.0
            set_volume(curr_vol)
        else:
            set_volume(1.0)
    else:
        if curr_vol >= 10:
            curr_vol = float(curr_vol - 10) / 100.0
            set_volume(curr_vol)
        else:
            set_volume(0.0)
