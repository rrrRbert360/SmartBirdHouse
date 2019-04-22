#####################################################################################################################################################################################
#
# Continues test loop 2sec interval switching LEDS high/low
#
import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
#GPIO.setwarnings(False)
GPIO.setup(18,GPIO.OUT) # pin12(gpio18) leds1
GPIO.setup(20,GPIO.OUT) # pin38(gpio20) leds2
GPIO.setup(23,GPIO.OUT) # pin8 (gpio14) leds3
GPIO.setup(24,GPIO.OUT) # pin10(gpio15) leds4

#####################################################################################################################################################################################
#
# Set the signals high/low
#
def GPTurn(Action):
    if Action == "low":
	GPIO.output(18,0)
        GPIO.output(20,0)
	GPIO.output(23,0)
        GPIO.output(24,0)

    if Action == "high":
	GPIO.output(18,1)
        GPIO.output(20,1)
	GPIO.output(23,1)
        GPIO.output(24,1)

while True:
	print "\n\n LEDS1,LEDS2, LEDS3, LEDS4 on\n"
	GPTurn("high")
	time.sleep(2)
	print "LEDS1,LEDS2, LEDS3, LEDS4 off\n"
	GPTurn("low")
	time.sleep(2)
