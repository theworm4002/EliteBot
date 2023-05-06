#!/usr/bin/env python3

import subprocess
import sys
import bot


def main():
    if len(sys.argv) < 2:
        print("Usage: ./elitebot.py <config_file>")
        sys.exit(1)

    config_file = sys.argv[1]
    config = bot.load_config(config_file)

    try:
        subprocess.Popen(["nohup", "python", "-c", "import bot; bot.main(" + str(config) + ")", "&"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("EliteBot started successfully!")
    except Exception as e:
        print(f"Error starting EliteBot: {e}")


if __name__ == "__main__":
    main()
