# Are we on our local dev machine?
import logging
import platform
import sys
import discord
import builtins
from discord.ext.commands import Bot

# Constants


BOT_PREFIX = ('?')

if platform.system() == 'Windows':
    DEBUG = True
elif platform.system() == 'Linux':
    DEBUG = False
else:  # I don't know what the hell is going on
    sys.exit("This is an unsupported system")

client = Bot(command_prefix=BOT_PREFIX)
builtins.client = client

if DEBUG:

    BOT_TOKEN = 'NTE5NzA2ODQ4NTg1MTg3MzMy.DujPDg.5kr_-LfnCUeRLTR23yaqFY97OWo'
    # Testing Discord
    SERVER_ID = 373782910010130442
    # bot-test channel
    SIGNUP_LOG_CHANNEL_ID = 518513396484800512
    OFFICER_CHANNEL_ID = 543925704358756352
    logging.basicConfig(filename='Asuna.log', filemode='w', format='%(asctime)s - %(levelname)s - %(message)s',
                        level=logging.DEBUG)
else:

    BOT_TOKEN = 'NTE4NTUzNTcyNDI2NjQ1NTA0.DuShbw.TwNTD0i5vvgjbM27QtHCYG3vY44'
    # Incurable Insanity Discord
    SERVER_ID = 269224197299896320
    # botspam channel
    SIGNUP_LOG_CHANNEL_ID = 480506881237057566
    # Asuna-communications channel
    OFFICER_CHANNEL_ID = 544214746249822209
    logging.basicConfig(filename='Asuna.log', format='%(asctime)s - %(levelname)s - %(message)s',
                        level=logging.INFO)


discord_events.init()
client.run(BOT_TOKEN)
