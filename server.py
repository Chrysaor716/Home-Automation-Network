#!/usr/bin/env python 

""" 
An echo server that uses threads to handle multiple clients at a time. 
Entering any line of input at the terminal will exit the server. 
""" 

import select 
import socket 
import sys 
import pickle
import threading 

class Home:
    def __init__(self): 
        self.lights = False
        self.fans = False
        self.temp = 72

    def report_status(self, client):
        data = pickle.dumps(self)
        client.send(data)


class Server: 
    def __init__(self): 
        self.host = '' 
        self.port = 50000 
        self.backlog = 5 
        self.size = 1024 
        self.server = None 
        self.threads = [] 
	self.home = Home()

    def open_socket(self): 
        try: 
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
            self.server.bind((self.host,self.port)) 
            self.server.listen(5) 
        except socket.error, (value,message): 
            if self.server: 
                self.server.close() 
            print "Could not open socket: " + message 
            sys.exit(1) 

    def run(self): 
        self.open_socket() 
        input = [self.server,sys.stdin] 
        running = 1 
        while running: 
            inputready,outputready,exceptready = select.select(input,[],[]) 

            for s in inputready: 

                if s == self.server: 
                    # handle the server socket 
                    c = Client(self.server.accept(), self.home) 
                    c.start() 
                    self.threads.append(c) 

                elif s == sys.stdin: 
                    # handle standard input 
                    junk = sys.stdin.readline() 
                    running = 0 

        # close all threads 

        self.server.close() 
        for c in self.threads: 
            c.join() 

class Client(threading.Thread): 
    def __init__(self,(client,address), home): 
        threading.Thread.__init__(self) 
        self.client = client 
        self.address = address 
        self.size = 1024 
	self.home = home
        print self.address

    def run(self): 
        running = 1 
        while running: 
            data = self.client.recv(self.size) 
            if data:
                words = data.split() 
                if 'PI1' in data:
                    if 'getStat' in data:
                        self.home.report_status(self.client)
                    elif 'fans' in data:
                        self.home.fans = not self.home.fans
                        client.send('ACK\n')
                    elif 'lights' in data:
                        self.home.lights = not self.home.lights
                        self.client.send('ACK\n')
                    else:
                        self.client.send('NACK\n')
                elif 'PI3' in data:
                    #self.client.send('receiving from pi 3\n')
                    if 'temp' in data:
                        self.home.temp = words[2]
                        self.client.send('ACK\n')
                    else:
                        self.client.send('NACK\n')
                elif 'PI4' in data:
                    if 'getStat' in data:
                        self.home.report_status(self.client)
                    else:
                        self.client.send('NACK\n')
                else: 
                    self.client.send(data) 
            else: 
                self.client.close() 
                running = 0 

if __name__ == "__main__": 
    s = Server() 
    s.run()
