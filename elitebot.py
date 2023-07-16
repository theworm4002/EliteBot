import sys
from src.bot import Bot

def main():
    if len(sys.argv) < 2:
        print("Usage: python elitebot.py <config_file>")
        sys.exit(1)

    config_file = sys.argv[1]
    bot = Bot(config_file)

    try:
        print("EliteBot started successfully!")
        bot.start()  
    except Exception as e:
        print(f"Error starting EliteBot: {e}")

if __name__ == "__main__":
    main()
