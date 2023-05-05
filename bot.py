#!/usr/bin/python3

import json
import os
import ssl
import socket
import time
import base64
import logging
from os import path


def load_config(config_file):
    logging.debug("Loading configuration from: %s", config_file)
    with open(config_file, 'r') as file:
        config = json.load(file)
    return config

connected = False

os.makedirs("logs", exist_ok=True)
logging.basicConfig(level=logging.DEBUG,
                    filename='logs/elitebot.log',
                    filemode='w',
                    format='%(asctime)s - %(levelname)s - %(message)s')
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
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

def connect(config):
    global ircsock
    global connected

    ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ircsock.settimeout(240)

    if str(config['BPORT'])[:1] == '+':
        ircsock = ssl.wrap_socket(ircsock)
        port = int(config['BPORT'][1:])
    else:
        port = int(config['BPORT'])

    if 'BBINDHOST' in config:
        ircsock.bind((config['BBINDHOST'], 0))

    logging.debug("Connecting to server: %s:%s", config['BSERVER'], port)
    ircsock.connect_ex((config['BSERVER'], port))
    ircsend(f'NICK {config["BNICK"]}')
    ircsend(f'USER {config["BIDENT"]} * * :{config["BNAME"]}')
    if config['UseSASL']:
       ircsend('CAP REQ :sasl')

def join_saved_channels():
    logging.debug("Joining saved channels")
    
    channels = load_channels()
    
    for channel in channels:
        ircsend(f'JOIN {channel}')
        print(f'JOIN {channel}')

def save_channel(channel):
    logging.debug("Saving channel: %s", channel)
    
    channels = load_channels()
    
    if channel not in channels:
        channels.append(channel)
        
        os.makedirs("data", exist_ok=True)
        with open('data/channels.json', 'w') as f:
            json.dump(channels, f)

def load_channels():
    os.makedirs("data", exist_ok=True)

    if not path.exists('data/channels.json'):
        with open('data/channels.json', 'w') as f:
            json.dump([], f)
        return []

    with open('data/channels.json', 'r') as f:
        return json.load(f)
        
def main(config):
    global connected

    while True:
        if not connected:
            try:
                connect(config)
                connected = True
            except Exception as e:
                logging.exception("Error connecting to server: %s", e)
                time.sleep(60)  # Wait 60 seconds before retrying the connection
                continue

        try:
            recvText = ircsock.recv(2048)
            if not recvText:  # If an empty message is received, the connection is closed
                logging.warning("Connection closed by server")
                connected = False
                continue

            ircmsg = decode(recvText)
            line = ircmsg.strip('\r\n')
            logging.info(line)

            if ircmsg.startswith('PING :') or (ircmsg.find('PING :') != -1 and ircmsg.lower().find('must') == -1):
                nospoof = ircmsg.split('PING :', 1)[1]
                if nospoof.find(' ') != -1: nospoof = nospoof.split()[0]
                ircsend(f'PONG :{nospoof}')
                
            if line.find('ACK :sasl') != -1 or ircmsg.find('ACK :sasl') != -1:
               ircsend('AUTHENTICATE PLAIN')
         
            elif ircmsg.find('AUTHENTICATE +') != -1:
               authpass = config["SANICK"] + '\x00' + config["SANICK"] + '\x00' + config["SAPASS"]
               ap_encoded = str(base64.b64encode(authpass.encode('UTF-8')), 'UTF-8')
               ircsend('AUTHENTICATE ' + ap_encoded)

            elif ircmsg.find(f' 903 {config["BNICK"]} :') != -1:
               ircsend('CAP END')

            # Add this condition to handle the !quit command
            if ircmsg.find(f':!quit') != -1:
                ircsend(f'QUIT :Goodbye!')
                connected = False
                break

            if ircmsg.find(f'INVITE {config["BNICK"]} :') != -1:
                channel = line.split(' ')[3]
                ircsend(f'JOIN {channel}')
                save_channel(channel)

            if ircmsg.find(f' 001 {config["BNICK"]} :') != -1:
                join_saved_channels()

            if ircmsg.find(f':!moo') != -1:
                channel = ircmsg.split(' ')[2]
                ircsend(f'PRIVMSG {channel} :moo')

        except Exception as e:
            logging.exception("Unexpected error occurred: %s", e)
            connected = False
        except BrokenPipeError as e:
            logging.error("Broken pipe error: %s", e)
            connected = False
        except Exception as e:
            logging.exception("Unexpected error occurred: %s", e)
            connected = False

    ircsock.close()
