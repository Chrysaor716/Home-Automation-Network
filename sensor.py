#!/usr/bin/env python

"""
Pi3: Sensor
Pi4: Output Devices
	This script will be run on a Pi that will act
		as both Pi3 and Pi4.
"""

import sys
import time
import signal
import socket
import globals
import RPi.GPIO as GPIO
import pickle

class Home:
    def __init__(self): 
        self.lights = False
        self.fans = False
        self.temp = 72

    def report_status(self, client):
        data = pickle.dumps(self)
        client.send(data)

# Initialize GPIO ports
gpio23 = 16 # GPIO 23 is pin 16 (RPi Model B+)
gpio24 = 18 # GPIO 24 is pin 18

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False) # Turn off GPIO warnings
# Set GPIO pins as outputs
GPIO.setup(gpio23, GPIO.OUT)
GPIO.setup(gpio24, GPIO.OUT)
GPIO.output(gpio23, GPIO.LOW)
GPIO.output(gpio24, GPIO.LOW)

'''	Set up socket	'''

host = globals.server_ip
port = 50000
SIZE = 1024	# Max data size client will handle at a time
s = None	# Initialize socket variable
try:
	# Create a socket object stored in s that will use
	#	IPv4 and TCP.
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.settimeout(5)
	# Connect to the server.
	s.connect((host, port))

	print 'connection opened'	
	# Handle socket connections (close when necessary)
	def signal_handler(signal, frame):
		s.close()
		print 'connection closed'
		GPIO.cleanup()
		sys.exit(0)
	signal.signal(signal.SIGINT, signal_handler)

except socket.error, (value, message):
	if s:
		s.close()
	print 'Could not open socket: ' + message


while 1:
	# Note: Enter this command to the terminal:
	#	ls -l /sys/bus/w1/devices
	# The temperature sensor appears with an
	#	address in the format 28-00000xxxxxx
	# Note: Enter this command to the terminal:
	#	cat /sys/bus/w1/devices/28-00000xxxxxx/w1_slave
	# The last parameter of the second line (starting
	#	with a "t=") displays a value 1000
	#	times the temperature reading in Celcius.

	try:
		# Open the file that contains the temperature
		# 	device connected to the Pi.
		file = open("/sys/bus/w1/devices/28-031572f40aff/w1_slave")
	except IOError as e:
		print 'Could not open file. Error ' + e
	fileRead = file.read()
	file.close()

	# Split text with new lines and get the second line.
	# 	Split line into space-delimited elements
	#	(separate line into words) and get the 10th
	#	word (index 9) of these elements.
	tempdata = fileRead.split("\n")[1].split(" ")[9]

	# Omit the first two characters ("t=") of 10th
	#	element and convert from a string to a float
	#	and divide by 1000.
	temperature = float(tempdata[2:])
	temperature = temperature / 1000

	# Client transmits data to server & returns how much
	#	data was sent to it.
	sendData = 'PI3 temp ' + str(temperature)
	s.send(sendData)

	# Retrieve data from server with a buffer size as the
	#	argument, indicating the maximum size it will
	#	handle at a time.
	data = s.recv(SIZE)
	print 'Received: ' + data + ' from server.'

	s.send('PI4 getStat')
	data = s.recv(SIZE)

	home = pickle.loads(data)
	
	print 'lights: ', home.lights
	if home.lights == False:
		GPIO.output(gpio23, GPIO.LOW)
	else:
		GPIO.output(gpio23, GPIO.HIGH)

	print 'fans: ', home.fans
	if home.fans == False:
		GPIO.output(gpio24, GPIO.LOW)
	else:
		GPIO.output(gpio24, GPIO.HIGH)
	
	print 'temperature: ', home.temp
	
	time.sleep(1) # Sample every second

s.close() # Close the socket
