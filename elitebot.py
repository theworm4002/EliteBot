#!/usr/bin/env python3

import sys
import bot

def main():
    if len(sys.argv) < 2:
        print("Usage: ./elitebot.py <config_file>")
        sys.exit(1)

    config_file = sys.argv[1]
    config = bot.load_config(config_file)

    try:
        print("EliteBot started successfully!")
        bot.main(config)
    except Exception as e:
        print(f"Error starting EliteBot: {e}")

if __name__ == "__main__":
    main()
