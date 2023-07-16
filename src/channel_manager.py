import json
import os
from os import path

class ChannelManager:
    def __init__(self):
        self.channels = self._load_channels()

    def _load_channels(self):
        os.makedirs("data", exist_ok=True)
        if not path.exists('data/channels.json'):
            with open('data/channels.json', 'w') as f:
                json.dump([], f)
            return []
        with open('data/channels.json', 'r') as f:
            return json.load(f)

    def save_channel(self, channel):
        channel = channel.lstrip(':')  
        if channel not in self.channels:
            self.channels.append(channel)
            self._write_channels()

    def remove_channel(self, channel):
        channel = channel.lstrip(':') 
        if channel in self.channels:
            self.channels.remove(channel)
            self._write_channels()

    def _write_channels(self):
        os.makedirs("data", exist_ok=True)
        with open('data/channels.json', 'w') as f:
            json.dump(self.channels, f)

    def get_channels(self):
        return self.channels
