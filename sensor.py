#!/usr/bin/env python

"""
Pi3: Sensor
"""

import sys
import time
import socket
import globals

# Number of samples to take (& compute average for)
numSamples = 0
averageTemperature = 0

'''	Set up socket	'''
"""

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
except socket.error, (value, message):
	if s:
		s.close()
	print 'Could not open socket: ' + message
	sys.exit(1)
"""





while 1:
	numSamples = numSamples + 1

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

	averageTemperature = averageTemperature + temperature

	# Compute average temperature every 30 seconds (30 samples)
	if numSamples == 30:
		averageTemperature = averageTemperature / numSamples

		# Client transmits data to server & returns how much
		#	data was sent to it.
#		s.send(averageTemperature)
#		print 'Sent ' + averageTemperature + ' to the server'

		print 'average temperature: ' + str(averageTemperature)
	
		numSamples = 0
		averageTemperature = 0
	
	print 'temp: ' + str(temperature)
		
	# Retrieve data from server with a buffer size as the
	#	argument, indicating the maximum size it will
	#	handle at a time.
#	data = s.recv(SIZE)
#	print 'Received: ' + data + ' from server.'

	time.sleep(1) # Sample every second

s.close() # Close the socket
