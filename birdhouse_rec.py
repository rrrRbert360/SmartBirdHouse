#!/usr/bin/python

from picamera import PiCamera
from time import sleep
import RPi.GPIO as GPIO
import Adafruit_DHT

#####################################################################################################################################################################################
#
# Setup GPIOs
#
GPIO.setmode(GPIO.BCM)
#GPIO.setwarnings(False)
GPIO.setup(18,GPIO.OUT) # pin12(gpio18) leds1
GPIO.setup(20,GPIO.OUT) # pin38(gpio20) leds2
GPIO.setup(23,GPIO.OUT)
GPIO.setup(24,GPIO.OUT)



#####################################################################################################################################################################################
#
# Setup Camera
#
camera = PiCamera()
#camera.resolution = (2592, 1944)
camera.resolution = (1920, 1080)
camera.rotation = 180
camera.framerate = 15
camera.brightness = 95
camera.contrast = 90

#####################################################################################################################################################################################
#
# Function to read temperature and humidity
def ReadTempSensor():
    try :
      humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, 4)
      humidity = round(humidity, 2)
      temperature = round(temperature, 2)
    except :
      validtempreading = 0
    else :
      validtempreading = 1
    return validtempreading, temperature, humidity


#####################################################################################################################################################################################
#
# Function to switch leds on/off
#
def LEDSTurn(Action):
    if Action == "off":
	GPIO.output(18,0)
        GPIO.output(20,0)
	GPIO.output(23,0)
        GPIO.output(24,0)

    if Action == "on":
	GPIO.output(18,1)
        GPIO.output(20,1)
	GPIO.output(23,1)
        GPIO.output(24,1)


print "Recording now..."

#camera.start_preview()
camera.annotate_text = "Hello World!"
camera.start_recording('/home/pi/bin/tmpvid.h264')

#camera.wait_recording(5)
sleep(4)
camera.stop_recording()
#camera.stop_preview()
##

print "Done"
LEDSTurn("off")

#validtempreading, temperature, humidity = ReadTempSensor()
#print temperature
#print humidity
