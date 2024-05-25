import osascript


# Function to set the system volume
def set_volume(value: float) -> None:
    """
    Set the system volume.

    Args:
    value (float): Volume level between 0.0 and 1.0.
    """
    value = int(value * 100)  # Convert to integer percentage
    try:
        if 0 <= value <= 100:  # Ensure value is within valid range
            osascript.osascript(f"set volume output volume {value}")
    except Exception as e:
        print("Error:", e)

# Function to get the current system volume
def get_volume() -> int:
    """
    Get the current system volume.

    Returns:
    int: Current volume level as a percentage.
    """
    result = osascript.osascript('get volume settings')
    volInfo = result[1].split(',')  # Split the volume settings string
    outputVol = int(volInfo[0].replace('output volume:', ''))  # Extract output volume
    return outputVol

# volume settings info
# (0, 'output volume:50, input volume:58, alert volume:100, output muted:false', '')
    

if __name__ == "__main__":
    print(f'current Volume: {get_volume()}')
    new_vol = int(input("Enter new volume (0.0-1.0): "))
    if 0.0 <= new_vol <= 1.0:
        vol = int(new_vol*100)
        set_volume(vol)
        print("Volume set to:", vol)
    else:
        print("Invalid brightness value. Please enter a value between 0.0 and 1.0.")