# Created by: Michael Klements
# For Raspberry Pi Desktop Case with OLED Stats Display
# Base on Adafruit CircuitPython & SSD1306 Libraries
# Installation & Setup Instructions - https://www.the-diy-life.com/add-an-oled-stats-display-to-raspberry-pi-os-bullseye/
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
FONTSIZE = 15
# Use for I2C.
i2c = board.I2C()
oled = adafruit_ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c, addr=0x3C, reset=oled_reset)

# Clear display.
oled.fill(0)
oled.show()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
#image = Image.new("1", (oled.width, oled.height))
##image = Image.open(return_wifi_img()).convert('1')
# Get drawing object to draw on image.
##draw = ImageDraw.Draw(image)

# Draw a white background
##draw.rectangle((0, 0, oled.width, oled.height), outline=255, fill=255)

font = ImageFont.truetype('/home/raspberry/OLED_Stats/PixelOperator.ttf', FONTSIZE)
#font = ImageFont.load_default()

image = Image.open('imgs/ofaydndev.ppm').convert('1')
draw = ImageDraw.Draw(image)
oled.image(image)
oled.show()
time.sleep(3)


while True:

#    print(return_wifi_img());
#    image = Image.open(img_path).convert(1)
#    image = Image.open(return_wifi_img).convert('1')
    # Draw a black filled box to clear the image.
    image = Image.open(return_wifi_img()).convert('1')
    draw = ImageDraw.Draw(image)
#    draw.rectangle((0, 0, oled.width, oled.height), outline=0, fill=0)
#    image = Image.open('imgs/wifi4.ppm').convert('1')

    oled.show()

    # Shell scripts for system monitoring from here : https://unix.stackexchange.com/questions/119126/command-to-display-memory-usage-disk-usage-and-cpu-load
    cmd = "hostname -I | cut -d\' \' -f1"
    IP = subprocess.check_output(cmd, shell = True )

#    cmd = "top -bn1 | grep load | awk '{printf \"CPU: %.2f\", $(NF-2)}'"
#    cmd = "top -bn1 | grep load | awk '{printf \"CPU: %.0f%%\", $(NF-2) * 25}'"
    cmd = "top -bn1 | grep load | awk '{cpu=$(NF-2)*25; if (cpu < 1) cpu=1; printf \"CPU: %.0f%%\", cpu}'"
    CPU = subprocess.check_output(cmd, shell = True )

#    cmd = "top -bn1 | grep 'Cpu(s)' | awk '{printf \"CPU: %.2f%%\", 100-$8}'"
#    CPU = subprocess.check_output(cmd, shell=True)

#    cmd = "free -m | awk 'NR==2{printf \"RAM: %s/%sM %d%%\", $3,$2,($3*100/$2)+0.5 }'"
    cmd = "free -m | awk 'NR==2{printf \"RAM: %.2f/%.1fG %d%%\", $3/1024,$2/1024,($3*100/$2)+0.5 }'"
    MemUsage = subprocess.check_output(cmd, shell = True )

    cmd = "df -h | awk '$NF==\"/\"{printf \"Disk: %d/%dGB %s\", $3,$2,$5}'"
    Disk = subprocess.check_output(cmd, shell = True )

    cmd = "vcgencmd measure_temp |cut -f 2 -d '='"
#    cmd = 'vcgencmd measure_temp | awk -F"[=]" \'{gsub("\'C", "", $2); printf "%s°C", $2}\''

    Temp = subprocess.check_output(cmd, shell = True )
#    Temp = str(Temp, 'utf-8').replace("'C", "°C")
    Temp = Temp.decode('utf-8').strip().replace("'C", "")  # Remove the 'C
    Temp = str(round(float(Temp))) + "°C"

    cmd = "date +'%H:%M'"
    Time = subprocess.check_output(cmd, shell=True)
    # Pi Stats Display
    draw.text((0, 0), str(IP,'utf-8'), font=font, fill=255)

    draw.text((0, 32), str(CPU, 'utf-8') , font=font, fill=255)

    draw.text((64, 32), Temp , font=font, fill=255)

    draw.text((96,32), str(Time, 'utf-8'),font=font, fill=255)

    draw.text((0, 48), str(MemUsage,'utf-8'), font=font, fill=255)

    draw.text((0, 16), str(Disk,'utf-8'), font=font, fill=255)

    # Display image
    oled.image(image)
    oled.show()
    time.sleep(LOOPTIME)
