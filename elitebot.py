#!/usr/bin/python3

import ssl
import socket
from EliteBotConfg import *
 
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

def decode(bytes):
    try: text = bytes.decode('utf-8')
    except UnicodeDecodeError:
        try: text = bytes.decode('latin1')
        except UnicodeDecodeError:
            try: text = bytes.decode('iso-8859-1')
            except UnicodeDecodeError:
                text = bytes.decode('cp1252')			
    return text
 
SendIRC(f'NICK {BNICK}')
SendIRC(f'USER {BIDENT} * * :{BNAME}')

while True:
    recvText = ircsock.recv(2048)
    ircmsg = decode(recvText)
    line = ircmsg.strip('\n\r')
    print(line)

    if ircmsg.find(f' 001 {BNICK} :') != -1:
        SendIRC(f'JOIN {BHOME}')

    if ircmsg.find('PING') != -1:
        pongis = ircmsg.split(' ', 1)[1] 
        SendIRC(f'PONG {pongis}')
        
    if ircmsg.find(f'443' {BNICK} :') != -1:
        SendIRC(f'NICK {BALT}')
        
    if ircmsg.find('say hi to') != -1:
        Nick2TellFkOff = ircmsg.split('say hi to ')[1]
        SendMsg(f'No! Fuck {Nick2TellFkOff}')

