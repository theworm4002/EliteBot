#!/usr/bin/python3

import ssl
import socket
from config import *
 
ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

if str(BPORT)[:1] == '+':
    print('Use SSL')
    ircsock = ssl.wrap_socket(ircsock)
    BPORT = int(BPORT[1:])
else:
    BPORT = int(BPORT)

ircsock.settimeout(240)

print(f'Connecting to {BSERVER} :{BPORT}')
ircsock.connect_ex((BSERVER, BPORT))

def SendIRC(msg):
    if msg != '': ircsock.send(bytes(f'{msg}\r\n','utf-8'))

def SendMsg(msg, target=BHOME): # Sends messages to the target.
    SendIRC("PRIVMSG "+ target +" :"+ msg)
 
SendIRC(f'NICK {BNICK}')
SendIRC(f'USER {BIDENT} * * :{BNAME}')

while True:
    recvText = ircsock.recv(2048)
    text = recvText.decode('utf-8') 
    line = text.split('\r\n')
    print(line)

    if text.find('PING') != -1:
        pongis = text.split(':')[1]
        SendIRC(f'PONG {pongis}')
        SendIRC(f'JOIN {BHOME}')
    
    if text.find('say hi to') != -1:
        Nick2TellFkOff = text.split('say hi to ')[1]
        SendMsg(f'No! Fuck {Nick2TellFkOff}')
