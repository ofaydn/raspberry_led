import time
import board
import busio
import digitalio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306
import subprocess
from func_img import return_wifi_img

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
image = Image.new("1", (oled.width, oled.height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a white background
draw.rectangle((0, 0, oled.width, oled.height), outline=255, fill=255)

font = ImageFont.truetype('PixelOperator.ttf', 16)

while True:
    # Get the image path for Wi-Fi signal strength
    img_path = return_wifi_img()

    # Open the Wi-Fi image
    wifi_image = Image.open(img_path).convert('1')

    # Clear the main image by filling it with white
    draw.rectangle((0, 0, oled.width, oled.height), outline=255, fill=255)

    # Paste the Wi-Fi image onto the main image
    image.paste(wifi_image, (0, 0))  # No offset, filling the entire display

    # Get system information
    cmd = "hostname -I | cut -d' ' -f1"
    IP = subprocess.check_output(cmd, shell=True).decode('utf-8').strip()
    
    cmd = "top -bn1 | grep load | awk '{printf \"CPU: %.2f\", $(NF-2)}'"
    CPU = subprocess.check_output(cmd, shell=True).decode('utf-8').strip()
    
    cmd = "free -m | awk 'NR==2{printf \"Mem: %s/%sMB %.2f%%\", $3,$2,$3*100/$2 }'"
    MemUsage = subprocess.check_output(cmd, shell=True).decode('utf-8').strip()
    
    cmd = "df -h | awk '$NF==\"/\"{printf \"Disk: %d/%dGB %s\", $3,$2,$5}'"
    Disk = subprocess.check_output(cmd, shell=True).decode('utf-8').strip()
    
    cmd = "vcgencmd measure_temp | cut -f 2 -d '='"
    Temp = subprocess.check_output(cmd, shell=True).decode('utf-8').strip()
    
    # Display system stats on top of the Wi-Fi image
    draw.text((0, 0), "IP: " + IP, font=font, fill=0)
    draw.text((0, 16), CPU + " LA", font=font, fill=0)
    draw.text((0, 32), MemUsage, font=font, fill=0)
    draw.text((0, 48), Disk, font=font, fill=0)

    # Display the combined image on the OLED
    oled.image(image)
    oled.show()

    # Pause for a specified interval
    time.sleep(LOOPTIME)
