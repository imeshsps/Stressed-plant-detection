import RPi.GPIO as GPIO
import time

import csv
import datetime

import logging

#----------------------------------------------
# Libraries for I2C Display

import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

#----------------------------------------------
# Display Initial Configs---

# Raspberry Pi pin configuration:
RST = 24
# Note the following are only used with SPI:
DC = 23
SPI_PORT = 0
SPI_DEVICE = 0

# Note you can change the I2C address by passing an i2c_address parameter like:
disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST, i2c_address=0x3C)

# Initialize library.
disp.begin()


# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = disp.width
height = disp.height
image = Image.new('1', (width, height))
image2 = Image.new('1', (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)
draw2 = ImageDraw.Draw(image2)

# First define some constants to allow easy resizing of shapes.
padding = 2
shape_width = 20
top = padding
bottom = height-padding
# Move left to right keeping track of the current x position for drawing shapes.
x = padding

# Load default font.
#font = ImageFont.load_default()

# Alternatively load a TTF font.  Make sure the .ttf font file is in the same directory as the python script!
# Some other nice fonts to try: http://www.dafont.com/bitmap.php
font = ImageFont.truetype('Apple.ttf', 7)
font2 = ImageFont.truetype('Apple.ttf', 8)

# Clear display.
disp.clear()
#draw2.text((x, top), 'Image Capturing..',  font=font2, fill=255)
draw2.text((x, top), 'Growlight',  font=font2, fill=255)
draw2.text((x, top+10), 'Control Started..',  font=font, fill=255)
disp.image(image2)
disp.display()

#--------------------------------------------------------


currentdate = datetime.datetime.now().strftime("%Y-%m-%d_%H%M")

#log file configuration
logging.basicConfig(filename='/home/pi/Deep_data/Logs/GrowLight_Control_Log.log' , filemode='a',format='%(asctime)s - %(message)s', level=logging.INFO)

growLight = 18

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(growLight,GPIO.OUT)

with open('/home/pi/Deep_data/growLight_status.csv', mode='r') as csv_file:
	    csv_reader = csv.DictReader(csv_file)
	    line_count = 0
	    for row in csv_reader:
	        if line_count == 0:
	            #print(f'Column names are {", ".join(row)}')
	            line_count += 1
            global growLight_status
            growLight_status = str(row["growLight"])
            line_count += 1	

if (int(growLight_status) == 1):
    GPIO.output(growLight,GPIO.HIGH)
    print "growLight off"
    draw2.text((x, top+20), 'Grow Light OFF..',  font=font, fill=255)
    disp.image(image2)
    disp.display()

    with open('/home/pi/Deep_data/growLight_status.csv', mode='w') as csv_file:
        fieldnames = ['timeStamp','growLight']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    
        writer.writeheader()
        writer.writerow({'timeStamp': currentdate,'growLight': '0'})
        
    logging.info('Grow Light turned off')
    
else :
    draw2.text((x, top+20), 'No Action taken',  font=font, fill=255)
    disp.image(image2)
    disp.display()

