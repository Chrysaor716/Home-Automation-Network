#!/usr/bin/env python

"""
An echo client that allows the user to send multiple lines to the server.
Entering a blank line will exit the client.
"""

import socket
import sys
import pickle

class Home:
    def __init__(self): 
        self.lights = False
        self.fans = False
        self.temp = 72

    def report_status(self, client):
        data = pickle.dumps(self)
        client.send(data)

host = 'localhost'
port = 50000
size = 1024
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host,port))
sys.stdout.write('%')

while 1:
    # read from keyboard
    line = sys.stdin.readline()
    if line == '\n':
        break
    s.send(line)
    data = s.recv(size)
    if 'getStat' in line:
    	print 'status of home'
    	home = pickle.loads(data)
    	print 'lights', home.lights
    	print 'fans', home.fans
    	print 'temp', home.temp
    else:
    	sys.stdout.write(data)
    sys.stdout.write('%')
s.close()