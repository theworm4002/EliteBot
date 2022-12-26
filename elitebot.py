#!/usr/bin/python3

from config import *
import ssl
import socket
import time
import base64
import logging
import os
from os import path

ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connected = False

# Set up logging to a file
logging.basicConfig(level=logging.DEBUG,
                    filename='irc.log',
                    filemode='w',
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Set up logging to the console
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)


def decode(bytes):
    try: 
        text = bytes.decode('utf-8')
    except UnicodeDecodeError:
        try: 
            text = bytes.decode('latin1')
        except UnicodeDecodeError:
            try: 
                text = bytes.decode('iso-8859-1')
            except UnicodeDecodeError:
                text = bytes.decode('cp1252')
    return text

def ircsend(msg):
    if msg != '':
        ircsock.send(bytes(f'{msg}\r\n','UTF-8'))

def connect():
    global ircsock
    global connected
    global BPORT
    
    ircsock.settimeout(240)
    if SSLCERT: 
        ssl.CERT_REQUIRED = True
    else:
        ssl.CERT_REQUIRED = False
        
    if str(BPORT)[:1] == '+':
        ircsock = ssl.wrap_socket(ircsock)
        BPORT = int(BPORT[1:])
    else:
        BPORT = int(BPORT)
    
    ircsock.connect_ex((BSERVER, BPORT))
    ircsend(f'NICK {BNICK}')
    ircsend(f'USER {BIDENT} * * :{BNAME}')
    if UseSASL:
        ircsend('CAP REQ :sasl')
    
def save_channel(channel):
    with open('channels.txt', 'a') as f:
        f.write(channel + '\n')
        
def join_saved_channels():
    if not path.exists('channels.txt'):
        with open('channels.txt', 'w') as f:
            pass  # create the file if it does not exist
    else:
        with open('channels.txt', 'r') as f:
            channels = f.readlines()
            for channel in channels:
                ircsend(f'JOIN {channel.strip()}')
                print(f'JOIN {channel.strip()}')

def main():
    global connected
    if not connected:
        connect()
        connected = True

    while connected:
        recvText = ircsock.recv(2048)
        ircmsg = decode(recvText)
        line = ircmsg.strip('\n\r')
        logging.info(line)
        print(line)
        
        queued_lines = []
        if ircmsg.find('PING') != -1:
            nospoof = ircmsg.split(' ', 1)[1]
            ircsend("PONG " + nospoof)

        if line.find('ACK :sasl') != -1 or ircmsg.find('ACK :sasl') != -1:
            ircsend('AUTHENTICATE PLAIN')
         
        elif ircmsg.find('AUTHENTICATE +') != -1:
            authpass = SANICK + '\x00' + SANICK + '\x00' + SAPASS
            ap_encoded = str(base64.b64encode(authpass.encode('UTF-8')), 'UTF-8')
            ircsend('AUTHENTICATE ' + ap_encoded)

        elif ircmsg.find(f' 903 {BNICK} :') != -1:
            ircsend('CAP END')
			
        if ircmsg.find(f'INVITE {BNICK} :') != -1:
            channel = line.split(' ')[3]
            ircsend(f'JOIN {channel}')
            save_channel(channel)
			
        for line in queued_lines:
            time.sleep(5)
            ircsock.send(bytes(f'{line}\r\n','UTF-8'))
        queued_lines = []
		
        if ircmsg.find(f' 001 {BNICK} :') != -1:
            join_saved_channels()
        
        if ircmsg.find(f':!moo') != -1:
            ircsend(f'PRIVMSG #ct :moo')
        
main()