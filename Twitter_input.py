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
APP_KEY = 'yjalXaP0cJMdmk6FtOWwa32sD'
APP_SECRET = '2mXoeI4iRNamLXJbEMfNPMfvAA5Ina5H79VIVj2STdRk1Bw560'
OAUTH_TOKEN = '2580010906-BtNa5Ikw8AP7f0Kh4GE4AbmReCMWJHnTaJs3NSx'
OAUTH_TOKEN_SECRET = 'Mex5kY88EYseVCs7WcFIUbPr5r4awXh8SyrmWSDgMwJfa'


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
                        #print data['text'].encode('utf-8')
                        str_data = data['text']

                        # Parsing mechanism
			if str_data == 'temp':
				instruction = 'PI1 getStat'
			else:
				instruction = "PI1 " + str_data
			print 'Instruction: ',instruction, '\n'
	
			host = globals.server_ip
			port = 50000
			size = 1024
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			s.connect((host,port))
			#sys.stdout.write('%')

   
                        s.send(instruction)  # Sending the instruction to Recipient RPi
                        data = s.recv(size)
    
			api = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)  # a new object for sending the response
			
			epoch_time = time.mktime(time.localtime())

			if str_data == 'getStat' or str_data == 'temp':
				if data:
    					print 'Status of Home:'
    					home = pickle.loads(data)
    					
					if home.lights == False:
                                                light = 'OFF'
                                        else:
                                                light = 'ON'
                                        if home.fans == False:
                                                fan = 'OFF'
                                        else:
                                                fan = 'ON'
					print 'Lights are:     ', light
    					print 'Fans are:       ', fan
    					print 'Temperature is: ', home.temp, 'C'
					print '\n'
					
					tweetStr = '@hmuham7 Status of Home (@Time: ' + str(epoch_time) + ') : ' + 'Lights are ' + str(light) + ', Fans are ' + str(fan) + ' and Temperature is ' + str(home.temp) + 'C'
					api.update_status(status=tweetStr)
    			
			if str_data == 'lights ON' or str_data == 'lights OFF':
				if data == 'ACK\n':
					light = '@Time: ' + str(epoch_time) + ' The Lights status has been changed'
					print light
					tweetStr = '@hmuham7 ' + str(light)
					api.update_status(status=tweetStr)
				else:
					light = '@Time: ' + str(epoch_time) + ' The Lights status is the same'
                                        print light
                                        tweetStr = '@hmuham7 ' + str(light)
                                        api.update_status(status=tweetStr)
			
			if str_data == 'fans ON' or str_data == 'fans OFF':
				if data == 'ACK\n':
					fan = '@Time: ' + str(epoch_time) + ' The Fans status has been changed'
					print fan
					tweetStr = '@hmuham7 ' + str(fan)
                                	api.update_status(status=tweetStr)
				else:
					fan = '@Time: ' + str(epoch_time) + ' The Fans status is the same'
                                        print fan
                                        tweetStr = '@hmuham7 ' + str(fan)
                                        api.update_status(status=tweetStr)
			
# Create streamer
try:
        stream = BlinkyStreamer(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
        stream.statuses.filter(follow='2580010906')

except KeyboardInterrupt:
        print '\nInterface has been Terminated Manually'


