#!/usr/bin/env python

"""
Pi3: Sensor
"""

import time

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

	# Get second line of file, split it into space-
	#	delimited elements, and gets the 10th
	#	(index 9) of these elements
	tempdata = fileRead.split("\n")[1].split(" ")[9]

	# Dumps the first two characters ("t=") of 10th
	#	element and converts the remaining from
	#	a string to a float and divide by 1000
	temperature = float(tempdata[2:])
	temperature  = temperature / 1000
	print temperature

	time.sleep(1)
