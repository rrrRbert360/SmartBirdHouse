############################################
#
# The variables in this file define the behavior of the birdhouse.
# Please notice that You MUST enter for your birdhouse the specific setting in the First section 
# You can change the other settings as well, but that might result in blocking API or other unforeseen behavior
#
#    This file is part of SmartBirdhouse.
#    SmartBirdhouse is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#    SmartBirdhouse is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#    You should have received a copy of the GNU General Public License
#    along with SmartBirdhouse.  If not, see <https://www.gnu.org/licenses/>.

############################################
#
# YOU MUST ENTER THE SPECIFIC DETAILS/CREDENTIALS OF YOUR OWN SMARTBIRDHOUSE HERE:
#
projectnamestr = 'YourSmartBirdHouseName'                                     # Name you want to give to your birdhouse. Use a single name without space or special characters like '!@#$%$%|[^%&*):-';"?! etc.
PublicURL = 'enter your URL here'                                             # URL you want to refer to in your open data mqtt messages
API_KEY = 'enter your own API key here'                                       # Your Youtube API; you can find under https://console.developers.google.com/apis/credentials  Learn here: https://www.youtube.com/watch?v=JbWnRhHfTDA
ChannelIdentifier = 'enter your own Channel-ID key here'                      # Your Youtube Channel-ID which you can find at https://www.youtube.com/account_advanced  Learn here: https://www.youtube.com/watch?v=tf42K4pPWkM  https://www.youtube.com/account_advanced


############################################
#
# FOR A QUICKSTART, IGNORE EVERYTHING HERE BELOW
# If you want to get your birdhouse working in the first place, please hold your horses DON'T CHANGE any of the values below this text.
# When it works though you can experiment by changing the settings below,
# but please notice that might result in temporarily blocking API, running out of memory or other unforeseen behavior.
# Tip: if you change any of timers and settings; please monitor (after a few days running) the following dashboard page and monitor the traffic and errors: https://console.developers.google.com

# Defines how youtube videos are published values can be: 'public', 'private' or 'unlisted'
ChannelPublishing = 'private'

# Defines under which youtube category identifiers clips are randomly picked and posted
YT_CatRandomList = [15,22,27,28]

# Titles and texts are generated by randomly merging these two sets of text strings [YT_DescRND_A] [YT_DescRND_B]
# You can modify these but please don't use any other characters than plain text! So for example no '!@#$%$%^^%&*):-';"?! etc.
YT_DescRND_A = ['Something is happening','Some movements','I detected something','Some activities detected','Another movement','Is it okay what is happening','Look','What about what is happening']
YT_DescRND_B = ['inside this DIY bird house','inside this bird box','here','inside this Self-Publishing DIY Bird house']


# Defines which tags can be randomly picked for search engine tagging
# You can modify these but please don't use any other characters than plain text! So for example no '!@#$%$%^^%&*):-';"?! etc.
YT_TagRandomList = ['','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','']
YT_TagRandomList[0] = 'nestkast'
YT_TagRandomList[1] = 'vogelhuis'
YT_TagRandomList[2] = 'nestkasje'
YT_TagRandomList[3] = 'vogelhuisje'
YT_TagRandomList[4] = 'nestelen'
YT_TagRandomList[5] = 'vogelvriendelijke tuin'
YT_TagRandomList[6] = 'Beleef de Lente'
YT_TagRandomList[7] = 'koolmees'
YT_TagRandomList[8] = 'mees'
YT_TagRandomList[9] = 'in mijn tuin'
YT_TagRandomList[10] = 'life nestkast'
YT_TagRandomList[11] = 'webcam nestkast'
YT_TagRandomList[12] = 'webcam vogelhuisje'
YT_TagRandomList[13] = 'broeden'
YT_TagRandomList[14] = 'camera nestkast'
YT_TagRandomList[15] = 'zelfbouw nestkast'
YT_TagRandomList[16] = 'vogelnest'
YT_TagRandomList[17] = 'vogelnestje'
YT_TagRandomList[18] = 'zelfbouw nestkast'
YT_TagRandomList[19] = 'zelfbouw vogelhuis'
YT_TagRandomList[20] = 'netkastcamera'
YT_TagRandomList[21] = 'birdbox'
YT_TagRandomList[22] = 'birdhouse'
YT_TagRandomList[23] = 'DIY birdhouse'
YT_TagRandomList[24] = 'DIY birdbox'
YT_TagRandomList[25] = 'birdbox camera'
YT_TagRandomList[26] = 'birdhouse camera'
YT_TagRandomList[27] = 'DIY bird house'
YT_TagRandomList[28] = 'DIY bird box'
YT_TagRandomList[29] = 'birdbox webcam'
YT_TagRandomList[30] = 'birdhouse webcam'

MTBRecordings = 5400                                            # Defines the minimum time in seconds between youtube video clip captures and upload, the default value is 5400 which equals 1,5 hour
OnlineVideoCleapUpAfter = 5
EarliestHour = 6                                                # Before this hour during the day no recordings are allowed (default value=6 which is 6:00AM)
LatestHour = 21                                                 # After this hour during the day no recordings are allowed (default value=21 which is 9:00PM)
ChannelCleaningHour = 23                                        # Defines at which hour the youtube channel cleaning takes place(if enabled by 'YTCleaning') default value=23 which is 11:00PM)
YTCleaning = 'yes'                                              # Defines if daily cleaning-up of youtube channel takes place (default is 'yes')
MaxNoVideos = 30                                                # Defines maximum number of video in youtube channel (if enabled by 'YTCleaning')

CameraResolutionX = 1920
CameraResolutionY = 1080
CameraRotation = 180
CameraFramerate = 15
CameraBrightness = 80
CameraContrast = 80

RecordingDuration = 20                                          # Defines the lenght in seconds of each uploaded video clip. PAY ATTENTION! Severely test the required memory and upload time before you change the default value of 20.

OnScreenName = 'yes'
OnScreenDateTime = 'yes'
OnScreenTempHum = 'yes'
OnScreenDebug = 'no'

MTBHB = 30                                                      # Defines the time in seconds between open data mqtt messages (default value is 600 which equals 10 minutes)
MinSensorloops = 3                                              # Defines number of required sensor read validations. Default value is 3.
                                                                # PLEASE NOTICE: When you make MinSensorloops too big you will miss high speed birds flying in and and only record leaving birds.
                                                                #                When you make MinSensorloops too small you will enjoy watching an empty birdhouse with insects flying in and out.


configfileversion = 1
