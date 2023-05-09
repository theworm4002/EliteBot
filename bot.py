#!/usr/bin/env python3

import json
import os
import ssl
import socket
import time
import base64
import sys
from os import path
from src.logging import Logger

def load_config(config_file):
    with open(config_file, 'r') as file:
        config = json.load(file)
    return config

connected = False
logger = Logger('logs/elitebot.log')

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

    ircsock.connect_ex((config['BSERVER'], port))
    ircsend(f'NICK {config["BNICK"]}')
    ircsend(f'USER {config["BIDENT"]} * * :{config["BNAME"]}')
    if config['UseSASL']:
       ircsend('CAP REQ :sasl')

def join_saved_channels(config):
    
    channels = load_channels()
    
    for channel in channels:
        ircsend(f'JOIN {channel}')

def save_channel(channel):
    
    channel = channel.lstrip(':')  # Remove leading colon, if any
    channels = load_channels()
    
    if channel not in channels:
        channels.append(channel)
        
        os.makedirs("data", exist_ok=True)
        with open('data/channels.json', 'w') as f:
            json.dump(channels, f)

def remove_channel(channel):
    
    channel = channel.lstrip(':')  # Remove leading colon, if any
    channels = load_channels()
    
    if channel in channels:
        channels.remove(channel)
        
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
        
def parse_message(message):
    parts = message.split()

    if not parts:
        return None, None, []

    source = parts[0][1:] if parts[0].startswith(':') else None
    command = parts[1] if source else parts[0]
    args_start = 2 if source else 1
    args = []
    trailing_arg_start = None

    for i, part in enumerate(parts[args_start:], args_start):
        if part.startswith(':'):
            trailing_arg_start = i
            break
        else:
            args.append(part)

    if trailing_arg_start is not None:
        args.append(' '.join(parts[trailing_arg_start:])[1:])

    return source, command, args

        
def main(config):
    global connected

    while True:
        if not connected:
            try:
                connect(config)
                connected = True
            except Exception as e:
                logger.error(f"Connection error: {e}")
                time.sleep(60)
                continue

        try:
            recvText = ircsock.recv(2048)
            if not recvText:
                connected = False
                continue

            ircmsg = decode(recvText)
            source, command, args = parse_message(ircmsg)
            print(f"Received: source: {source} | command: {command} | args: {args}")
            logger.debug(f"Received: source: {source} | command: {command} | args: {args}")

            if command == "PING":
                nospoof = args[0][1:] if args[0].startswith(':') else args[0]
                ircsend(f'PONG :{nospoof}')

            if command == 'CAP' and args[1] == 'ACK' and 'sasl' in args[2]:
                ircsend('AUTHENTICATE PLAIN')

            elif command == 'AUTHENTICATE' and args[0] == '+':
                authpass = config["SANICK"] + '\x00' + config["SANICK"] + '\x00' + config["SAPASS"]
                ap_encoded = str(base64.b64encode(authpass.encode('UTF-8')), 'UTF-8')
                ircsend('AUTHENTICATE ' + ap_encoded)

            elif command == '903':
                ircsend('CAP END')

            if command == 'PRIVMSG':
               channel, message = args[0], args[1]

               if message.startswith('!moo'):
                  ircsend(f'PRIVMSG {channel} :moo')

            if command == '001':
                join_saved_channels(config)

        except Exception as e:
            logger.error(f"Error: {e}")
            connected = False

    ircsock.close()
