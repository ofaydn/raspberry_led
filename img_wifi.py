
import time
import board
import busio
import digitalio

from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306

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


# Define the Reset Pin
oled_reset = digitalio.DigitalInOut(board.D4)

# Display Parameters
WIDTH = 128
HEIGHT = 64
BORDER = 5

# Display Refresh
LOOPTIME = 1.0

# Use for I2C.
i2c = board.I2C()
oled = adafruit_ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c, addr=0x3C, reset=oled_reset)

# Clear display.
oled.fill(0)
oled.show()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
image = Image.new("1", (oled.width, oled.height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a white background
draw.rectangle((0, 0, oled.width, oled.height), outline=255, fill=255)

font = ImageFont.truetype('PixelOperator.ttf', 16)
#font = ImageFont.load_default()

#intro


while True:
    signal_category = get_signal_strength_category()

# Display the appropriate image based on signal strength
    if signal_category == 0:
    	image = Image.open('imgs/wifi0.ppm').convert('1')
    elif signal_category == 1:
    	image = Image.open('imgs/wifi1.ppm').convert('1')
    elif signal_category == 2:
    	image = Image.open('imgs/wifi2.ppm').convert('1')
    elif signal_category == 3:
    	image = Image.open('imgs/wifi3.ppm').convert('1')
    elif signal_category == 4:
    	image = Image.open('imgs/wifi4.ppm').convert('1')
    elif signal_category == 5:
    	image = Image.open('imgs/wifi5.ppm').convert('1')
    oled.image(image)
    oled.show()
    time.sleep(LOOPTIME)
