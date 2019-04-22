import RPi.GPIO as GPIO
import time
import Adafruit_DHT


##################
#
# I/O Set-up
#
#

GPIO.setmode(GPIO.BOARD)


##################
#
# Function definitions
#
#



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



##################
#
# Start Main programme
#
#
validtempreading, temperature, humidity = ReadTempSensor()
print temperature
print humidity

