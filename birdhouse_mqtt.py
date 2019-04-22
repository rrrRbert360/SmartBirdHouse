#!/usr/bin/python
#
#
import time
import os
import random
import sys
import picamera
import socket
import urllib #importing to use its urlencode function
import urllib2 #for making http requests
from datetime import date
from datetime import datetime
from urllib2 import urlopen, URLError, HTTPError
import logging
import RPi.GPIO as GPIO
import Adafruit_DHT
import paho.mqtt.publish as publish
import httplib


#####################################################################################################################################################################################
#
# Default settings how to deal with sensor. You can change these, but test new settings for a few days/week and see how it behaves and works.
#
TriggerValidations = 10   # number of validation loops after a sensor trigger
falseTriggers = 0
trueTriggers = 0
SwitchState = 0


#####################################################################################################################################################################################
#
# Default settings. You can change these, but test new settings for a few days/week and see how it behaves and works.
#
EarliestHour = 6                                    # Before this hour during the day no recordings are allowed
LatestHour = 23                                     # After this hour during the day no recordings are allowed

#####################################################################################################################################################################################
#
# Default report interval (MQTT and Log-file) 
#
MTBHB = 10                              # Setting of report interval in seconds/MinTimeBetweenHeartBeats (note 900=15min)


#####################################################################################################################################################################################
#
# Default MQTT publish OpenData (only temperature and humidity)
#
projectnamestr="DEBUG_TEST_MODE"
mqtturl="test.mosquitto.org"
mqttreportaddress = "aterhzhwlz/" + projectnamestr + "/Report"


#####################################################################################################################################################################################
#
# Set GPIO outputs to power leds and sensor
#
#
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(18,GPIO.OUT) # video led light
GPIO.setup(17,GPIO.OUT) # power for sensor emitter
GPIO.setup(27,GPIO.OUT) # power for sensor detector
GPIO.setup(21,GPIO.IN, pull_up_down=GPIO.PUD_UP) # switch-input (other end to GND)

IR_GPIO = 22
GPIO.setup(IR_GPIO,GPIO.IN, pull_up_down=GPIO.PUD_UP)



#####################################################################################################################################################################################
#
# This function is turn the light to record video on or off.
#
def VideoLedTurn(LedAction):
    if LedAction == "off":
        GPIO.output(18,GPIO.LOW)
    if LedAction == "on":
        GPIO.output(18,GPIO.HIGH)


#####################################################################################################################################################################################
#
# This function is turn the IR sensor on or off.
#
def SwitchSensor(SensoreAction):
    if SensoreAction == "off":
        GPIO.output(17,GPIO.LOW)
        GPIO.output(27,GPIO.LOW)
    if SensoreAction == "on":
        GPIO.output(17,GPIO.HIGH)
        GPIO.output(27,GPIO.HIGH)


####################################################################################################################################################################################
#
# Read temperature/humidity sensor
#
#
def ReadTempSensor():
    try :
      humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, 4)
      humidity = round(humidity, 2)
      temperature = round(temperature, 2)
#      humidity = 0
#      temperature = 0
    except :
      validtempreading = 0
    else :
      validtempreading = 1
    return validtempreading, temperature, humidity


#####################################################################################################################################################################################
#
# This function is used to publish OpenData with MQTT
#
def MQTTshareOpenData(mqttreportaddress, texttosend, hostname):
    try:
        publish.single(mqttreportaddress, texttosend, hostname=mqtturl)
        mqqtpuplishok = 1
    except:
        print("%s No connection to MQTT broker" % (time.strftime("%Y-%m%d-%H%M-%S")))
        logging.info("%s No connection to MQTT broker" % (time.strftime("%Y-%m%d-%H%M-%S")))
        mqqtpuplishok = 0
    return mqqtpuplishok







#####################################################################################################################################################################################
#
# Read IR presence sensor
#
#
def ReadIRsensor(Swat):
    global IR_GPIO
    if (Swat == True):
        if ( GPIO.input(IR_GPIO) == 0):
            IRTrigger = 1
        else:
            IRTrigger = 0
    if (Swat == False):
        if ( GPIO.input(IR_GPIO) == 0):
            RequiredLoops = 10;
            StayLoop = True
            counter = 0;
            while (counter < RequiredLoops) and StayLoop:
                counter = counter + 1
                DoubleCheckStatus = GPIO.input(IR_GPIO)
                if (DoubleCheckStatus == 0) and StayLoop:
                    StayLoop = True
                    IRTrigger = 2
                    time.sleep(0.05)
                else:
                    StayLoop = False
                    IRTrigger = 1
        else:
            IRTrigger = 0
    return IRTrigger
            
                        

#####################################################################################################################################################################################
#
# Sheduled heartbeat reporting 
#
#
def SheduledReport():
    global LastHeartBeat
    global MTBHB
    global trueTriggers
    elapsedHBi = time.time() - LastHeartBeat
#    print(elapsedHBi)
    if (elapsedHBi > MTBHB):
        print("HeartBeat...")
        validtempreading, temperature, humidity = ReadTempSensor()
#        validtempreading = 1
#        temperature = 999
#        humidity = 999
        if validtempreading == 1 :
            print("MQTT Reporting")
#                print(("%s Log heart beat:" % (time.strftime("%Y-%m%d-%H%M-%S")) + " trueTriggers=" + str(trueTriggers) + " falseTriggers=" + str(falseTriggers) + " Temperature:" + str(temperature) + " Humidity:" + str(humidity))
#                logging.info("%s Log heart beat:" % (time.strftime("%Y-%m%d-%H%M-%S")) + " trueTriggers=" + str(trueTriggers) + " Temperature:" + str(temperature) + " Humidity:" + str(humidity) )
            texttosendA = '{' + '"hid":"' + projectnamestr + '"'
            texttosendB = ', "time":"' + time.strftime("%Y-%m-%dT%H:%M:%S") + '"'
            texttosendC = ', "temp":' + str(temperature)+ ', "hum":' + str(humidity)
            texttosendD = ', "trueTriggers":' + str(trueTriggers)
            texttosendE = ', "switch":' + str(SwitchState) + '}'
        else:
            validtempreading = 0
            print("MQTT Reporting")
#                print(("%s Log heart beat:" % (time.strftime("%Y-%m%d-%H%M-%S")) + " trueTriggers=" + str(trueTriggers) + " falseTriggers=" + str(falseTriggers) + " ERROR Temperature/Humidity sensor"))
#                logging.info("%s Log heart beat:" % (time.strftime("%Y-%m%d-%H%M-%S")) + " trueTriggers=" + str(trueTriggers) + " ERROR Temperature/Humidity sensor" )
            texttosendA = '{' + '"hid":"' + projectnamestr + '"'
            texttosendB = ', "time":"' + time.strftime("%Y-%m-%dT%H:%M:%S") + '"'
            texttosendC = ''
            texttosendD = ', "trueTriggers":' + str(trueTriggers)
            texttosendE = ', "switch":' + str(SwitchState) + '}'
        texttosend = texttosendA + texttosendB + texttosendC + texttosendD + texttosendE
        MQTTshareOpenData(mqttreportaddress, texttosend, hostname=mqtturl)
        LastHeartBeat = time.time()






#####################################################################################################################################################################################
#
# Power on sensor
#
SwitchSensor("off") #power off sensor emitter (just in case it was on after a reboot)
print("Power on sensor")
logging.info("%s Power on sensor" % (time.strftime("%Y-%m%d-%H%M-%S")) )
SwitchSensor("on")



#####################################################################################################################################################################################
#
# Reset some variables before we loop
#
#
LastSwitchState = GPIO.input(21)
print ("Switch status:", LastSwitchState)
logging.info("%s Switch status:" % (time.strftime("%Y-%m%d-%H%M-%S")) + str(LastSwitchState)  )
LastHeartBeat = time.time()
IRTrigger = False
trueTriggers = 0


#####################################################################################################################################################################################
#
# Main software loop
#
#
while True:
    Chour = int(time.strftime("%H"))
    if (Chour < LatestHour ) & (Chour > EarliestHour):
        IRTrigger = ReadIRsensor(IRTrigger)
        if (IRTrigger == 0):
            IRTrigger = False
        if (IRTrigger == 1):
            IRTrigger = True
            IRSensorTriggeredNow = 1
        if (IRTrigger == 2):
            IRTrigger = True
            print ("IR_Sensor Triggered!")
            trueTriggers = trueTriggers +1
            print (trueTriggers)
    SheduledReport()



