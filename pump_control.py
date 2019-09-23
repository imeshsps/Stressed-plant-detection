import RPi.GPIO as GPIO
import time

import logging

import datetime

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
draw2.text((x, top), 'Pump Control',  font=font2, fill=255)
draw2.text((x, top+10), 'Started..',  font=font, fill=255)
disp.image(image2)
disp.display()

#--------------------------------------------------------

day_int = int(datetime.datetime.now().strftime("%d"))

#log file configuration
logging.basicConfig(filename='/home/pi/Deep_data/Logs/Pump_Control_Log.log' , filemode='a',format='%(asctime)s - %(message)s', level=logging.INFO)

pump = 10

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(pump,GPIO.OUT)

if (day_int%2)==1 :
	
	GPIO.output(pump,GPIO.LOW)
	print "Pump on"
	logging.info('Pump turned On')
	draw2.text((x, top+20), 'Pump Started..',  font=font, fill=255)
	disp.image(image2)
	disp.display()
	time.sleep(4)
	GPIO.output(pump,GPIO.HIGH)
	print "Pump off"
	logging.info('Pump turned Off')
	draw2.text((x, top+30), 'Pump turned OFF',  font=font, fill=255)
	disp.image(image2)
	disp.display()


else :
	
	logging.info('Even day, No watering today')
	draw2.text((x, top+30), 'Even day, No',  font=font, fill=255)
	draw2.text((x, top+40), 'watering today',  font=font, fill=255)
	disp.image(image2)
	disp.display()
    
