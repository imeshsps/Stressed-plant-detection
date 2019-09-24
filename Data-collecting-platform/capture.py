#----------------------------------------------
# Library Imports

# Libs for GPIO
import RPi.GPIO as GPIO
import time
# Libs for pycam

from picamera import PiCamera
from time import sleep
# Libs for webcam
import os
import datetime
import sys
import subprocess
#libs for time stamp
#from datetime import datetime, timedelta

import logging

#-----------------------------------------------
#Libs for sensor data collecting and logging
import csv
#import os.path
import os

import sys
import Adafruit_DHT

# Import the ADS1x15 module.
import Adafruit_ADS1x15

import datetime

import time
from w1thermsensor import W1ThermSensor 

# Libraries for I2C Display

import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

#---------------------------------------------
# Initial Configurations

GAIN = 1
pump = 0
growLight_status = 0
global soil_lvl

sensor = W1ThermSensor()

# Create an ADS1115 ADC (16-bit) instance.
adc = Adafruit_ADS1x15.ADS1115()

#get the date and time, set the date and time as a filename.
currentdate = datetime.datetime.now().strftime("%Y-%m-%d_%H%M")
mnAnddt = datetime.datetime.now().strftime("%m-%d")

#log file configuration
logging.basicConfig(filename='/home/pi/Deep_data/Logs/Capture_logs/Log_%s.log' % mnAnddt, filemode='a',format='%(asctime)s - %(message)s', level=logging.INFO)

# Pin Definitions for relay control
growLight = 18
whiteLight = 17
irLED = 27

# Pi camera setup
camera = PiCamera(resolution=(2592, 1944), framerate=30)
# Set ISO to the desired value
camera.iso = 100

# GPIO Setup
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(growLight,GPIO.OUT)
GPIO.setup(whiteLight,GPIO.OUT)
GPIO.setup(irLED,GPIO.OUT)

GPIO.output(growLight,GPIO.HIGH)
GPIO.output(whiteLight,GPIO.HIGH)
GPIO.output(irLED,GPIO.HIGH)

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
draw2.text((x, top), 'Image Capturing..',  font=font2, fill=255)
disp.image(image2)
disp.display()

#--------------------------------------------------------
#Function Definitions

def set_growLight_status_back():
	
	print("Grow Light :%d" % int(growLight_status))
	
	if (int(growLight_status) == 1):
		GPIO.output(growLight,GPIO.LOW)
		print "Grow Light Turned On"
		
	elif (int(growLight_status) == 0):
		GPIO.output(growLight,GPIO.HIGH)
		print "Grow Light Turned off"

def check_growLight_status():
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

def SensorData_Logging_display_update():
	
	
	draw2.text((x, top+30), 'Sensor Data',  font=font, fill=255)
	disp.image(image2)
	disp.display()
	# Create an ADS1115 ADC (16-bit) instance.
	adc = Adafruit_ADS1x15.ADS1115()
	
	adc_value = adc.read_adc(0, gain=GAIN)
	print('ADC :'+str(adc_value))
	
	if adc_value < 8000 :
		soil_lvl = Err
	else :
		soil_lvl = round((-adc_value+23000)/(13000.00)*100.0,2)
	
	draw2.text((x, top+40), 'Soil',  font=font, fill=255)
	disp.image(image2)
	disp.display()
	
	temperature = sensor.get_temperature()
	draw2.text((x+40, top+40), 'Temp',  font=font, fill=255)
	disp.image(image2)
	disp.display()
	
	humidity, temperature2 = Adafruit_DHT.read_retry(11, 22)
	if humidity>100 :
		humidity, temperature2 = Adafruit_DHT.read_retry(11, 22)
	
	temperature = sensor.get_temperature()
	draw2.text((x+80, top+40), 'Hum',  font=font, fill=255)
	disp.image(image2)
	disp.display()
	
	currentdate = datetime.datetime.now().strftime("%Y-%m-%d_%H%M")
	mnAnddt = datetime.datetime.now().strftime("%m-%d")
	hrAndmnt = datetime.datetime.now().strftime("%H-%M")
	
	mnAnddt_dis = datetime.datetime.now().strftime("%m/%d")
	hrAndmnt_dis = datetime.datetime.now().strftime("%I:%M%p")
	
	draw2.text((x, top+50), 'Done..',  font=font, fill=255)
	disp.image(image2)
	disp.display()
	sleep(2)
	
	#if (os.path.exists('/home/pi/Deep_data/csv_files/%s' % (mnAnddt)) == False ):
	#    os.mkdir('/home/pi/Deep_data/csv_files/%s' % mnAnddt)
	
	isFileAvailable = os.path.isfile('/home/pi/Deep_data/csv_files/dataFile_%s.csv' % (mnAnddt))
	
	with open('/home/pi/Deep_data/csv_files/dataFile_%s.csv' % (mnAnddt), mode='a') as csv_file:
	    fieldnames = ['Time_stamp','Temperature', 'Humidity', 'Soil_Mosture']
	    
	    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
	
	    if (isFileAvailable == False):
	     writer.writeheader()
	    
	    writer.writerow({'Time_stamp': currentdate,'Temperature': temperature, 'Humidity': humidity, 'Soil_Mosture': soil_lvl})
	    print('Entry added at %s' % currentdate)
	    logging.info('CSV entry added')
	
	# Write to Display
	disp.clear()
	draw.text((x, top),    'Upt:'+mnAnddt_dis+' '+hrAndmnt_dis,  font=font, fill=255)
	draw.text((x, top+10), 'Tempture:'+str(temperature)+' C', font=font, fill=255)
	draw.text((x, top+20),  'Humidity:'+str(humidity)+' %',  font=font, fill=255)
	draw.text((x, top+30), 'S.Mosture:'+str(soil_lvl)+' %', font=font, fill=255)
	
	
	# with open('/home/pi/Deep_data/pump_status.csv', mode='r') as csv_file:
	    # csv_reader = csv.DictReader(csv_file)
	    # line_count = 0
	    # for row in csv_reader:
	        # if line_count == 0:
	            # #print(f'Column names are {", ".join(row)}')
	            # line_count += 1
	        # pump = str(row["pump"])
	        # line_count += 1	
	
	
	
	with open('/home/pi/Deep_data/waterLvl_status.csv', mode='r') as csv_file:
	    csv_reader = csv.DictReader(csv_file)
	    line_count = 0
	    for row in csv_reader:
	        if line_count == 0:
	            #print(f'Column names are {", ".join(row)}')
	            line_count += 1
	        draw.text((x, top+40), 'Watr lvl:'+ str(row["waterLvl"]+' %'),  font=font, fill=255)
	        line_count += 1	
	draw.text((x, top+50), 'Grow Light:'+str(growLight_status), font=font, fill=255)
	
	# with open('/home/pi/Deep_data/bulbs_status.csv', mode='r') as csv_file:
	    # csv_reader = csv.DictReader(csv_file)
	    # line_count = 0
	    # for row in csv_reader:
	        # if line_count == 0:
	            # #print(f'Column names are {", ".join(row)}')
	            # line_count += 1
	        
	        # line_count += 1	
	
	# Display image.
	disp.image(image)
	disp.display()
	print('Display Updated')
	logging.info('Display Updated')
	
def NoIR_Capture():
	
	GPIO.output(irLED,GPIO.LOW)
	print "ir LED on"
	time.sleep(2)
	#webcam capture

	# read the absolute path
	script_dir = os.path.dirname(__file__)
	# call the .sh to capture the image
	os.system('./webcam.sh')
	#get the date and time, set the date and time as a filename.
	currentdate = datetime.datetime.now().strftime("%Y-%m-%d_%H%M")
	# create the real path
	rel_path = currentdate +".jpg"
	#  join the absolute path and created file name
	abs_file_path = os.path.join(script_dir, rel_path)
	print abs_file_path

	GPIO.output(irLED,GPIO.HIGH)
	print "ir LED off"
	logging.info('IR Captured')
	draw2.text((x, top+10), 'IR image captured',  font=font, fill=255)
	disp.image(image2)
	disp.display()

def RGB_Capture():
	GPIO.output(whiteLight,GPIO.LOW)
	print "white Light on"
	time.sleep(2)

	# Now fix the values
	camera.shutter_speed = camera.exposure_speed
	camera.exposure_mode = 'off'
	camera.brightness = 60
	camera.saturation = 0
	g = camera.awb_gains
	camera.awb_mode = 'off'
	camera.awb_gains = g
	# Finally, take photo with the fixed settings

	camera.capture('/home/pi/Deep_data/rgb/image_%s.jpg' % currentdate)
	print('Captured image_%s.jpg' % currentdate)
	logging.info('RGB Captured')
	draw2.text((x, top+20), 'RGB image captured',  font=font, fill=255)
	disp.image(image2)
	disp.display()
	GPIO.output(whiteLight,GPIO.HIGH)
	print "white Light off"
	
#--------------------------------------------------------
# Calling Functions

check_growLight_status()
NoIR_Capture()
RGB_Capture()
SensorData_Logging_display_update()
set_growLight_status_back()
