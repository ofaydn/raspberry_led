import subprocess

def get_signal_strength_category():
    # Run the iwconfig command to get Wi-Fi signal strength
    result = subprocess.run(['iwconfig'], capture_output=True, text=True)
    
    # Parse the result to find the signal strength
    for line in result.stdout.split('\n'):
        if 'Signal level' in line:
            signal = line.split('Signal level=')[1].split(' ')[0]
            signal_strength = int(signal)
            
            # Categorize signal strength into 0-5
            if signal_strength >= -50:
                return 5  # Excellent
            elif -60 <= signal_strength < -50:
                return 4  # Good
            elif -70 <= signal_strength < -60:
                return 3  # Fair
            elif -80 <= signal_strength < -70:
                return 2  # Weak
            elif -90 <= signal_strength < -80:
                return 1  # Very weak
            else:
                return 0  # No signal or extremely weak signal

    return 0  # If no signal information found
