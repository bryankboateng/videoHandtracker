import subprocess

def set_brightness(value) -> None:
    """
    Sets the screen brightness to the specified value.

    Args:
    value (float): Desired brightness level, typically between 0.0 and 1.0.
    """
    try:
        # Use the 'brightness' command-line tool to set the brightness
        subprocess.call(["brightness", str(value)])
    except Exception as e:
        print("Error:", e)

def get_brightness() -> float:
    """
    Retrieves the current screen brightness level.

    Returns:
    float: Current brightness level as a float between 0.0 and 1.0.
    """
    try:
        # Use the 'brightness' command-line tool with '-l' to list the current brightness level
        output = subprocess.check_output(["brightness", "-l"], universal_newlines=True)
        # Extract the brightness level from the last line of the output
        line = output.strip().split('\n')[-1]
        current_brightness = float(line.split("brightness")[-1].strip())
        return current_brightness
    except Exception as e:
        print("Error:", e)
        return None

    

        
        


if __name__ == "__main__":
    print(f'current Brightness: {get_brightness()}')
    new_brightness = float(input("Enter new brightness (0-1.0): "))
    if 0.0 <= new_brightness <= 1.0:
        set_brightness(new_brightness)
        print("Brightness set to:", new_brightness)
    else:
        print("Invalid brightness value. Please enter a value between 0.0 and 1.0.")





