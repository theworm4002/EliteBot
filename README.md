# IRC Bot

This is an IRC bot written in Python. It connects to an IRC server, authenticates using SASL if desired, and responds to various commands. It is also able to join and save channels that it is invited to.

## Requirements

- Python 3
- A configuration file `config.py` containing the following variables:
  - `BSERVER`: the IRC server to connect to
  - `BPORT`: the port to use for the connection (can be preceded with a `+` to specify a secure connection)
  - `BNICK`: the desired bot nickname
  - `BIDENT`: the bot's ident
  - `BNAME`: the bot's real name
  - `UseSASL`: a boolean indicating whether or not to use SASL authentication
  - `SANICK`: the bot's SASL account name (if using SASL)
  - `SAPASS`: the bot's SASL password (if using SASL)
  - `SSLCERT`: a boolean indicating whether or not to verify the SSL certificate when using a secure connection
  
## Usage

To run the bot, simply execute the script with `python3 irc_bot.py`. The bot will connect to the specified server and authenticate if necessary. It will then listen for commands and respond accordingly.

## Commands

The following commands are recognized by the bot:

- `!join`: causes the bot to join the specified channel
- `!part`: causes the bot to leave the specified channel
- `!invite`: invites the bot to the specified channel
- `!save`: saves the specified channel to the list of saved channels

## Saving Channels

The bot is able to save a list of channels that it should automatically join upon connecting to the server. To add a channel to this list, use the `!save` command while in the desired channel. The bot will then join the channel whenever it reconnects to the server.

## Contributing

If you have any suggestions or improvements for the bot, feel free to create a pull request.
