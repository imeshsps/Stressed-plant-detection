import time
import RPi.GPIO as GPIO

import csv
import datetime

import logging
from time import sleep

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
draw2.text((x, top), 'Water level',  font=font2, fill=255)
draw2.text((x, top+10), 'Measuring Started',  font=font, fill=255)
disp.image(image2)
disp.display()

#--------------------------------------------------------

currentdate = datetime.datetime.now().strftime("%Y-%m-%d_%H%M")

global test_bit
test_bit = 0

#log file configuration

#logger = logging.basicConfig(filename='/home/pi/Deep_data/Logs/Water_lvl_Log.log' , filemode='a',format='%(asctime)s - %(message)s', level=logging.INFO)
#logger2 = logging.basicConfig(filename='/home/pi/Deep_data/Logs/Low_water_level_Log.log' , filemode='a',format='%(asctime)s - %(message)s', level=logging.INFO)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')

# Use BCM GPIO references
# instead of physical pin numbers
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Define GPIO to use on Pi
GPIO_TRIGGER = 23
GPIO_ECHO    = 24
buzzer    = 25


# Set pins as output and input
GPIO.setup(GPIO_TRIGGER,GPIO.OUT)  # Trigger
GPIO.setup(GPIO_ECHO,GPIO.IN)      # Echo
GPIO.setup(buzzer,GPIO.OUT)      # Echo

GPIO.output(buzzer, 0)

def setup_logger(name, log_file, level=logging.INFO):
    """Function setup as many loggers as you want"""

    handler = logging.FileHandler(log_file)        
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger
    
# first file logger
lvl_logger = setup_logger('lvl_logger', '/home/pi/Deep_data/Logs/Water_lvl_Log.log')
#logger.info('This is just info message')

# second file logger
low_lvl_logger = setup_logger('low_lvl_logger', '/home/pi/Deep_data/Logs/Low_water_level_Log.log')
#super_logger.info('This is an error message')

def water_lvl():
	
    # Set trigger to False (Low)
    GPIO.output(GPIO_TRIGGER, False)
	
    #print "Ultrasonic Measurement"

    #Allow module to settle
    time.sleep(0.5)

    # Send 10us pulse to trigger
    GPIO.output(GPIO_TRIGGER, True)
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
    start = time.time()

    while GPIO.input(GPIO_ECHO)==0:
      start = time.time()

    while GPIO.input(GPIO_ECHO)==1:
      stop = time.time()

    # Calculate pulse length
    elapsed = stop-start

    # Distance pulse travelled in that time is time
    # multiplied by the speed of sound (cm/s)
    distancet = elapsed * 34300

    # That was the distance there and back so halve the value
    distance = distancet / 2
    global water_level
    water_level = ((-distance + 39)/20)*100
    #return distance
    if water_level>100 :
        water_level = 100
    elif water_level<0 :
        water_level = 0
    
    if test_bit == 0:
        lvl_logger.info('Water level check finished. level :'+ str(round(water_level,1))+' %')
        draw2.text((x, top+20), 'Water lvl :'+str(round(water_level,1))+' %',  font=font2, fill=255)
        disp.image(image2)
        disp.display()
    
    
    with open('/home/pi/Deep_data/waterLvl_status.csv', mode='w') as csv_file:
        fieldnames = ['timeStamp','waterLvl']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    
        writer.writeheader()
        writer.writerow({'timeStamp': currentdate,'waterLvl': round(water_level,1)})
    
    
    return round(water_level,1)


print "Water level :", water_lvl()



checker = True

if water_level <40:
    
    test_bit = 1
    low_lvl_logger.info('Low Water level Detected. level :'+ str(round(water_level,1))+' %')
    draw2.text((x, top+30), 'Low Water level..',  font=font, fill=255)
    disp.image(image2)
    disp.display()
    

while water_level <40:

      
      GPIO.output(buzzer, checker)
      sleep(1)
      checker = not checker
      print "Distance :", water_lvl()
      

GPIO.output(buzzer, 0)
    
if test_bit == 1:
    
    low_lvl_logger.info('Water refill detected. level :'+ str(round(water_level,1))+' %')
    draw2.text((x, top+40), 'Refill detected',  font=font2, fill=255)
    draw2.text((x, top+50), 'level :'+str(round(water_level,1))+' %',  font=font2, fill=255)
    disp.image(image2)
    disp.display()

#print "Elaspsed time :", elapsed

#print "Total distance :", distancet



# Reset GPIO settings
# GPIO.cleanup()
