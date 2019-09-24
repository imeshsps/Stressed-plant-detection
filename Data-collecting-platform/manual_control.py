import RPi.GPIO as GPIO

#-----------
# Pin defs

growLight = 18
pump = 10
whiteLight = 17
irLED = 27

pinNo = 17

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(pinNo,GPIO.OUT)


#GPIO.output(pinNo,GPIO.HIGH) #to turn off
GPIO.output(pinNo,GPIO.LOW) #to turn on
