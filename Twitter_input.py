#!/usr/bin/env python
import sys
import socket
import pickle
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

class Home:
    def __init__(self): 
        self.lights = False
        self.fans = False
        self.temp = 72

    def report_status(self, client):
        data = pickle.dumps(self)
        client.send(data)

# Setup callbacks from Twython Streamer
class BlinkyStreamer(TwythonStreamer):
        def on_success(self, data):
                if 'text' in data:
                        print data['text'].encode('utf-8')
                        str = data['text']

                        # Parsing mechanism
			if str == 'temp':
				instruction = 'PI1 getStat'
			else:
				instruction = "PI1" + str
			
			host = globals.server_ip
			port = 50000
			size = 1024
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			s.connect((host,port))
			sys.stdout.write('%')

   
                        s.send(instruction)  # Sending the instruction to Recipient RPi
                        data = s.recv(size)
    
			api = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)  # a new object for sending the response
	
			if instruction == 'getStat' or instruction == 'temp':
    				print 'status of home'
    				home = pickle.loads(data)
    				print 'lights', home.lights
    				print 'fans', home.fans
    				print 'temp', home.temp
				tweetStr = '@hmuham7 Status of Home: ' + str(home.lights) + str(home.fans) + str(home.temp)
				api.update_status(status=tweetStr)
    			
			if instruction == 'lights ON' or instruction == 'lights OFF':
				if data == 'ACK':
					light = 'Lights status has been changed'
					print light
					tweetStr = '@hmuham7 ' + str(light)
					api.update_status(status=tweetStr)
				else:
					light = 'Lights status is the same'
                                        print light
                                        tweetStr = '@hmuham7 ' + str(light)
                                        api.update_status(status=tweetStr)
			
			if instruction == 'fans ON' or instruction == 'fans OFF':
				if data == 'ACK':
					fan = 'Fans status has been changed'
					print fan
					tweetStr = '@hmuham7 ' + str(fan)
                                	api.update_status(status=tweetStr)
				else:
					fan = 'Fans status is the same'
                                        print fan
                                        tweetStr = '@hmuham7 ' + str(fan)
                                        api.update_status(status=tweetStr)
			
			else:			
    				sys.stdout.write(data)
    				sys.stdout.write('%')

                        s.close()
                        stream = BlinkyStreamer(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
                        stream.statuses.filter(follow='2580010906')     # user ID is used to track users account for upcoming feeds.

# Create streamer
try:
        stream = BlinkyStreamer(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
        stream.statuses.filter(follow='2580010906')

except KeyboardInterrupt:
        print 'Interface has been Terminated Manually'


