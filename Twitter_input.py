#!/usr/bin/env python
import sys
import socket
import time
import globals
import RPi.GPIO as GPIO
from twython import TwythonStreamer
from twython import Twython

# Twitter application authentication for @hmuham7
APP_KEY = '2ZKhoaqOmPWtaxbunwLb8bEcl'
APP_SECRET = 'rIvACXB3VwbmnfGPPA0sAcKiWNHNtnlCfX2nArbnhLuyx1Li7t'
OAUTH_TOKEN = '2580010906-OCwRjPlBoC1vBvbqUvYggMSLJiIVbiox9k1ac27'
OAUTH_TOKEN_SECRET = 'rFE5jrWsQ71ipO94fYtUwe292gGeU1HMJtIGlFuTkCTDQ'


#Setting up global variable to be used later
instruction = ''


# Setup callbacks from Twython Streamer
class BlinkyStreamer(TwythonStreamer):
        def on_success(self, data):
                if 'text' in data:
                        print data['text'].encode('utf-8')
                        str = data['text']

                        # Parsing mechanism
                        strlist = str.split("_")
                        instruction = strlist[0]
			if len(strlist) > 1:
				instruction =+ strlist[1]

                        #Client side connection after receiving the IP and port number of Recipient RPi
                        HOST = globals.server_ip    # The remote host
                        PORT = 5000  # The same port as used by the server

                        #Sockect initialization
                        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        s.connect((HOST, PORT))
                        
                        s.send(instruction)  # Sending the instruction to Recipient RPi
                        data = s.recv(1024)
                        #print 'Response from Server: ', repr(data)   #Receiving response from server

                        api = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)  # a new object for sending the response


                        #Sending the response tweet
                        if data:
                                tweetStr = '@hmuham7' + str
                                api.update_status(status=tweetStr)
                                print "Tweeted: " + tweetStr
                        s.close()
                        stream = BlinkyStreamer(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
                        stream.statuses.filter(follow='2580010906')     # user ID is used to track users account for upcoming feeds.

# Create streamer
try:
        stream = BlinkyStreamer(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
        stream.statuses.filter(follow='2580010906')

except KeyboardInterrupt:
        print 'Interface has been Terminated Manually'


