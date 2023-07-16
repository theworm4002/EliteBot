import ssl
import time
import json
import base64
import socket

class Bot:
    def __init__(self, config_file, ChannelManager, Logger):
        self.config = self._load_config(config_file)        
        self.channel_manager = ChannelManager
        self.logger = Logger
        self.connected = False
        self.ircsock = None

    def _load_config(self, config_file):
        with open(config_file, 'r') as file:
            config = json.load(file)
        return config

    def _decode(self, bytes):
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

    def _ircsend(self, msg):
        if msg != '':
            self.ircsock.send(bytes(f'{msg}\r\n','UTF-8'))

    def _parse_message(self, message):
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

    def connect(self):
        self.ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ircsock.settimeout(240)

        if str(self.config['BPORT'])[:1] == '+':
            self.ircsock = ssl.wrap_socket(self.ircsock)
            port = int(self.config['BPORT'][1:])
        else:
            port = int(self.config['BPORT'])

        if 'BBINDHOST' in self.config:
            self.ircsock.bind((self.config['BBINDHOST'], 0))

        self.ircsock.connect_ex((self.config['BSERVER'], port))
        self._ircsend(f'NICK {self.config["BNICK"]}')
        self._ircsend(f'USER {self.config["BIDENT"]} * * :{self.config["BNAME"]}')
        if self.config['UseSASL']:
           self._ircsend('CAP REQ :sasl')

    def start(self):
        while True:
            if not self.connected:
                try:
                    self.connect()
                    self.connected = True
                except Exception as e:
                    self.logger.error(f"Connection error: {e}")
                    time.sleep(60)
                    continue

            try:
                recvText = self.ircsock.recv(2048)
                if not recvText:
                    self.connected = False
                    continue

                ircmsg = self._decode(recvText)
                source, command, args = self._parse_message(ircmsg)
                print(f"Received: source: {source} | command: {command} | args: {args}")
                self.logger.debug(f"Received: source: {source} | command: {command} | args: {args}")

                if command == "PING":
                    nospoof = args[0][1:] if args[0].startswith(':') else args[0]
                    self._ircsend(f'PONG :{nospoof}')

                if command == 'CAP' and args[1] == 'ACK' and 'sasl' in args[2]:
                    self._ircsend('AUTHENTICATE PLAIN')

                elif command == 'AUTHENTICATE' and args[0] == '+':
                    authpass = self.config["SANICK"] + '\x00' + self.config["SANICK"] + '\x00' + self.config["SAPASS"]
                    ap_encoded = str(base64.b64encode(authpass.encode('UTF-8')), 'UTF-8')
                    self._ircsend('AUTHENTICATE ' + ap_encoded)

                elif command == '903':
                    self._ircsend('CAP END')

                if command == 'PRIVMSG':
                    channel, message = args[0], args[1]
                    if message.startswith('!moo'):
                        self._ircsend(f'PRIVMSG {channel} :moo')

                if command == '001':
                    for channel in self.channel_manager.get_channels():
                        self._ircsend(f'JOIN {channel}')

                if command == 'INVITE':
                    channel = args[1]
                    self._ircsend(f'join {channel}')
                    self.channel_manager.save_channel(channel)
                    print(f'JOIN {channel}')

            except Exception as e:
                self.logger.error(f"Error: {e}")
                self.connected = False

        self.ircsock.close()
