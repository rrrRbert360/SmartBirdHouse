import RPi.GPIO as GPIO
import time
import Adafruit_DHT



GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(17,GPIO.OUT) 
GPIO.setup(27,GPIO.OUT) 


#####################################################################################################################################################################################
#
# Set IR on
#
GPIO.output(17,1)
GPIO.output(27,1)

# Initialize IR break detector
#
IR_GPIO = 22
GPIO.setup(IR_GPIO,GPIO.IN, pull_up_down=GPIO.PUD_UP)





while True:
    print GPIO.input(IR_GPIO)

#GPIO.remove_event_detect(22)
#GPIO.add_event_detect(IR_GPIO, GPIO.FALLING)
# do_something()
#if GPIO.event_detected(IR_GPIO):
#    print('Button pressed')
    
