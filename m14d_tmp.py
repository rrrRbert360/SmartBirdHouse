#!/usr/bin/python
#
# Put your IoT-hands on and Make your own SmartBirdhouse 
# Robert J. Heerekop IOTC360.COM
#
# Please notice that the writer is not an experienced Python programmer.
# Improving, adapting, modifying is highly appreciated!
# Please share your findings and versions and remember that going out there and 
# watching birds in real life is also fun!
#
currentversion = "20190704"
#
#
# This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
#
import time
import httplib
import httplib2
import os
import random
import sys
from picamera import PiCamera
import socket
from apiclient.discovery import build
from apiclient.errors import HttpError
from apiclient.http import MediaFileUpload
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow
import urllib                                               #importing to use its urlencode function
import urllib2                                              #for making http requests
import json                                                 #for decoding a JSON response
from datetime import date
from datetime import datetime
from urllib2 import urlopen, URLError, HTTPError
import logging
import RPi.GPIO as GPIO
import Adafruit_DHT
import paho.mqtt.publish as publish



#####################################################################################################################################################################################
#
# Specific settings for your project are read from the file birdhouseconfig.py
# PLEASE ENSURE to put your own settings in that file!
# YOU MUST PUT YOUR OWN CREDENTIALS INTO THE FILE birdhouseconfig.py BEFORE USING THIS PROGRAMME. Use a text editor.
#


Requiredconfigfileversion = 1                               #this is variable used to verify the format version of the to be imported file birdhouseconfig.py
import birdhouseconfig


print "birdhouseconfig.projectnamestr = " + birdhouseconfig.projectnamestr
print "sw = " + currentversion
print "birdhouseconfig.API_KEY = " + birdhouseconfig.API_KEY
print "birdhouseconfig.ChannelIdentifier = " + birdhouseconfig.ChannelIdentifier
print "birdhouseconfig.MaxNoVideos = " + str(birdhouseconfig.MaxNoVideos)
print "birdhouseconfig.MTBRecordings = " + str(birdhouseconfig.MTBRecordings)
print "birdhouseconfig.EarliestHour = " + str(birdhouseconfig.EarliestHour)
print "birdhouseconfig.LatestHour = " + str(birdhouseconfig.LatestHour)
print "birdhouseconfig.MTBHB = " + str(birdhouseconfig.MTBHB)
print " "

# Define temp video file name extension
filenameextstr = '.h264'
filenamestr = 'tmpvid.h264'


#####################################################################################################################################################################################
#
# Default MQTT publish OpenData (only temperature and humidity)
#
mqtturl="test.mosquitto.org"
mqttreportaddress = "aterhzhwlz/" + birdhouseconfig.projectnamestr + "/Report"


#####################################################################################################################################################################################
#
# This function is called upload a video to Youtube.
# The only this function does is that it creates a shell command string (including the required arguments)to fire the external program
# "upload.py" which must be placed in the same directory as this program
# The original version I took to make this work can be found here:https://developers.google.com/youtube/v3/guides/uploading_a_video
#
def Actions_to_upload():
    global projectnamestr
    global filenamestr
    global YT_TagRandomList
    global YT_CatRandomList
    global YT_DescRND_A
    global YT_DescRND_B
    print("Now uploading video...")
    logging.info("%s VideoClip upload procedure starts..." % (time.strftime("%Y-%m%d-%H%M-%S")))
    OS_StringA = 'sudo python upload.py --file="tmpvid.mp4" --title="'
    OS_StringB = random.choice(birdhouseconfig.YT_DescRND_A) + " " + random.choice(birdhouseconfig.YT_DescRND_B)
    OS_StringC = '" --description="'
    OS_StringD = random.choice(birdhouseconfig.YT_DescRND_A) + " " + random.choice(birdhouseconfig.YT_DescRND_B)
    OS_StringE = '" --keywords="'
    OS_StringF = random.choice(birdhouseconfig.YT_TagRandomList) + ',' + random.choice(birdhouseconfig.YT_TagRandomList) + ',' + random.choice(birdhouseconfig.YT_TagRandomList)
    OS_StringG = '" --category="'
    OS_StringH = str(random.choice(birdhouseconfig.YT_CatRandomList))
    OS_StringI = '" --privacyStatus="public" --noauth_local_webserver'
    if (birdhouseconfig.ChannelPublishing == "private"): OS_StringI = '" --privacyStatus="private" --noauth_local_webserver'
    if (birdhouseconfig.ChannelPublishing == "unlisted"): OS_StringI = '" --privacyStatus="unlisted" --noauth_local_webserver'
    OS_String = OS_StringA + OS_StringB + OS_StringC + OS_StringD + OS_StringE + OS_StringF + OS_StringG + OS_StringH + OS_StringI
    print("The following shell command string has been generated:")
    print(OS_String)
    if TestInternetConnection('https://www.youtube.com/') == 1 :
        print("%s Internet connection tested and OK, now executing generated shell command..." % (time.strftime("%Y-%m%d-%H%M-%S")))
        os.system (OS_String)
    else :
      print("%s Internet connection test FAILED" % (time.strftime("%Y-%m%d-%H%M-%S")))
      logging.info("%s Internet connection test FAILED, upload wil not be performed." % (time.strftime("%Y-%m%d-%H%M-%S")))
    print("Video upload procedure ended and temp file will be deleted.")
    logging.info("%s Video upload procedure ended" % (time.strftime("%Y-%m%d-%H%M-%S")))
    os.system ('rm tmpvid.mp4')



#####################################################################################################################################################################################
#
# This function is called to delete a specific Youtube clip
# The only this function does is that it creates a shell command string (including the required arguments) to fire the external program
# "python delete_video.py" which must be placed in the same directory as this program
# The original version I took to make this work can be found here: https://stackoverflow.com/questions/33646280/deleting-a-video-from-youtube-youtube-data-api-v3-and-python
#
def Actions_to_delete(ID_Refer):
    global projectnamestr
    print("Now starting up program to delete video..." + ID_Refer)
    OS_StringA = 'python delete_video.py --id='
    OS_StringB = ' --noauth_local_webserver'
    OS_String = OS_StringA + ID_Refer
    print(OS_String)
    if TestInternetConnection('https://www.youtube.com/') == 1 :
        print("%s Internet connection tested and OK" % (time.strftime("%Y-%m%d-%H%M-%S")))
        os.system (OS_String)
    else :
      print("%s Internet connection test FAILED" % (time.strftime("%Y-%m%d-%H%M-%S")))
      logging.info("%s Internet connection test FAILED, delete of youtube therefore not performed." % (time.strftime("%Y-%m%d-%H%M-%S")))
      print("Video delete ended")
    logging.info("%s Video delete ended" % (time.strftime("%Y-%m%d-%H%M-%S")))
    print("Now back in main program.")


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
# This function is used to test if there is an internet connection
#
def TestInternetConnection(url):
    try:
        response = urlopen(url)
    except HTTPError, e:
        InternetStatus = 0
    except URLError, e:
        InternetStatus = 0
    else:
        html = response.read()
        InternetStatus = 1
    return InternetStatus


#####################################################################################################################################################################################
#
# MakeVideoClip
#
def MakeVideoClip():
    global projectnamestr
    global temperature
    global humidity
    global AllowedUploads
    global OnScreenName
    global OnScreenDateTime
    global OnScreenTempHum
    global OnScreenDebug
    print("Recording...")
    texttoshowA = ''
    texttoshowB = ''
    texttoshowC = ''
    texttoshowD = ''
    if (birdhouseconfig.OnScreenName == "yes"): texttoshowA = birdhouseconfig.projectnamestr + ' '
    if (birdhouseconfig.OnScreenDateTime == "yes"): texttoshowB = time.strftime("%d-%m-%Y %H:%M") + ' '
    if (birdhouseconfig.OnScreenTempHum == "yes"):
        texttoshowC = 'temp.:' + str(temperature)+ 'C hum.:' + str(humidity) + '% '
        if (humidity == 999): texttoshowC = ''
    if (birdhouseconfig.OnScreenDebug == "yes"): texttoshowD = 'Triggers:' + str(trueTriggers) + ' Uploads:' + str(AllowedUploads) + ' sw:' + currentversion
    camera.annotate_text = texttoshowA + texttoshowB + texttoshowC +texttoshowD
    print(camera.annotate_text)
    camera.start_recording('/home/pi/bin/tmpvid.h264')
    camera.wait_recording(1)
    time.sleep(birdhouseconfig.RecordingDuration)
    camera.stop_recording()
    logging.info("%s VideoClip Recorded with text:" % (time.strftime("%Y-%m%d-%H%M-%S")) + " " + camera.annotate_text)
    print("Rec done. Now convertring to mp4")
    os.system ('MP4Box -add tmpvid.h264 tmpvid.mp4')
    os.system ('rm tmpvid.h264')
    print("Conversion to mp4 done.")




#####################################################################################################################################################################################
#
# CheckAllowedtoRecordClip
#
def CheckAllowedtoRecordClip():
    global LastRecording
    global MTBRecordings
    global AllowedUploads
    elapsedRECi = time.time() - LastRecording
    print(elapsedRECi)
    if (elapsedRECi > birdhouseconfig.MTBRecordings):
        print("Allowed to record, enough time elapsed since last recording.")
        logging.info("%s Allowed to record, enough time elapsed since last recording." % (time.strftime("%Y-%m%d-%H%M-%S")))
        AllowedUploads = AllowedUploads + 1
        MakeVideoClip()
        Actions_to_upload()
        LastRecording = time.time()
    else:
        print("No recording, not enough time elapsed since last recording.")
        logging.info("%s NOT ALLOWED enough time elapsed since last recording." % (time.strftime("%Y-%m%d-%H%M-%S")))


#####################################################################################################################################################################################
#
# This function is turn the infrared(IR) light break sensor on or off.
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
    global temperature
    global humidity
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
            RequiredLoops = birdhouseconfig.MinSensorloops;
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
    global PublicURL
    global currentversion
    global AllowedUploads
    elapsedHBi = time.time() - LastHeartBeat
    if (elapsedHBi > birdhouseconfig.MTBHB):
        print("MQTT HeartBeat coming up, pse wait...")
        validtempreading, temperature, humidity = ReadTempSensor()
        if validtempreading == 1 :
            print("MQTT Reporting")
            print(("%s Log heart beat:" % (time.strftime("%Y-%m%d-%H%M-%S")) + " trueTriggers=" + " Temperature:" + str(temperature) + " Humidity:" + str(humidity)))
            logging.info("%s Log heart beat:" % (time.strftime("%Y-%m%d-%H%M-%S")) + " trueTriggers=" + str(trueTriggers) + " Temperature:" + str(temperature) + " Humidity:" + str(humidity) )
            texttosendA = '{' + '"hid":"' + birdhouseconfig.projectnamestr + '"'
            texttosendB = ', "time":"' + time.strftime("%Y-%m-%dT%H:%M:%S") + '"'
            texttosendC = ', "temp":' + str(temperature)+ ', "hum":' + str(humidity)
            texttosendD = ', "trueTriggers":' + str(trueTriggers) + ', "AllowedUploads":' + str(AllowedUploads)
            texttosendE = ', "url":"' + birdhouseconfig.PublicURL
            texttosendF = '", "switch":' + str(SwitchState) + ', "sw":"' + currentversion + '"}'
        else:
            validtempreading = 0
            print("MQTT Reporting")
            print(("%s Log heart beat:" % (time.strftime("%Y-%m%d-%H%M-%S")) + " trueTriggers=" + str(trueTriggers) + " ERROR Temperature/Humidity sensor"))
            logging.info("%s Log heart beat:" % (time.strftime("%Y-%m%d-%H%M-%S")) + " trueTriggers=" + str(trueTriggers) + " ERROR Temperature/Humidity sensor" )
            texttosendA = '{' + '"hid":"' + birdhouseconfig.projectnamestr + '"'
            texttosendB = ', "time":"' + time.strftime("%Y-%m-%dT%H:%M:%S") + '"'
            texttosendC = ''
            texttosendD = ', "trueTriggers":' + str(trueTriggers) + ', "AllowedUploads":' + str(AllowedUploads)
            texttosendE = ', "url":"' + birdhouseconfig.PublicURL
            texttosendF = '", "switch":' + str(SwitchState) + ', "sw":"' + currentversion + '"}'
        texttosend = texttosendA + texttosendB + texttosendC + texttosendD + texttosendE + texttosendF
        MQTTshareOpenData(mqttreportaddress, texttosend, hostname=mqtturl)
        LastHeartBeat = time.time()
        print(texttosendD)
        print("HeartBeat done.")



#####################################################################################################################################################################################
#
# This function is used for Youtube channel housekeeping.
# When there are too many uploaded video's they will be ranked and old ones which are not viewed, liked or commented are deleted.
#
def YoutubeHousekeeping():
    global ChannelIdentifier
    global API_KEY
    global MaxNoVideos
    VideoList = [
    #------------   VideoID    VideoAge    Stats StatsCorrected --
              ]
    print("%s * * * START HOUSEKEEPING * * * started YoutubeHousekeeping()" % (time.strftime("%Y-%m%d-%H%M-%S")))
    logging.info("%s * * * START HOUSEKEEPING * * * started YoutubeHousekeeping()" % (time.strftime("%Y-%m%d-%H%M-%S")))
    try:
        url = 'https://www.googleapis.com/youtube/v3/search?part=snippet&channelId='+birdhouseconfig.ChannelIdentifier+'&maxResults=50&type=video&key='+birdhouseconfig.API_KEY
        response = urllib2.urlopen(url)
        videos = json.load(response)
        videoMetadata = []
        NumberOfVideos = 0
        for video in videos['items']:
          if video['id']['kind'] == 'youtube#video':
              videoMetadata.append(video['id']['videoId'])
              NumberOfVideos = NumberOfVideos + 1
        print "\nActual number of read public videos in youtube channel:" + str(NumberOfVideos) + "Now going to read Youtube API and retrieve detailed data all public videos in the youtube channel...\nThis can take some time...hold on...\n\n"
        logging.info("%s I have read the number of videos in the youtube channel, which is:" % (time.strftime("%Y-%m%d-%H%M-%S")))
        logging.info(str(NumberOfVideos))

    # In this second part, a loop will run through the listvideoMetadata. During each step the details a specific video are retrieved and stored in the same list.
        VideoPointer = 0
        TotalFeedbackStats = 0
        for metadata in videoMetadata:
          SpecificVideoID = metadata
          SpecificVideoUrl = 'https://www.googleapis.com/youtube/v3/videos?part=snippet%2CcontentDetails%2Cstatistics&id='+SpecificVideoID+'&key='+birdhouseconfig.API_KEY
          response = urllib2.urlopen(SpecificVideoUrl)      #makes the call to a specific YouTube
          videos = json.load(response)                      #decodes the response so we can work with it
          videoMetadata = []                                #declaring our list
          for video in videos['items']:
            if video['kind'] == 'youtube#video':
                SpecificDateLong = video['snippet']['publishedAt']
                UploadYearStr,UploadMonthStr,UploadDayRaw = SpecificDateLong.split("-")
                UploadDayStr,UploadTimeRaw = UploadDayRaw.split("T")      # The Day and Time still need to be splitted in day and time e.g. 13T09:43:26.000Z
                UploadHrStr,UploadMinStr,UploadSecRaw = UploadTimeRaw.split(":")
                UploadSecStr = UploadSecRaw[:-5]
                UploadYear = int(UploadYearStr)
                UploadMonth = int(UploadMonthStr)
                UploadDay = int(UploadDayStr)
                UploadHr = int(UploadHrStr)
                UploadMin = int(UploadMinStr)
                UploadSec = int(UploadSecStr)
                VideoAge_in_s = int((datetime.now() - datetime(UploadYear, UploadMonth, UploadDay, UploadHr, UploadMin, UploadSec)).total_seconds())
                FeedBackStats = int(video['statistics']['viewCount']) + int(video['statistics']['likeCount']) - int(video['statistics']['dislikeCount']) + int(video['statistics']['favoriteCount']) + int(video['statistics']['commentCount'])
                if FeedBackStats<=0 : FeedBackStats = 0
                TotalFeedbackStats = TotalFeedbackStats + FeedBackStats
                print "ListIndex:" + str(VideoPointer) + " YoutubeID:" + metadata + " Video age in sec:" + str(VideoAge_in_s) + " Total stats:" + str(FeedBackStats)
                VideoList.append([metadata, VideoAge_in_s, FeedBackStats, 0])
                VideoPointer = VideoPointer + 1
        NumberOfVideos = VideoPointer
        AverageFeedbackStats = int(TotalFeedbackStats / VideoPointer)
        print "Number of public videos:" + str(NumberOfVideos) + " TotalFeedbackStats:" + str(TotalFeedbackStats) + " AverageFeedback:" + str(AverageFeedbackStats)
        print "\nlen(VideoList):" + str(len(VideoList))
        if NumberOfVideos>birdhouseconfig.MaxNoVideos :      # if length of list is too long, then delete least interesting videos
           print "\nI will reorder the list of video's based on Age. newest up, oldest down."
           logging.info("%s I will reorder the list of video's based on Age. newest up, oldest down." % (time.strftime("%Y-%m%d-%H%M-%S")))
           for n in range(0, len(VideoList)):                #Correct the statistics
             CorrectedVideoStats = VideoList[n][2] - AverageFeedbackStats
             if CorrectedVideoStats<0 : CorrectedVideoStats = 0
             VideoList[n][3] = CorrectedVideoStats           # Store the corrected video stats in list
           VideoList.sort(key=lambda x: x[1])                # The list of video's will be re-ordered based on Age. newest up, oldest down.
           print "VideoList lenghts:   " + str(len(VideoList))
           for n in range(0, len(VideoList)):                #Print the video list
             print str(n) + ":" + str(VideoList[n][0]) + " " + " " + str(VideoList[n][1]) + " " + str(VideoList[n][2]) + " " + str(VideoList[n][3])
           NumberOfVideosToDelete = NumberOfVideos - birdhouseconfig.MaxNoVideos
           NumberOfVideosActuallyDeleted = 0
           for x in range(len(VideoList)-1, -1, -1):
            if (VideoList[x][3] == 0 ) and (NumberOfVideosActuallyDeleted != NumberOfVideosToDelete) :
              print "To limit number of videos in youtube channel I will delete the most uninteresting video: " + VideoList[x][0]
              ID_Refer = VideoList[x][0]                     # delete the oldest and most uninteresting video
              Actions_to_delete(ID_Refer)
              VideoList.pop(x)                               # delete the list entry related to the oldest and most uninteresting video
              NumberOfVideosActuallyDeleted = NumberOfVideosActuallyDeleted + 1
              if NumberOfVideosActuallyDeleted == NumberOfVideosToDelete : break
        else:
          print "Not too many video's. I won't delete any."
          logging.info("%s Not too many video's. I won't delete any." % (time.strftime("%Y-%m%d-%H%M-%S")))
    except:
        print("Something went wrong during housekeeping")

    print("%s * * * END OF  HOUSEKEEPING * * * end of YoutubeHousekeeping()" % (time.strftime("%Y-%m%d-%H%M-%S")))
    logging.info("%s * * * END OF HOUSEKEEPING * * *" % (time.strftime("%Y-%m%d-%H%M-%S")))



#####################################################################################################################################################################################
#
# Setup Camera
#
#
camera = PiCamera()
camera.resolution = (birdhouseconfig.CameraResolutionX, birdhouseconfig.CameraResolutionY)
camera.rotation = birdhouseconfig.CameraRotation
camera.framerate = birdhouseconfig.CameraFramerate
camera.brightness = birdhouseconfig.CameraBrightness
camera.contrast = birdhouseconfig.CameraContrast


#####################################################################################################################################################################################
#
# Set GPIO outputs to power leds and sensor
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
# Power on sensor
#
SwitchSensor("off")                                         #power off sensor emitter (just in case it was on after a reboot)
print("Power on sensor")
logging.info("%s Power on sensor" % (time.strftime("%Y-%m%d-%H%M-%S")) )
SwitchSensor("on")


#####################################################################################################################################################################################
#
# Clean-up after starting-up
#
os.system ('rm tmpvid.*')                                   #clean-up possible tmp files after possible crash
os.system ('rm *.h264')
os.system ('rm *.mp4')


#####################################################################################################################################################################################
#
# Set some variables before we loop
#
LastHeartBeat = time.time() - birdhouseconfig.MTBHB         # ensure immediately report OpenData after booting
LastRecording = time.time() - birdhouseconfig.MTBRecordings # allow recording after booting
IRTrigger = False
ChannelCleaned = 0
trueTriggers = 0
SwitchState = 0
AllowedUploads = 0
humidity = 999
temperature = 999


#####################################################################################################################################################################################
#
# Create and shift logfiles
#
os.system ('mv previous.log preprevious.log')
os.system ('mv current.log previous.log')
formatter = logging.Formatter('%(message)s')
logging.getLogger('').setLevel(logging.DEBUG)
fh = logging.FileHandler('current.log')
fh.setLevel(logging.INFO)
fh.setFormatter(formatter)
logging.getLogger('').addHandler(fh)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
ch.setFormatter(formatter)
logging.getLogger('').addHandler(ch)


#####################################################################################################################################################################################
#
# Run some initialization code before we loop
#
if ((len(birdhouseconfig.projectnamestr) + len(birdhouseconfig.API_KEY) + len (birdhouseconfig.ChannelIdentifier)) == 0):
    print "\n\nSTOP! Before you start this programme you need to enter your projectname and\nYoutube API crentials in the source code merge.py!\nIt should for example look like this:\n\n#######################################################################\n# Your Youtube channel credentials\n#\nprojectnamestr = 'MyBirdHouse'\nbirdhouseconfig.API_KEY = 'AIzaSyBBNzL34L1VPOL4X06DKKBENxI69KHg47sQ'\nbirdhouseconfig.ChannelIdentifier = 'UCD34_H1HWTERF8QWAi4WoEg'\n\n"
    raw_input('Press CTRL+C to quit')

if ( birdhouseconfig.configfileversion != Requiredconfigfileversion):
    print "\n\nSTOP! The version of the file birdhouseconfig.py does not match which the version this program needs and is not compatible!"
    raw_input('Press CTRL+C to quit')

print "This is:" + birdhouseconfig.projectnamestr
logging.info("This is:" + birdhouseconfig.projectnamestr)
logging.info("%s * * * * * * * * * This programme was started * * * * * * * * * " % (time.strftime("%Y-%m%d-%H%M-%S")))


LastSwitchState = GPIO.input(21)
print ("Switch status:", LastSwitchState)
logging.info("%s Switch status:" % (time.strftime("%Y-%m%d-%H%M-%S")) + str(LastSwitchState)  )

if (TestInternetConnection('https://www.youtube.com/')) == 1 :
    print("%s Internet connection tested and OK" % (time.strftime("%Y-%m%d-%H%M-%S")))
    logging.info("%s Internet connection tested and OK" % (time.strftime("%Y-%m%d-%H%M-%S")))
else :
    print("%s Internet connection test FAILED." % (time.strftime("%Y-%m%d-%H%M-%S")))
    logging.info("%s Internet connection test FAILED." % (time.strftime("%Y-%m%d-%H%M-%S")))




#####################################################################################################################################################################################
#
# Main software loop
#
#
MakeVideoClip()        # uncomment to debug
Actions_to_upload()    # uncomment to debug
SheduledReport()       # uncomment to debug
#YoutubeHousekeeping()  # uncomment to debug
while False:           # uncomment to debug
#while True:             # comment to debug(prevent loop)
     Chour = int(time.strftime("%H"))
     if (Chour < birdhouseconfig.LatestHour ) and (Chour > birdhouseconfig.EarliestHour):
         IRTrigger = ReadIRsensor(IRTrigger)
         if (IRTrigger == 0):
             IRTrigger = False
         if (IRTrigger == 1):
             IRTrigger = True
             IRSensorTriggeredNow = 1
         if (IRTrigger == 2):
             IRTrigger = True
             print ("IR_Sensor Triggered!")
             trueTriggers = trueTriggers + 1
             print (trueTriggers)
             CheckAllowedtoRecordClip()
             SheduledReport()                               # Sent message because of event just happened

     SheduledReport()                                       # Sheduled heartbeat interval reporting
                                                            # Sheduled daily VideoChannel Cleaning
     if ((Chour == birdhouseconfig.ChannelCleaningHour ) and (ChannelCleaned == 0) and (birdhouseconfig.YTCleaning == 'yes')):
         ChannelCleaned = 1
         print ("*********** CLEANING *************")
         YoutubeHousekeeping()

