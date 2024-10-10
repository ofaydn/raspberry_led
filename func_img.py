import subprocess


def get_signal_strength_category():
    # Run the iwconfig command to get Wi-Fi signal strength
    result = subprocess.run(['/usr/sbin/iwconfig'], capture_output=True, text=True)
    
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

def get_wifi_image_path(signal_category):
    # Map signal categories to image file names
    image_map = {
        0: 'imgs/wifi0.ppm',
        1: 'imgs/wifi1.ppm',
        2: 'imgs/wifi2.ppm',
        3: 'imgs/wifi3.ppm',
        4: 'imgs/wifi4.ppm',
        5: 'imgs/wifi5.ppm',
    }
    
    # Return the corresponding image path based on the signal category
    return image_map.get(signal_category, 'imgs/wifi0.ppm')  # Default to wifi0 if not found

# Main execution
def return_wifi_img():
    signal_category = get_signal_strength_category()
    image_path = get_wifi_image_path(signal_category)
    return image_path


