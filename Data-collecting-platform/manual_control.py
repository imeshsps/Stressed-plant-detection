import RPi.GPIO as GPIO

#-----------
# Pin defs

growLight = 18
pump = 10
whiteLight = 17
irLED = 27

GPIO.setup(growLight,GPIO.OUT)

GPIO.output(growLight,GPIO.HIGH) #to turn off
GPIO.output(growLight,GPIO.LOW) #to turn on
