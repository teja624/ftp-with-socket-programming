#!/usr/bin/env python

#Programming assignment 1 for cs372 online by Kamal Chaya
#A simple ftp client implementation

import socket
import sys
import errno
from os import *

#functions
def getHostPort():
    """Get the hostName and port number
    to connect to from the command line arguments"""
    if (len(sys.argv) != 3):
        print "Incorrect command line arguments given\n"
        sys.exit()

    else:    
        hostName = sys.argv[1] + '.engr.oregonstate.edu'
        portNum = int(sys.argv[2])
        return hostName, portNum

def createControlSocket():
    """Creates a socket for the TCP control connection 
    and returns it, and handles the appropriate exceptions"""

    try:
        return socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Create the socket
    except socket.error:
        print "Error in socket creation"
        sys.exit()

def connectControlSocket(controlSocket, hostName, portNum):
    """Connects the socket to the host and port, and 
    handles any exceptions"""
    try:
        controlSocket.connect((hostName, portNum))
    except socket.error as e:
        if e.errno == errno.ECONNREFUSED: #Handling the exception of the socket connection being refused
            print "error: socket connection refused"
            sys.exit()
        else:
            print "Error: a socket exception occured"
            sys.exit(1)

    print 'Sucessfully established TCP control connection\n'        

def getCmdAndSend(controlSocket):
    """Get the command to execute on the server as user input.
    Send the command to the server.
    exit the program if an invalid command is entered"""
    print 'valid commands are \'list\' and \'get <filename>\'\n'
    cmd = raw_input('Enter a command')

    #send the command
    controlSocket.send(cmd)    
    recieved = controlSocket.recv(1024)
    print "Recieved: ", recieved
    controlSocket.close()


#Main program
hostName, portNum = getHostPort() #Get the hostname and port number
controlSocket = createControlSocket() #Make the socket for the client
connectControlSocket(controlSocket, hostName, portNum) # connect the client socket
getCmdAndSend(controlSocket) #get the command from user input and send to the server


