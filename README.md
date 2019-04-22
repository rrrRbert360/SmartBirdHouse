# SmartBirdHouse RaspberryPI

## Description
Welcome to the Smart DIY Birdbox located in The Hague.
This self-publishing birdbox operates autonomously and self-publishes short video clips to its own youtube channel.

Clips which are not viewed or old are ranked low and automatically deleted by the Birdbox’s algorithm.
If you want to prevent a clip to be deleted, like it or place your comment.

OpenData (temp,humidity,day visits is free available via MQTT Server: test.mosquitto.org Topic: aterhzhwlz/#

This is a DIY volunteer project  of IOTC360 to promote coding to kids and managers.
IoT- and Smart devices are not rocket-science and can be made by everyone who is interested.

Robert Heerekop IOTC360 @rrrRbert360

## Example of autonomous operating SmartBirdHouse 
https://www.youtube.com/channel/UCJmk5jYL5iiKyNsDDG8RZ9w



# INSTALLATION INSTRUCTIONS
SmartBirdhouse Installation and setup V1. 22032019 Robert J. Heerekop
Based on: "Rasberry PI Zero W v1.1" and "NOOBS_v3_0_0"
Expierenced ones Skip Step1

## Step1: PREPARE YOUR RASPBERRY PI
Download with a computer from https://www.raspberrypi.org/downloads/ the NOOBS software as a ZIP-file( version: 'Offline and network install')
Unpack the zip-file on your computer
Prepare an 8GB SD-Card by following the instructions: https://projects.raspberrypi.org/en/projects/raspberry-pi-setting-up/3

Place the SD-CARD, connect a mouse, keyboard, monitor and camera to the RaspberryPI and power on the Raspberry PI.
Select the (upper) suggested installation 'Raspbian FULL' and hit install and get some slow&tasty coffee.
Follow the set-up process and also set-up the WiFi connection to the internet.
Also enter your own country and time zone. This important for the bird monitoring time slot
Yes, take some time to install the offered updates and after the restart continue:

Login the the RasberryPI and:

Hit the Bluetooth icon (in the top menu bar)and “Turn Off Bluetooth”
Hit Raspberry symbol and goto Preferences> RaspberryPI Configuration> Interfaces> 
- enable: Camera, SSH, VNC, Remote GPIO
Confirm the system reboot

## Step2: TEST YOUR CONNECTION
Check: enter the command line (by using LX Terminal offered in the upper task bar) and verify if you can connect to the internet by entering the command:
ping 8.8.8.8
abort the test with CTRL-C

Advised(not mandatory though) is to give your raspberry PI a fixed(also named 'static') IP address on your own LAN.
Hit the WiFi symbol in the taskbar with the right-mouse bottom and change the network settings.


## Step3: PREPARE THE RASPBERRY PI TO RUN THE BIRDHOUSE SOFTWARE 
Install all the required packages by entering the following commands (by using LX Terminal offered in the upper task bar):

sudo pip install paho-mqtt
sudo pip install google-api-python-client
sudo pip install google-auth google-auth-oauthlib google-auth-httplib2
sudo pip install oauth2client
sudo git clone https://github.com/adafruit/Adafruit_Python_DHT.git
cd Adafruit_Python_DHT
sudo python setup.py install
sudo apt-get install gpac
cd ..
mkdir bin
cd bin
PATH=$PATH:/home/pi/bin
Check: Now you will see the prompt "pi@raspberrypi:~/bin $"

Advised is to change the settings file and prevent remote GUI problems. Please enter:
sudo nano /boot/config.txt
The screen editor 'Nano' will start and scroll with the arrow-key down and remove the '#' at the lines:
frame_width=1280
framebuffer_height=720
Exit the text editor with CTRL-X

Restart the Rasberry PI by performing frm the commandline: 
sudo reboot -f



## Step4: PREPARE A GOOGLE ACCOUNT
Its advised not to use your personal google account for this project and set-up a special account for this project.
When somebody steals your birdhouse they can remove the SD-card and extract the associate google account details. 
Choose your own unique project name for your Smartbirdhouse e.g. 'ThereseSmartBirdBox' (please no space or special characters like '!@#$%$%|[^%&*):-';"?! etc.)
Create a new and specific google account for yourself and this project (this name doesn't really matter and can also contain numbers)
Enable for this account the Youtube APIes "Youtube API V3.0" and "Youtune Analytics"
Download the google json credentials file from https://console.developers.google.com (section: login, OAuth 2.0-client-ID's) and rename it "client_secrets.json" and store it on a safe location.
Please also copy and store from this account on a safe location the following details:
API_KEY = 'Replace this with your own youtube api key'                 # Your Youtube API; you can find under https://console.developers.google.com/apis/credentials  Learn here: https://www.youtube.com/watch?v=JbWnRhHfTDA
ChannelIdentifier = 'Replace this with your own Youtube Channel-ID '   # Your Youtube Channel-ID which you can find at https://www.youtube.com/account_advanced  Learn here: https://www.youtube.com/watch?v=tf42K4pPWkM  https://www.youtube.com/account_advanced



## Step5: PREPARE YOUR COMPUTER with TOOLING
You control can control the graphical user interface of your RasberryPI by installing the 'VNC® Viewer' on your computer.
The same VNC® Viewer can be used to transfer files to your RasberryPI.
Please notice that if your computer and RaspberryPI are in the same LAN you don't need to make a VNC online account.
If you want to place the birdhouse at your grandmothers forest and remotely access it, please also create an account.
It is suggested to run this birdhouse in first time on your local LAN otherwise you keep traveling to your grandmother.
Download it from: https://www.realvnc.com/en/connect/download/viewer/
Also download the Putty SSH client on yoru computer from: https://www.putty.org/


## Step6: PERSONALISE YOUR BIRDHOUSE FILE
This readme file comes with a lot of other files.
Enter your on Youtube account details in the upper part of this file: BIRDHOUSECONFIG.PY 
Open the file BIRDHOUSECONFIG.PY and enter the following credentials related to your own account:
projectnamestr = '...'                                                 # Name you want to give to your birdhouse. Use a single name without space or special characters like '!@#$%$%|[^%&*):-';"?! etc.
PublicURL = '...'                                                      # URL you want to refer to in your open data mqtt messages
API_KEY = '...'                                                        # Your Youtube API; you can find under https://console.developers.google.com/apis/credentials  Learn here: https://www.youtube.com/watch?v=JbWnRhHfTDA
ChannelIdentifier = '...'                                              # Your Youtube Channel-ID which you can find at https://www.youtube.com/account_advanced  Learn here: https://www.youtube.com/watch?v=tf42K4pPWkM  https://www.youtube.com/account_advanced



## Step7: INSTALL THE BIRDHOUSE SOFTWARE
If you enter 'ifconfig' in the command line of your RasberryPI you can see thr IP-address.
Start on your computer the VNC® Viewer and enter the IP address of your RasberryPI in the offered box where you need to enter a server IP-address.
If the connection is ok, now the graphical user interface of your Raspberry PI appears.
Right-click the top bar of the VNC-viewer running on your PC and select "Transfer files"
Please copy all the birdhouse files from your computer including the adapted "birdhouseconfig.py" and downloaded "client_secrets.json" to the Rasberry PI.

The files will appear on the Desktop of the RasberryPI. Copy those file with the file manager to directory "/home/pi/bin" in the RaspberryPI.
Check: enter the following command from the command line:
cd bin
ls

The result should be the list:
birdhouseconfig.py          this is the configuration file of your birdhouse which YOU MUST MODIFY with a text editor
birdhouse_leds.py           this is a script file to test the leds (if you want them to have in the first place)
birdhouse_rec.py            this is a script test file to test the camera and record a short video clip
delete_video.py             this is a file which is executed by the main program to delete a video clip from its own youtube channel
m14d.py                     this is the main program
m14d_tmp.py                 this is a single test run version of the main program
Wirering_plan_Rev1.png      this is a wiring plan for the sensor and optional enhancements
yt.sh                       this is test shell script file which tests the upload program
birdhouse_ir.py             this is a script file to test the infrared (entrance) sensor
birdhouse_mqtt.py           this is a script test file to test the working of the MQTT library to sent the OpenData statistics
birdhouse_temp.py           this is a script file to test the temperature/humidity sensor (if you want him to have)
launcher.sh                 this is a shell script file which boots the main program
upload.py                   this is a file which is executed by the main program to upload a video clip to youtube
client_secrets.json         this is a authentication file which you must download from google related to your own birdhouse account  
Wood_cutting_plan_Rev1.png  this is a simple construction plan with important dimensions


Now you have to make the two script files executable by performing the command:
sudo chmod 755 yt.sh
sudo chmod 755 launcher.sh


## Step8: Test the GPIO:
Connect a wire to  GPIO22 (see Wirering_plan_Rev1.png)
start from the command line:
python birdhouse_ir.py
Now you will see fast scrollin lines with '1'
Connect the wire to a ground pin and see if the value turns into '0'
End the test with CTRL-C



## Step9: Test the camera:
start from the command line:
python birdhouse_rec.py
Wait until it is finished and hit the command 'ls' and verify if the file 'tmpvid.h264' has been generated.
Now you have a test video clip in h264 video format.



## Step10: Prepare your Raspberry to Upload video clips
Normally the main program converts the h264 video clip in mp4 format and uploads that to youtube.
With this we prevent speed replay anomalies.
For this test though it is sufficient to upload the previous recorded 'tmpvid.h264' 
WARNING: This step can be frustrating but if you follow these stepds carefully you can manage it.
Don't worry if you fail. You can retry again.
You need to be logged in with your computer to youtube and need to use VNC to remotely access your RaspberryPI.
Warning to the experts: Don't use PUTTY but VNC! 
Ok, there we go:

Use VNC to access the RasberryPI and enter the command line by using LX_terminal.
Enter the commands:
cd bin
yt.sh

A text with hyperlink appears! Now carefully:
Hoover with your mouse over the link and with the right-mouse button copy this URL.
In your own computer (not theRaspbeeryPI) paste this URL in your computer browser and login to the google account of the birdhouse project.
Follow the confirm seqeunce until a code appears which you can copy.

Go back to VNC and select with the left-mouse button the command line terminal.
Paste with your right-mouse the code and you will see a message "Authentication successful."
If you are too slow or make a mistake, down't worry try again by starting yt.sh

If you succeeded you will see a notification that a video with video-ID was uploaded.
Copy this video-id because you also need it in the next step.
If you open your computer's internetbrowser and go to "https://youtu.be/" followed by the id (without colon') you will see the video.
Als if you look in the directory of your RaspberryPI you will see a authentication file.
Ok, when this all worked out we need to be able to delete the file form yourtube.
Go to the next step.
Before you proceed delete the temporariy video clip from the RasberryPI by enterring
rm tmpvid.h264



## Step11: Prepare your Raspberry to delete video clips
When you've done the previous step, this one is easy because it is more or less the same procedure.
Take the video-id from your own birdhouse youtube channel which you want to delete.
Hit the following instruction in the command line and replace HERE_YOUR_VIDEO_ID with the video-id.
python delete_video.py --id=HERE_YOUR_VIDEO_ID --noauth_local_webserver  
Now you can see that the video clip has been deleted from the youtube channel.
So now we have the situation that your Rasberry is allowed to upload and deleted files from its own youtube channel.
Time to launch!


## Step12: Test RUN your application
enter:
sudo python m14d_tmp.py

Watch the software running, take some time and look at your youtube channel
BE PATIENT!

ENJOY!




