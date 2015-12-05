#!/usr/bin/env python

"""
Pi3: Sensor
"""

import time
import pika
import uuid

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

	# Open the file that contains the temperature
	# 	device connected to the Pi.
	file = open("/sys/bus/w1/devices/28-031572f40aff/w1_slave")
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
	print temperature

	time.sleep(1)
