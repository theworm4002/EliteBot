################################################################################
# IRC CONFIGURATION
#
# This configuration file contains all the necessary settings for connecting to
# an IRC server and interacting with it.
#
# Please make sure to update the values below according to your needs.
###############################################################################

# IRC server address
#
# This should be the address of the IRC server that you want to connect to.
#
# Examples:
#   'irc.example.com'
##
BSERVER = 'irc.example.net'

# IRC server port number
#
# This should be the port number of the IRC server.
#
# If the port number starts with a '+' sign, it will be treated as an SSL/TLS
# port and the connection will be made using SSL/TLS.
#
# Examples:
#   6667 (plain text)
#   +6697 (SSL/TLS)
##
BPORT = +6697

# Desired nickname for the bot
#
# This should be the nickname that you want the bot to use when connecting to
# the IRC server.
#
# Examples:
#   'MyBot'
#   'BottyMcBotface'
##
BNICK = 'elitebot'

# Desired ident for the bot
#
# This should be the ident that you want the bot to use when connecting to the
# IRC server.
#
# Examples:
#   'mybot'
#   'bot'
##
BIDENT = 'elitebot'

# Desired name for the bot
#
# This should be the name that you want the bot to use when connecting to the
# IRC server.
#
# Examples:
#   'My Bot'
#   'The Bot'
##
BNAME = 'elitebot'

# Use SASL authentication
#
# Set this to True to use SASL authentication when connecting to the IRC server,
# or False to disable SASL authentication.
#
# SASL authentication is an optional feature that allows you to authenticate
# with the IRC server using a separate username and password, instead of using
# the nickname and ident as credentials.
#
# If you set this to True, you will also need to provide a SASL username and
# password in the SANICK and SAPASS variables, respectively.
##
UseSASL = True

# Use SSL/TLS with certificate verification
#
# Set this to True to use SSL/TLS with certificate verification when connecting
# to the IRC server, or False to disable SSL/TLS.
#
# SSL/TLS is an optional feature that allows you to establish a secure,
# encrypted connection to the IRC server. Certificate verification ensures that
# the server's SSL/TLS certificate is valid and issued by a trusted authority.
#
# If you set this to True, you will also need to use an SSL/TLS port number in
# the BPORT variable.
##
SSLCERT = True

# SASL username
#
# This should be the SASL username that you want to use for SASL authentication.
# Only needed if UseSASL is True.
#
# Examples:
#   'mybot'
#   'bottymcbotface'
##
SANICK = 'elitebot'

# SASL password
#
# This should be the SASL password that you want to use for SASL authentication.
# Only needed if UseSASL is True.
##
SAPASS = 'elite//789//'