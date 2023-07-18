import os
import sys
from src import *

def main():
    #  Getting current Dir
    exePath =  os.path.dirname(os.path.abspath(__file__))

    # ConfFile
    config_file = f'{exePath}/config.json'

    # Setup logger 
    logFile =  f'{exePath}/logs/elitebot.log'
    logTool = Logger(logFile)    

    chMang = ChannelManager()
    
    # Run the bot
    bot = Bot(config_file, chMang, logTool)

    try:
        print("EliteBot started successfully!")
        bot.start()  
    except Exception as e:
        print(f"Error starting EliteBot: {e}")

if __name__ == "__main__":
    main()
